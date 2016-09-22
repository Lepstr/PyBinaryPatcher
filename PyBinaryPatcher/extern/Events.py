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

from extern.collectionex import Collection
from typing import Callable


class Event:
    def __init__(self, name, cb: Callable[..., None], once=False) -> None:
        self.name = name
        self.once = once

        if callable(cb):
            self.callback = cb
        else:
            self.callback = lambda: print("Callback is not registered yet.")

    def dynamic_invoke(self, *arguments) -> None:
        try:
            if len(arguments) > 0:
                self.callback(*arguments)
            else:
                self.callback()
        except RuntimeError:
            print("Thrown exception at 'dynamic_invoke(self, name, *arguments)' [Events.py] class Event")
            exit(1)
        finally:
            if self.once:
                self.name = None
                self.callback = None


class EventCollection(Collection):
    def append(self, item):
        if isinstance(item, Event):
            super().append(item)
        else:
            raise TypeError("Item must be an type of 'Event' [class Event -> [Events.py]]")

    def __getitem__(self, item):
        return super().__getitem__(item)

    def __setitem__(self, key, value):
        super().__setitem__(key, value)

    def __iter__(self):
        super().__iter__()


class EventEmitter:
    def __init__(self, cache=True) -> None:
        self.__listening = EventCollection()
        self.__do_cache = cache
        self.__cache = []

    def emit(self, name, *arguments):
        try:
            event = self.__listening.first_or_none(lambda ev: ev.name == name)

            if event is not None:
                event.dynamic_invoke(*arguments)

                if event.once:
                    self.remove_listener(name)
            else:
                if self.__do_cache and event not in self.__cache:
                    self.__cache.append((name, arguments))
                else:
                    return False
        except RuntimeError:
            raise RuntimeError("Thrown exception at 'emit(self, name, *arguments)' [Events.py] class EventEmitter")

    def on(self, name, cb: Callable[..., None]):
        try:
            if self.__listening.first_or_none(lambda ev: ev.name == name) is None:
                self.__listening.append(Event(name, cb))

            if self.__do_cache:
                if self._check_cache(name):
                    self.__cache.clear()
                    return True
                else:
                    return False
            else:
                return True
        except RuntimeError:
            raise RuntimeError("Thrown exception at 'on(self, name, callback)' [Events.py] class EventEmitter")

    def once(self, name, cb: Callable[..., None]):
        try:
            if not self.__listening.first_or_none(lambda ev: ev.name == name) is None:
                self.__listening.append(Event(name, cb, True))

            if self.__do_cache:
                if self._check_cache(name):
                    self.__cache.clear()
                    return True
                else:
                    return False
            else:
                return True

        except RuntimeError:
            raise RuntimeError("Thrown exception at 'once(self, name, callback)' [Events.py] class EventEmitter")

    def _check_cache(self, name):
        try:
            if len(self.__cache) > 0:
                for el in self.__cache:
                    if el[0] == name:
                        self.emit(el[0], *el[1])
                        return True
                    else:
                        continue
                return False
        except RuntimeError:
            raise RuntimeError("Thrown exception at '_check_cache(self, name)' [Events.py] class EventEmitter.")

    def remove_listener(self, name):
        try:
            for x in self.__listening:
                if x.name == name:
                    self.__listening.remove(x)
                else:
                    continue

        except RuntimeError:
            raise RuntimeError("Thrown exception at 'remove_listener(self, name)' [Events.py] class EventEmitter")

    def remove_all_listeners(self):
        self.__listening.clear()

    def is_listening_on(self, name):
        return self.__listening.first_or_none(lambda ev: ev.name == name)
