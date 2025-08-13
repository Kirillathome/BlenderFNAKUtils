# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

from bpy.types import Operator
import bpy

class BulkEditNodeOperator(Operator):
    bl_idname = "node.bulk_edit"
    bl_label = "Bulk Edit Nodes"
    bl_description = "Adds/Selects every Image Texture Node and sets their Textures using the specified settings."
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.scene.fnak_util_settings.enabled_materials is not None and context.scene.fnak_util_settings.target_image is not None

    def execute(self, context):
        props = context.scene.fnak_util_settings
        enabled = props.enabled_materials
        name = props.target_node_name
        image = context.scene.fnak_util_settings.target_image

        for i, e in enumerate(enabled):
            node = None
            if name in enabled[i].material.node_tree.nodes.keys():
                node = enabled[i].material.node_tree.nodes[name]
                print("node exists")
            else:
                node = enabled[i].material.node_tree.nodes.new("ShaderNodeTexImage")
                node.name = name
                print("node does not exist")

            # for n in enabled[i].material.node_tree.nodes:
            #     n.select = False

            node.label = name
            node.image = image
            enabled[i].material.node_tree.nodes.active = node

        return {'FINISHED'}