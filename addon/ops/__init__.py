# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

import bpy
from .print_name import PrintNameOperator
from .enable_material import *
from .generate_uv import GenerateUVOperator, BulkSelectUVOperator, BulkRenderActivateUVOperator, BulkDeleteUVOperator
from .select_node import BulkEditNodeOperator

# SURELY there is a better way to do this, right?

def register():
    print("registering ops")
    bpy.utils.register_class(PrintNameOperator)
    bpy.utils.register_class(PrintEnabledOperator)
    bpy.utils.register_class(EnableMaterialOperator)
    bpy.utils.register_class(DisableMaterialOperator)
    bpy.utils.register_class(EnableAllOperator)
    bpy.utils.register_class(DisableAllOperator)
    bpy.utils.register_class(GenerateUVOperator)
    bpy.utils.register_class(BulkSelectUVOperator)
    bpy.utils.register_class(BulkRenderActivateUVOperator)
    bpy.utils.register_class(BulkDeleteUVOperator)
    bpy.utils.register_class(BulkEditNodeOperator)

def unregister():
    print("unregistering ops")
    bpy.utils.unregister_class(PrintNameOperator)
    bpy.utils.unregister_class(PrintEnabledOperator)
    bpy.utils.unregister_class(EnableMaterialOperator)
    bpy.utils.unregister_class(DisableMaterialOperator)
    bpy.utils.unregister_class(EnableAllOperator)
    bpy.utils.unregister_class(DisableAllOperator)
    bpy.utils.unregister_class(GenerateUVOperator)
    bpy.utils.unregister_class(BulkSelectUVOperator)
    bpy.utils.unregister_class(BulkRenderActivateUVOperator)
    bpy.utils.unregister_class(BulkDeleteUVOperator)
    bpy.utils.unregister_class(BulkEditNodeOperator)