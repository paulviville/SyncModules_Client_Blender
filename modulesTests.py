import sys
import bpy
import uuid
import json

from pathlib import Path
import importlib 

modules_path = Path(bpy.data.filepath).parent 

if str(modules_path) not in sys.path:
    sys.path.insert(0, str(modules_path))
        
import SyncModulesPython as SyncModules
import SyncModulesViews_Python as SyncModulesViews


package = SyncModules.__name__
packageViews = SyncModulesViews.__name__

mods = [
    m for name, m in sys.modules.items()
    if name == package or name.startswith(package + ".") or name == packageViews or name.startswith(packageViews + ".")
]

# Reload deepest modules first
mods.sort(key=lambda m: m.__name__.count("."), reverse=True)

for m in mods:
    importlib.reload(m)


print(dir(SyncModules))
print(dir(SyncModules.Core.ModulesRegistry))

print(SyncModules.Core.ModulesRegistry)

print(SyncModulesViews)
print(dir(SyncModulesViews))
print(dir(SyncModules))

UUID = uuid.uuid4()

def outputFn( data ):
    print(data)


registry = SyncModules.Core.ModulesRegistry.ModulesRegistry(outputFn)
viewsregistry = SyncModulesViews.ViewsRegistry.ViewsRegistry(registry)

bpy.app.driver_namespace["registry"] = registry
bpy.app.driver_namespace["viewsregistry"] = viewsregistry