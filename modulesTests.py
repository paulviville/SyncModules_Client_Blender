import sys
import bpy
import uuid
import json

from pathlib import Path

modules_path = Path(bpy.data.filepath).parent 

if str(modules_path) not in sys.path:
    sys.path.insert(0, str(modules_path))
        
import SyncModulesPython as SyncModules
import SyncModulesViews_Python as SyncModulesViews
from SyncModulesPython.Core.ModulesRegistry import ModulesRegistry




print(ModulesRegistry)

print(SyncModulesViews)
print(dir(SyncModulesViews))
print(dir(SyncModules))

UUID = uuid.uuid4()

def outputFn( data ):
    print(data)


registry = ModulesRegistry(outputFn)
print(registry)


