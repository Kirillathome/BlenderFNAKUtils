# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

import bpy
from .main_panel import DebugPanel, UVPanel

def register():
    print("registering UI")
    # bpy.utils.register_class(Sidebar)
    bpy.utils.register_class(DebugPanel)
    bpy.utils.register_class(UVPanel)


def unregister():
    print("unregistering UI")
    # bpy.utils.unregister_class(Sidebar)
    bpy.utils.unregister_class(DebugPanel)
    bpy.utils.unregister_class(UVPanel)