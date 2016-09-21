#!/usr/bin/env python

# IDA Binary/DIF Patcher Written in Python 3.5.2

_VERSION = "1.0"

REPLACE_OLD = (0x01 << 0)
RENAME_NEW = (0x01 << 2)
LOG = (0x01 << 3)
DIF_HEADLINE = "This difference file has been created by IDA"

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

from sys import argv
from re import split
import os
from time import strftime
from struct import unpack
from extern.Events import EventEmitter
from io import FileIO, SEEK_CUR, SEEK_END, SEEK_SET


class Patcher(EventEmitter):
    def __init__(self, flags):
        super().__init__(True)
        self.__log_cache = []

        self.__flags = flags
        self.__file_path_bin = ''
        self.__file_path_dif = ''

    def patch(self, path_bin='', path_dif=''):
        try:
            if path_bin is '' and path_dif is '':
                if not len(argv) > 2:
                    raise FileNotFoundError("Invalid number of arguments, Syntax: <file_path_bin> <file_path_dif>")
                else:
                    self.__file_path_bin = str(r'' + argv[0][0:] + '')
                    self.__file_path_dif = str(r'' + argv[1][0:] + '')
            else:
                self.__file_path_bin = path_bin
                self.__file_path_dif = path_dif

            if self.is_patch_ready(self.__file_path_dif):
                if self.is_patch_ready(self.__file_path_bin):
                    file_bin = None
                    file_target_bin = None

                    if self.__flags & RENAME_NEW:
                        bin_name = self.__file_path_bin[self.__file_path_bin.rfind('\\') + 1:]
                        new_bin_path = self.__file_path_bin.replace(bin_name,
                                                                    bin_name + '_patched_' + strftime("%d-%m-%y"))

                        for i in (i for i in range(0, 50)):
                            if not os.path.exists(new_bin_path + '_' + str(i)):
                                new_bin_path += ('_' + str(i))
                                break
                            else:
                                continue
                        file_target_bin = open(new_bin_path, 'wb+')

                    if file_target_bin is not None:
                        file_bin = open(self.__file_path_bin, 'rb+')
                    else:
                        file_bin = open(self.__file_path_bin, 'wb+')
                        file_target_bin = file_bin

                    file_dif = open(self.__file_path_dif, 'r')

                    dif_hex = []
                    with file_dif as file:
                        if str(file_dif.readline()).strip('\t\n\r') is str(DIF_HEADLINE):
                            self.emit('abort', "Invalid DIF-File Headline.")
                        else:
                            # Blank Line, get that out of the way
                            file_dif.readline()
                            self.emit('log', 'Original DIF-Target File Name: {}'.format(file_dif.readline()))

                            for line in file:
                                cur_spl = split(r'[ :\n]', line)

                                val_off = int((cur_spl[0]).strip().encode('ascii'), 16)
                                src_val = int((cur_spl[2]).strip().encode('ascii'), 16)
                                new_val = int((cur_spl[3]).strip().encode('ascii'), 16)

                                print(val_off)
                                if src_val > 0xFF and src_val != 0xFFFFFFFF or new_val > 0xFF and \
                                    new_val is not 0xFFFFFFFF:
                                    self.emit('abort', "Selected File is not a DIF-File.")
                                    break

                                dif_hex.append((val_off, new_val))

                    file_size_bin = os.fstat(file_bin.fileno()).st_size

                    for elem in dif_hex:
                        if elem[0] is 0xFFFFFFFF:
                            if file_size_bin > elem[0]:
                                file_size_bin = elem[0]
                            continue
                        while elem[0] >= file_size_bin:
                            file_bin.seek(0, SEEK_END)
                            file_bin.write(bytes([elem[0]]))

                        file_bin.seek(elem[0], 0)
                        file_bin.write(bytes([elem[1]]))

                    if file_target_bin is not None:
                        file_target_bin.close()

                    file_bin.close()
                    file_dif.close()

                else:
                    self.emit('abort', "There is no valid path to your binary file.")
            else:
                self.emit('abort', "There is no valid path to your .dif file")

        except RuntimeError:
            raise RuntimeError("Thrown Exception at 'patch(self, path_bin, path_diff) unsolved Exception.")
        finally:
            print("successfully")

    @staticmethod
    def is_patch_ready(path):
        if os.path.abspath(path):
            ext = path[path.find('.') + 1:]

            if ext is 'exe' or 'dif':
                return True
            else:
                return False
        else:
            raise SyntaxError("Given path is not absolute.")
