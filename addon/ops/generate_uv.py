from bpy.types import Operator
import bpy, bmesh, math, mathutils

class GenerateUVOperator(Operator):
    bl_idname = "object.generate_uv"
    bl_label = "Generate UVs"
    bl_description = "Generates the two UV maps using the specified settings."
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.mode == 'OBJECT' and context.scene.fnak_util_settings.enabled_materials is not None

    def execute(self, context):
        # getting the relevant meshes
        props = context.scene.fnak_util_settings
        enabled = props.enabled_materials
        uv_factor = math.ceil(math.sqrt(len(enabled))) # y'know, how many rows/columns the atlas should have
        meshes = [o for o in context.scene.objects if o.type == 'MESH' and has_enabled_materials(o, enabled) and o.visible_get()]

        bpy.ops.object.select_all(action='DESELECT')

        # DONT'T FORGET:
        # obj: meshes[i]
        # source_uv: uvs[props.source_uv_name]
        # baking_uv: uvs[props.baking_uv_name]
        # uvs: meshes[i].data.uv_layers

        for i, obj in enumerate(meshes):
            #region setting up or getting the one UV layer
            # print(f"Working on object {meshes[i].name}")
            uvs = meshes[i].data.uv_layers
            if props.source_uv_name in uvs:
                # print(f"{props.source_uv_name} is already a UV map")
                pass
            else:
                # print(f"{props.source_uv_name} not a UV map, creating new...")
                uvs.new(name=props.source_uv_name)
            uvs[props.source_uv_name].active = True
            uvs[props.source_uv_name].active_render = True
            #endregion

            #region processing seams
            if props.do_seams:
                meshes[i].select_set(True)

                bpy.ops.object.mode_set_with_submode(mode='EDIT', mesh_select_mode={'EDGE'})

                bpy.ops.mesh.select_all(action='SELECT')
                bpy.ops.mesh.mark_seam(clear=True) # clear previous seams
                bpy.ops.mesh.select_all(action='DESELECT')

                bpy.ops.mesh.edges_select_sharp(sharpness=math.radians(60)) # math is better than typing it out manually ig
                bpy.ops.mesh.mark_seam(clear=False) # select new seams

                bpy.ops.mesh.select_all(action='DESELECT')

                bpy.ops.object.mode_set(mode='OBJECT')
                
                meshes[i].select_set(False)
            #endregion

            #region processing source uv
            if props.do_source_uv:
                meshes[i].select_set(True)
                bpy.ops.object.mode_set(mode='EDIT')
                bpy.ops.mesh.select_all(action='SELECT')

                if props.use_cube_project_source:
                    bpy.ops.uv.cube_project(clip_to_bounds=True, scale_to_bounds=True) # cube project if enabled

                bpy.ops.object.mode_set(mode='OBJECT')
                
                meshes[i].select_set(False)
            #endregion

            #region setting up or getting the second UV layer
            uvs = meshes[i].data.uv_layers
            if props.baking_uv_name in uvs:
                # print(f"{props.baking_uv_name} is already a UV map")
                pass
            else:
                # print(f"{props.baking_uv_name} not a UV map, creating new...")
                uvs.new(name=props.baking_uv_name)
            uvs[props.baking_uv_name].active = True
            uvs[props.baking_uv_name].active_render = True
            #endregion

            #region processing #2
            if props.do_baking_uv:
                meshes[i].select_set(True)
                bpy.ops.object.mode_set(mode='EDIT')
                bpy.ops.mesh.select_all(action='SELECT')

                if props.use_cube_project_baking:
                    # print("cube projecting for bake")
                    bpy.ops.uv.cube_project(clip_to_bounds=True, scale_to_bounds=True) # cube project if enabled

                # so... what do we do now?
                #region bmesh shenanigans
                bm = bmesh.from_edit_mesh(meshes[i].data)

                uv_lay = bm.loops.layers.uv.active # it SHOULD always be the Baking UV, but what do I know anyway?
                # print(uv_lay.name)
                for face in bm.faces:
                    mat_index = find_material_index_from_int(face.material_index, meshes[i], enabled)
                    if mat_index == -1:
                        continue # not my problem (for now...)

                    # print(f"{meshes[i].name} has a face with material {enabled[mat_index].material.name}")
                    # print(f"index: {mat_index}")

                    for loop in face.loops:
                        uv_vec = loop[uv_lay].uv
                        loop[uv_lay].uv = mathutils.Vector((mat_index % uv_factor, math.floor(mat_index / uv_factor))) / uv_factor + uv_vec / uv_factor
                        # print("Loop UV: %f, %f" % uv[:])

                bmesh.update_edit_mesh(meshes[i].data)
                bm.free()
                #endregion

                bpy.ops.object.mode_set(mode='OBJECT')
                
                meshes[i].select_set(False)
            #endregion

            # reset
            uvs[props.source_uv_name].active_render = True
            uvs[props.baking_uv_name].active = True


        # print("finished!!! (please don't crash)")
        return {'FINISHED'}

class BulkSelectUVOperator(Operator):
    bl_idname = "object.bulk_select_uv"
    bl_label = "Bulk Select UVs"
    bl_description = "Selects the specified UV map for every visible Mesh (if applicable)."
    bl_options = {'REGISTER', 'UNDO'}

    uv_name: bpy.props.StringProperty()

    @classmethod
    def poll(cls, context):
        return context.selected_objects is not None and context.scene.fnak_util_settings is not None
    
    def execute(self, context):
        if self.uv_name == "":
            self.uv_name = context.scene.fnak_util_settings.source_uv_name

        meshes = [o for o in context.scene.objects if o.type == 'MESH' and o.visible_get() and self.uv_name in o.data.uv_layers]
        for m in meshes:
            m.data.uv_layers[self.uv_name].active = True

        return {'FINISHED'}

class BulkRenderActivateUVOperator(Operator):
    bl_idname = "object.bulk_render_activate_uv"
    bl_label = "Bulk Activate UVs"
    bl_description = "Activates the specified UV map for render for every visible Mesh (if applicable)."
    bl_options = {'REGISTER', 'UNDO'}

    uv_name: bpy.props.StringProperty()

    @classmethod
    def poll(cls, context):
        return context.selected_objects is not None and context.scene.fnak_util_settings is not None
    
    def execute(self, context):
        if self.uv_name == "":
            self.uv_name = context.scene.fnak_util_settings.source_uv_name

        meshes = [o for o in context.scene.objects if o.type == 'MESH' and o.visible_get() and self.uv_name in o.data.uv_layers]
        for m in meshes:
            m.data.uv_layers[self.uv_name].active_render = True

        return {'FINISHED'}

class BulkDeleteUVOperator(Operator):
    bl_idname = "object.bulk_delete_uv"
    bl_label = "Bulk Delete UVs"
    bl_description = "Deletes all UV maps except the one specified for EVERY visible Mesh."
    bl_options = {'REGISTER', 'UNDO'}

    uv_name: bpy.props.StringProperty()

    @classmethod
    def poll(cls, context):
        return context.selected_objects is not None and context.scene.fnak_util_settings is not None
    
    def execute(self, context):
        if self.uv_name == "":
            self.uv_name = context.scene.fnak_util_settings.baking_uv_name

        meshes = [o for o in context.scene.objects if o.type == 'MESH' and o.visible_get() and self.uv_name in o.data.uv_layers]
        for i, obj in enumerate(meshes):
            l = list()
            for u in meshes[i].data.uv_layers.values():
                if self.uv_name != u.name:
                    print(f"{u.name} does NOT match the uv_name {self.uv_name}, meaning deletion!")
                    l.append(u.name)
            
            print(f"the full list: ")
            for u in l:
                meshes[i].data.uv_layers.remove(meshes[i].data.uv_layers[u])

        return {'FINISHED'}

def has_enabled_materials(object, enabled):
    for e in enabled:
        for m in object.material_slots.keys():
            if m == e.material.name:
                return True
    
    return False

def find_material_index_from_int(index, object, enabled):
    mat_name = object.material_slots[index].name

    for i, e in enumerate(enabled):
        if e.material.name == mat_name:
            return i

    return -1