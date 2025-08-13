# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

from bpy.props import BoolProperty, StringProperty, CollectionProperty, PointerProperty, IntProperty
from bpy.types import PropertyGroup, Material, Image

class MaterialProperties(PropertyGroup):
    material: PointerProperty(type=Material)
    enabled: BoolProperty()

class SceneProperties(PropertyGroup):
    # uhhhhhh
    source_uv_name: StringProperty(
        name="Source UV Name",
        default="SourceUV",
        maxlen=64,
    )
    baking_uv_name: StringProperty(
        name="Baking UV Name",
        default="BakingUV",
        maxlen=64,
    )

    do_seams: BoolProperty(
        name="Overwrite Seams",
        description="Automatically generates Seams based on sharp edges",
        default=False
    )
    do_source_uv: BoolProperty(
        name="Write Source UV",
        description="Creates/Overrides UV maps for the SourceUV",
        default=True,
    )
    do_baking_uv: BoolProperty(
        name="Write Baking UV",
        description="Creates/Overrides UV maps for the BakingUV",
        default=True,
    )
    
    use_cube_project_source: BoolProperty(
        name="Cube Project Source UV",
        description="Use Square Project on the Source UV",
        default=False,
    )
    use_cube_project_baking: BoolProperty(
        name="Cube Project Baking UV",
        description="Use Square Project on the UV before aligning it",
        default=False,
    )

    enabled_materials: CollectionProperty(
        name="Enabled Materials",
        description="Materials for which the UV maps will be generated",
        type=MaterialProperties,
    )


    source_texture_size: IntProperty(
        name="Source Texture Size",
        description="Common size of the source textures (used for calculating atlas size)",
        subtype="PIXEL",
        min=256,
        max=8192,
        step=64,
        default=1024,
    )

    target_node_name: StringProperty(
        name="Target Node Name",
        default="FNAK Image Texture",
        maxlen=64,
        description="Name of the Image Texture Node which will be selected/modified",
    )
    target_image: PointerProperty(
        name="Target Image",
        type=Image,
    )