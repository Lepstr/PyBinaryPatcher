#!/usr/bin/env python

# IDA Binary Patcher Written in Python 3.5.2

_VERSION = "1.0"

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
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
# ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import Patcher


class UserInterface:
    def __init__(self):
        self.patcher = Patcher.Patcher(Patcher.RENAME_NEW)
        self.patcher.on('abort', lambda ex: print(ex))
        self.patcher.on('log', lambda log: print("[LOG] " + str(log)))

        self.patcher.patch(r'C:\Users\Skloa\Documents\Personal\Reverse Engineering\SemperVideoEngineeringChallange\CrackMe v2\CrackMe v2.exe',
                           r'C:\Users\Skloa\Documents\Personal\Reverse Engineering\SemperVideoEngineeringChallange\CrackMe v2\CrackMe v2.dif')



def main():
    interface = UserInterface()

if __name__ == '__main__':
    main()




