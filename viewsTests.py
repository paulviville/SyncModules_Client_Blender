import bpy
import uuid

objects = { }

def add_tests ( ):
    bpy.ops.object.empty_add( )
    obj = bpy.context.object
    obj_id = str( uuid.uuid4( ) )

    objects[ obj_id ] = obj
    return obj_id, obj

id0, obj0 = add_tests( )
id1, obj1 = add_tests( )
id1, obj1 = add_tests( )

obj1.parent = obj0



def on_depsgraph_update(scene, depsgraph):
    for update in depsgraph.updates:
        obj = getattr(update.id, "name", None)

        if isinstance(update.id, bpy.types.Object):
            if update.is_updated_transform:
                print(f"Moved: {update.id.name}")

# Register
if on_depsgraph_update not in bpy.app.handlers.depsgraph_update_post:
    bpy.app.handlers.depsgraph_update_post.append(on_depsgraph_update)