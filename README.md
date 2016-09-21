# PyBinaryPatcher - Python 3.5.2 IDA/.DIF File Patcher
Python Binary Patcher to patch Binary-Files with ".dif" Files from IDA

<b>NOTE:</b> This module is probably not downward compatible with < 3.2

## Usage
````python
from Patcher import Patcher

class MyClass:
  def __init__(self):
    self.patcher = Patcher()
    self.patcher.patch('C:\Users\root\Documents\Patch\Patching.exe', 
                       'C:\Users\root\Documents\Patch\Patching.dif')
                       
    self.patcher.on('abort', lambda msg: print(msg))
    self.patcher.on('log', lambda log: print(log))
````
Or using the User Interface thats comming soon.

## Module Feature Pipeline
- [x] Basic Patch of Binarys, get overall features working.
- [x] Implement Event System using [Events.py](https://github.com/Lepstr/PyEvent)
- [ ] Implement User Interface for comfortable use
- [ ] Performance Optimizations
