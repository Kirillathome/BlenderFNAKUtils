# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

import bpy
from .props import MaterialProperties, SceneProperties

def register():
    print("registering props")
    bpy.utils.register_class(MaterialProperties)
    bpy.utils.register_class(SceneProperties)
    bpy.types.Scene.fnak_util_settings = bpy.props.PointerProperty(type=SceneProperties)

def unregister():
    print("unregistering props")
    bpy.utils.unregister_class(SceneProperties)
    bpy.utils.unregister_class(MaterialProperties)
    del bpy.types.Scene.fnak_util_settings