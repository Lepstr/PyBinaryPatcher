# PyBinaryPatcher - Python 3.5.2 IDA/.DIF File Patcher
Python Binary Patcher to patch Binary-Files with ".dif" Files from IDA

<b>NOTE:</b> This module is probably not downward compatible with < 3.2

## Usage
````python
from Patcher import Patcher

class MyClass:
  def __init__(self):
    self.patcher = Patcher()
    
    self.patcher.on('abort', lambda msg: print(msg))
    self.patcher.on('log', lambda log: print(log))
  
  def do_patch(self):
    self.patcher.patch('C:\Users\root\Documents\Patch\Patching.exe', 
                       'C:\Users\root\Documents\Patch\Patching.dif')
                       
  
instance = MyClass()
instance.do_patch()
````
Or using the User Interface thats comming soon.

## Module Feature Pipeline
- [x] Basic Patch of Binarys, get overall features working.
- [x] Implement Event System using [Events.py](https://github.com/Lepstr/PyEvent)
- [x] Performance Optimizations

## License
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
<hr />
<b>THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NON INFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.</b>
