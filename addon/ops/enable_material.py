# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

from bpy.types import Operator
import bpy

class PrintEnabledOperator(Operator):
    bl_idname = "material.print_enabled"
    bl_label = "Print Enabled Materials"
    bl_description = "Does what it says"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.scene.fnak_util_settings.enabled_materials is not None

    def execute(self, context):
        for m in context.scene.fnak_util_settings.enabled_materials:
            print(m.name)

        return {'FINISHED'}

class EnableMaterialOperator(Operator):
    bl_idname = "material.fnak_enable"
    bl_label = "Enable Material for FNAK"
    bl_description = "Does what it says"
    bl_options = {'REGISTER', 'UNDO'}

    material_name: bpy.props.StringProperty()

    @classmethod
    def poll(cls, context):
        return context.scene.fnak_util_settings.enabled_materials is not None
    
    def execute(self, context):
        material = bpy.data.materials.get(self.material_name, None)

        if material is not None:
            enabled = context.scene.fnak_util_settings.enabled_materials

            found = -1
            for i, m in enumerate(enabled):
                if m.material == material:
                    found = i
                    break
            
            if found >= 0:
                enabled[found].material = material
                enabled[found].enabled = True
            else:
                a = enabled.add()
                a.material = material
                a.enabled = True
            
            enabled.update()
        else:
            self.report({'ERROR_INVALID_INPUT'}, f"Material {self.material_name} not found!")

        return {'FINISHED'}

class DisableMaterialOperator(Operator):
    bl_idname = "material.fnak_disable"
    bl_label = "Disable Material for FNAK"
    bl_description = "Does what it says"
    bl_options = {'REGISTER', 'UNDO'}

    material_name: bpy.props.StringProperty()

    @classmethod
    def poll(cls, context):
        # return context.scene.fnak_util_settings.enabled_materials is not None and context.active_object.active_material is not None
        return context.scene.fnak_util_settings.enabled_materials is not None
    
    def execute(self, context):
        material = bpy.data.materials.get(self.material_name, None)

        if material is not None:
            enabled = context.scene.fnak_util_settings.enabled_materials

            found = -1
            for i, m in enumerate(enabled):
                if m.material == material:
                    found = i
                    break
            
            if found >= 0:
                enabled.remove(found)
            else:
                self.report({'WARN'}, f"Material {self.material_name} not found in enabled.")
            
            enabled.update()
        else:
            self.report({'ERROR_INVALID_INPUT'}, f"Material {self.material_name} not found!")

        return {'FINISHED'}

class EnableAllOperator(Operator):
    bl_idname = "material.fnak_enable_all"
    bl_label = "Enable every Material for FNAK"
    bl_description = "Does what it says"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.scene.fnak_util_settings.enabled_materials is not None and bpy.data.materials is not None
    
    def execute(self, context):
        materials = bpy.data.materials
        enabled = context.scene.fnak_util_settings.enabled_materials
        
        enabled.clear()

        for m in materials:
            a = enabled.add()
            a.material = m
            a.enabled = True

        enabled.update()

        return {'FINISHED'}

class DisableAllOperator(Operator):
    bl_idname = "material.fnak_disable_all"
    bl_label = "Disable every Material for FNAK"
    bl_description = "Does what it says"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.scene.fnak_util_settings.enabled_materials is not None
    
    def execute(self, context):
        enabled = context.scene.fnak_util_settings.enabled_materials
        
        enabled.clear()

        enabled.update()

        return {'FINISHED'}