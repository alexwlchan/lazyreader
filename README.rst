lazyreader
==========

lazyreader is a Python module for doing lazy reading of file objects.

The Python standard library lets you read a file a line-at-a-time, saving you from loading the entire file into memory.
For example:

.. code-block:: python

   with open('large_file.txt') as f:
       for line in f:
           print(line)

lazyreader lets you do the same thing, but with an arbitrary delimiter, and for any object that presents a ``.read()`` method.
For example:

.. code-block:: python

   from lazyreader import lazyread

   with open('large_file.txt') as f:
       for doc in lazyread(f, delimiter=';'):
           print(doc)

This is a snippet of code I spun out from the `Wellcome Digital Platform <https://github.com/wellcometrust/platform-api>`_.
We have large XML and JSON files stored in S3 -- sometimes multiple GBs -- but each file is really a series of "documents", separated by known delimiters.
Downloading and parsing the entire file would be prohibitively expensive, but lazyreader allows us to hold just a single document in memory at a time.

Examples
********

If we have a file stored locally, we can open it and split based on any choice of delimiter.
For example, if we had a text file in which record were separated by commas:

.. code-block:: python

   with open('lots_of_records.txt') as f:
       for doc in lazyread(f, delimiter=';'):
           print(doc)

Another example: we have a file stored in Amazon S3, and we'd like to read it line-by-line.
The `boto3 <https://boto3.readthedocs.io/en/stable/>`_ API gives us a file object for reading from S3:

.. code-block:: python

   import boto3

   s3 = boto3.client('s3')
   s3_object = client.get_object(Bucket='example-bucket', Key='words.txt')
   body = s3_object['Body']

   for doc in lazyread(body, delimiter=b'\n'):
       print(doc)

(This is the use case for which this code was originally written.)

One more example: we're fetching an HTML page, and want to read lines separated by ``<br>`` in the underlying HTML.
Like so:

.. code-block:: python

   import urllib.request

   with urllib.request.urlopen('https://example.org/') as f:
       for doc in lazyread(f, delimiter=b'<br>'):
           print(doc)

Advanced usage
**************

``lazyread()`` returns a generator, which you can wrap to build a pipeline of generators which do processing on the data.

First example: we have a file which contains a list of JSON objects, one per line.
(This is the format of output files from `elasticdump <https://github.com/taskrabbit/elasticsearch-dump>`_.)
What the caller really needs is Python dictionaries, not JSON strings.
We can wrap ``lazyread()`` like so:

.. code-block:: python

   import json

   def lazyjson(f, delimiter=b'\n'):
       for doc in lazyread(f, delimiter=delimiter):

           # Ignore empty lines, e.g. the last line in a file
           if not doc.strip():
               continue

           yield json.loads(doc)

Another example: we want to parse a large XML file, but not load it all into memory at once.
We can write the following wrapper:

.. code-block:: python

   import lxml

   def lazyxml(f, opening_tag, closing_tag):
       for doc in lazyread(f, delimiter=closing_tag):
           if opening_tag not in doc:
               continue

           # We want complete XML blocks, so look for the opening tag and
           # just return its contents
           block = doc.split(opening_tag)[-1]
           yield opening_tag + block

We use both of these wrappers at Wellcome to do efficient processing of large files that are kept in Amazon S3.

Isn't this a bit simple to be a module?
***************************************

Maybe.
There are recipes on Stack Overflow that do very similar, but I find it useful to have in a standalone module.

And it's not completely trivial -- at least, not for me.
I made two mistakes when I first wrote this:

*  I was hard-coding the initial running string as

   .. code-block:: python

      running = b''

   That only works if your file object is returning bytestrings.
   If it's returning Unicode strings, you get a ``TypeError`` (`can't concat bytes to str`) when it first tries to read from the file.

*  After I'd read another 1024 characters from the file, I checked for the delimiter like so:

   .. code-block:: python

      running += new_data
      if delimiter in running:
          curr, running = running.split(delimiter)
          yield curr + delimiter

   For my initial use case, individual documents were `much` bigger than 1024 characters, so the new data would never contain multiple delimiters.
   But with smaller documents, you might get multiple delimiters in one read, and then unpacking the result of ``.split()`` would throw a ``ValueError``.
   So now the code correctly checks and handles the case where a single read includes more than one delimiter.

License
*******

MIT.
