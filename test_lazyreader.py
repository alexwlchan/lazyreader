# -*- encoding: utf-8

from lazyreader import lazyread


class Readable(object):
    def __init__(self, body):
        self.body = body
        self.position = 0

    def read(self, size):
        retval = self.body[self.position:self.position + size]
        self.position += size
        return retval


def test_read_single_line_with_binary_file():
    f = open('README.rst', 'rb')
    assert next(lazyread(f, delimiter=b'\n')) == b'lazyreader\n'


def test_read_single_line_with_unicode_file():
    f = open('README.rst', 'r')
    assert next(lazyread(f, delimiter='\n')) == 'lazyreader\n'


def test_can_read_entire_file():
    expected = [
        'A triplet of lines;',
        'separated by semicolons;',
        'not newlines'
    ]
    f = Readable(''.join(expected))
    assert list(lazyread(f, delimiter=';')) == expected
