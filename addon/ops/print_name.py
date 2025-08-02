# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

import bpy

class PrintNameOperator(bpy.types.Operator):
    bl_idname = "object.print_name"
    bl_label = "Print Name"
    bl_description = "Does what it says"

    @classmethod
    def poll(cls, context):
        return context.selected_objects is not None

    def execute(self, context):
        for o in context.selected_objects:
            print(o.name)

        return {'FINISHED'}    