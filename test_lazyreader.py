# -*- encoding: utf-8

import random
import string

import pytest

from lazyreader import lazyread


def random_string(size):
    random.seed(0)
    return ''.join([random.choice(string.printable) for _ in range(size)])


class Readable(object):
    def __init__(self, body):
        self.body = body
        self.position = 0
        self.read_calls = []

    def read(self, size):
        self.read_calls.append(size)
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


@pytest.mark.parametrize('read_size', [1, 10, 27])
def test_reads_file_object_readsize_bytes_at_a_time(read_size):
    f = Readable(random_string(1000))
    lazyread(f, delimiter=';', read_size=read_size)
    assert all([call == read_size for call in f.read_calls])
