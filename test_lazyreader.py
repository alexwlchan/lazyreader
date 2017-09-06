# -*- encoding: utf-8

import boto3
import moto
import pytest

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


@moto.mock_s3
def test_can_read_from_s3():
    s3 = boto3.client('s3')
    s3.create_bucket(Bucket='bukkit')
    s3.put_object(Bucket='bukkit', Key='long_file.txt', Body=b'foo\nbar\nbaz')

    f = s3.get_object(Bucket='bukkit', Key='long_file.txt')['Body']
    assert list(lazyread(f, delimiter=b'\n')) == [b'foo\n', b'bar\n', b'baz']


def test_unexpected_error_is_still_raised():
    class BrokenReadable(object):
        def read(self, size):
            raise RuntimeError("Reading from this object isn't allowed!")

    f = BrokenReadable()

    with pytest.raises(RuntimeError):
        next(lazyread(f, delimiter=b'\n'))
