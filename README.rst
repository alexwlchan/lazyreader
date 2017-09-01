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
