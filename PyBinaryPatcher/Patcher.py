#!/usr/bin/env python

# IDA Binary/DIF Patcher Written in Python 3.5.2

_VERSION = "1.2"

RENAME_NEW = (0x01 << 2)
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
import os
from time import strftime
from extern.Events import EventEmitter
from io import SEEK_END

from shutil import copy


class Patcher(EventEmitter):

    def __init__(self, flags=0):
        super().__init__(True)
        self.__flags = flags

        self.error_message = None
        self.__path_bin = None
        self.__path_dif = None

    def patch(self, path_bin, path_dif):
        try:
            if path_bin is None or path_dif is None:
                if len(argv) > 2:
                    self.__path_bin = r''+argv[0]+''
                    self.__path_dif = r''+argv[1]+''
                else:
                    raise Exception("There are a invalid number of arguments. Syntax: <{0}> <{1}>"
                                    .format("path_bin", "path_dif"))
            else:
                self.__path_bin = path_bin
                self.__path_dif = path_dif

            if self.is_patch_ready(self.__path_bin) and self.is_patch_ready(self.__path_dif):
                file_target_bin = None
                file_target_dif = open(self.__path_dif, 'r', encoding='utf8', errors='ignore')

                if self.__flags & RENAME_NEW:
                    bin_name = self.__path_bin[:self.__path_bin.rfind('.')]

                    bin_name_target = bin_name + '_patched_' + strftime("%y-%d-%m")
                    bin_path_target = None

                    for i in (self.__path_bin.replace(bin_name, (bin_name_target + '_' + str(i))) for i in range(0, 50)):
                        if not os.path.exists(i):
                            bin_path_target = i
                            break
                        else:
                            continue

                    if bin_path_target is None:
                        self.error_message = "You have too many patched Binary-Files in your Folder."

                        if self.is_listening_on('abort'):
                            self.emit('abort', self.error_message)
                            return

                        raise Exception(self.error_message)

                    file_target_bin = open(bin_path_target, 'wb+')
                    copy(self.__path_bin, bin_path_target)

                if file_target_bin is None:
                    file_target_bin = open(self.__path_bin, 'rb+')

                if self.error_message is not None:
                    return

                dif_offset_val = []
                with file_target_dif as dif_file:

                    if str(dif_file.readline()).strip() is str(DIF_HEADLINE):
                        self.error_message = "Selected DIF-File is not an valid DIF-File, please check your Path."

                        if self.is_listening_on('abort'):
                            self.emit('abort', self.error_message)
                            return
                        raise Exception(self.error_message)

                    dif_file.readline()
                    self.emit('log', "Patching Binary-File: {0}".format(str(dif_file.readline()).strip()))

                    for line in (line for line in dif_file):

                        offset = int(((line.strip()[:line.rfind(':')]).strip()).encode('ascii'), 16)

                        _values = ((line.strip()[line.rfind(':')+1:]).strip()).split(' ')
                        prev_val = int(_values[0].encode('ascii'), 16)
                        new_val = int(_values[1].encode('ascii'), 16)

                        if new_val < 0 or new_val > 255 or prev_val < 0 or prev_val > 255:
                            self.error_message = "Selected DIF-File is not an valid DIF-File, {0}".\
                                format("values are greater then 255 or less then zero.")

                            if self.is_listening_on('abort'):
                                self.emit('abort', self.error_message)
                                break
                            raise Exception(self.error_message)

                        dif_offset_val.append((offset, new_val))

                    if self.error_message is not None:
                        return

                with file_target_bin:

                    file_size_bin = os.fstat(file_target_bin.fileno()).st_size
                    for elem in (el for el in dif_offset_val):
                        if elem[0] is 0xFFFFFFFF:
                            if file_size_bin > elem[0]:
                                file_size_bin = elem[0]
                            continue
                        while elem[0] >= file_size_bin:
                            file_target_bin.seek(0, SEEK_END)
                            file_target_bin.write(bytes([elem[0]]))

                        file_target_bin.seek(elem[0], 0)
                        read_byte = file_target_bin.read()[0]

                        if read_byte is elem[1]:
                            warn_msg = "Patcher wasn't able to replace byte at offset <{0}> to byte <{1}>".\
                                format(str(elem[0]), str(elem[1]))
                            self.emit('log', '[WARNING] {0}'.format(warn_msg))
                        else:
                            file_target_bin.seek(elem[0], 0)
                            file_target_bin.write(bytes([elem[1]]))

                            log_msg = "Changed <{0}> => <{1}> at <{2}>".\
                                format(hex(read_byte), hex(elem[1]), hex(elem[0]))
                            self.emit('log', log_msg)

                file_target_bin.close()
                file_target_dif.close()

                if self.error_message is None:
                    self.emit('log', "Patching Successful!")

                    if len(argv) > 0:
                        print("Patching Successful!")
            else:
                self.error_message = "One of your files is not ready to patch, {0}".\
                    format("please check both your Binary and DIF File.")
                if self.is_listening_on('abort'):
                    self.emit('abort', self.error_message)
                    return
                raise Exception(self.error_message)

        except RuntimeError:
            self.error_message = "Wasn't able to Patch Binary with {0} -> {1}".format(path_bin, path_dif)

            if self.is_listening_on('abort'):
                self.emit('abort', self.error_message)
                return

            raise RuntimeError(self.error_message)

    @staticmethod
    def is_patch_ready(path):
        if os.path.abspath(path):
            ext = path[path.rfind('.') + 1:]

            if ext is 'exe' or 'dif':
                return True
            else:
                return False
        else:
            return False

