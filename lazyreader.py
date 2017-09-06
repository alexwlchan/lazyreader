# -*- encoding: utf-8

def lazyread(f, delimiter):
    """
    Generator which continually reads ``f`` to the next instance
    of ``delimiter``.

    This allows you to do batch processing on the contents of ``f`` without
    loading the entire file into memory.

    :param f: Any file-like object which has a ``.read()`` method.
    :param delimiter: Delimiter on which to split up the file.
    """
    # Get an empty string to start with.  We need to make sure that if the
    # file is opened in binary mode, we're using byte strings, and similar
    # for Unicode.  Otherwise trying to update the running string will
    # hit a TypeError.
    try:
        running = f.read(0)
    except Exception as e:

        # The boto3 APIs don't let you read zero bytes from an S3 object, but
        # they always return bytestrings, so in this case we know what to
        # start with.
        if e.__class__.__name__ == 'IncompleteReadError':
            running = b''
        else:
            raise

    while True:
        new_data = f.read(1024)

        # When a call to read() returns nothing, we're at the end of the file.
        if not new_data:
            yield running
            return

        # Otherwise, update the running stream and look for instances of
        # the delimiter.  Remember we might have read more than one delimiter
        # since the last time we checked
        running += new_data
        while delimiter in running:
            curr, running = running.split(delimiter, 1)
            yield curr + delimiter
