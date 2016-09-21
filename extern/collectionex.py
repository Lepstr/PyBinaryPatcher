#!/usr/bin/env python

# Dynamic Event System for Python 3.5.2

# Copyright (c) 2016 Bastian Hoffmann
# All rights reserved

# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
# documentation files (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all copies
# or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING
# BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NON INFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
# ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from abc import ABCMeta, abstractmethod
from typing import Callable

from collections import Iterable


class Enumerable(Iterable, metaclass=ABCMeta):
    def __init__(self, iterable):
        self.__iterable = iterable

        self.__cache = None

    @abstractmethod
    def __getitem__(self, item):
        pass

    @abstractmethod
    def __setitem__(self, key, value):
        pass

    def first_or_none(self, predicate: Callable[..., bool]):
        self.__cache = None
        for elem in self.__iterable:
            if predicate(elem):
                self.__cache = elem
                break
            else:
                continue

        return self.__cache

    def where(self, predicate: Callable[..., bool]):
        self.__cache = []
        for elem in self.__iterable:
            if predicate(elem):
                self.__cache.append(elem)
            else:
                continue

        return self.__cache

    def contains(self, predicate: Callable[..., bool]):
        self.__cache = 0
        for elem in self.__iterable:
            self.__cache += 1
            if predicate(elem):
                break
            else:
                continue

        return self.__cache


class Collection(Enumerable):
    def __init__(self):
        self.__list = []
        super().__init__(self.__list)

    def pop(self):
        removed = self.__list[-1]
        self.remove_at(self.__list[-1])
        return removed

    def last(self):
        return self.__list[-1]

    def append(self, value):
        self.__list.append(value)

    def insert_at(self, idx, value):
        self.__list.insert(idx, value)

    def element_at(self, x):
        return self.first_or_none(lambda elem: elem == x)

    def remove_at(self, idx):
        self.__list.remove(self.__list[idx])

    def remove(self, element):
        self.__list.remove(element)

    def index_of(self, element):
        for ele in self.__list:
            if ele == element:
                return self.__list.index(ele)
            else:
                continue
        return -1

    def clear(self):
        self.__list.clear()

    def count(self):
        return len(self.__list)

    def __getitem__(self, item):
        return self.__list[item]

    def __setitem__(self, key, value):
        self.__list[key] = value

    def __iter__(self):
        return (self.__list[i] for i in range(0, self.count()))



