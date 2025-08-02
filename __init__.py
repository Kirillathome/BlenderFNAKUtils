# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

bl_info = {
    "name": "FNAK Utils",
    "author": "Kirillathome",
    "description": "Horrible utilities for UV & Baking",
    "blender": (3, 0, 0),
    "version": (0, 0, 1)
}

from . import addon

def register():
    print("registering from main file")
    addon.register()

def unregister():
    print("unregistering from main file")
    addon.unregister()