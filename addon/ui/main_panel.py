# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

import bpy
import math
from ..props import MaterialProperties

class Sidebar:
    bl_category = 'FNAK Utils'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'

    @classmethod
    def poll(cls, context):
        return context.mode in {"OBJECT", "EDIT_MESH"}

# class DebugPanel(Sidebar, bpy.types.Panel):
#     bl_idname = 'FNAK_PT_DebugPanel'
#     bl_options = {"DEFAULT_CLOSED"}
#     bl_label = 'Debug'

#     def draw(self, context):
#         layout = self.layout

#         layout.label(text="sup")
#         col = layout.column(align=True)
#         col.operator("object.select_all", text="Select All")

#         col = layout.column(align=True)
#         col.enabled = len(context.selected_objects) >= 1
#         col.operator("object.print_name", text="Print Name")
        
class UVPanel(Sidebar, bpy.types.Panel):
    bl_idname = 'FNAK_PT_UVPanel'
    bl_label = 'UV Management'

    def draw(self, context):
        layout = self.layout
        props = context.scene.fnak_util_settings

        header, panel = layout.panel("options", default_closed=True)
        header.label(text="Options")

        if panel:
            col = panel.column()
            sub = col.column()
            sub.label(text="Source UV Name")
            sub.prop(props, "source_uv_name", text="")
            sub = col.column()
            sub.label(text="Baking UV Name")
            sub.prop(props, "baking_uv_name", text="")
            col = panel.column()
            col.prop(props, "do_seams")
            col.prop(props, "do_source_uv")
            col.prop(props, "do_baking_uv")
            col.prop(props, "use_cube_project_source")
            col.prop(props, "use_cube_project_baking")


        header, panel = layout.panel("all_materials", default_closed=True)
        header.label(text="All Materials")

        if panel:
            col = panel.column(align=True)
            materials = bpy.data.materials
            if materials is not None:
                box = col.box()
                box.operator("material.fnak_enable_all", text="Enable All")
                for m in materials:
                    row = box.row()
                    row.template_icon(box.icon(m))
                    row.label(text=m.name)
                    op = row.operator("material.fnak_enable", text="e")
                    op.material_name = m.name
        
        
        header, panel = layout.panel("enabled_materials", default_closed=True)
        header.label(text="Enabled Materials")

        if panel:
            col = panel.column(align=True)
            enabled = props.enabled_materials
            if enabled is not None:
                box = col.box()
                box.operator("material.fnak_disable_all", text="disable all")
                for m in enabled:
                    row = box.row()
                    row.template_icon(box.icon(m.material))
                    row.label(text=m.material.name)
                    op = row.operator("material.fnak_disable", text="d")
                    op.material_name = m.material.name
        

        header, panel = layout.panel("uv_maps", default_closed=True)
        header.label(text="UV Maps")
        
        if panel:
            col = panel.column(align=True)
            op = col.operator("object.bulk_select_uv", text="Select Source UV")
            op.uv_name = props.source_uv_name
            op = col.operator("object.bulk_select_uv", text="Select Baking UV")
            op.uv_name = props.baking_uv_name
            op = col.operator("object.bulk_render_activate_uv", text="Render Activate Source UV")
            op.uv_name = props.source_uv_name
            op = col.operator("object.bulk_render_activate_uv", text="Render Activate Baking UV")
            op.uv_name = props.baking_uv_name

        col = layout.column()
        col.operator("object.generate_uv", text="Generate UVs")

        # col = layout.column()
        # op = col.operator("material.fnak_enable", text="Enable Material")
        # op.material_name = material_name

class TexturePanel(Sidebar, bpy.types.Panel):
    bl_idname = 'FNAK_PT_TexturePanel'
    bl_label = 'Texture Management'
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout
        props = context.scene.fnak_util_settings

        header, panel = layout.panel("options", default_closed=True)
        header.label(text="Options")

        uv_factor = math.ceil(math.sqrt(len(props.enabled_materials)))
        image_size = uv_factor * props.source_texture_size

        if panel:
            col = panel.column()
            col.prop(props, "source_texture_size")
            sub = col.column()

            sub.label(text="Target Node Name")
            sub.prop(props, "target_node_name", text="")
            sub = col.column()

            sub.label(text="Target Image")
            sub.prop(props, "target_image", text="")

            row = col.row(align=True)
            op = row.operator("image.new", text="New", icon='ADD')
            op.width = image_size
            op.height = image_size
            row.operator("image.open", text="Open", icon='FILE_FOLDER')

            sub = col.column(align=True)
            sub.label(text=f"recommended: {image_size}px")
            sub.label(text=f"({len(props.enabled_materials)}/{uv_factor**2} fit)")

        col = layout.column()
        col.operator("node.bulk_edit")

class DangerPanel(Sidebar, bpy.types.Panel):
    bl_idname = 'FNAK_PT_DangerPanel'
    bl_label = 'Danger Zone'
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout
        props = context.scene.fnak_util_settings
        
        layout.label(text="USE WITH CAUTION!")
        layout.label(text="MAKE BACKUPS!")

        col = layout.column()
        op = col.operator("object.bulk_delete_uv", text="Bulk DELETE UVs")
        op.uv_name = props.baking_uv_name
