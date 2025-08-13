# Blender FNAK Utils

## what is this?

This is a Blender addon that I wrote specifically to assist me in creating the UVs and baking the textures correctly for a large 3D scene.

Since I doubt that many have the same texturing/baking worklow as me, this is more intended to be a **template** for automating **your own** workflow than an actual addon for use.

**TLDR: this addon creates two UV maps, one as the source for baking (using the whole texture), and one as the output for baking (atlas-like).**

## how does this work?

You can choose materials to enable, and the addon will do certain things to every **visible** **Mesh** with at least one **enabled material**.
If nothing extra is enabled, it will only generate two new UV maps: `SourceUV` and `BakingUV`.

You can change the names of the generated maps in the settings.

There are more settings of course:
- `Overwrite Seams`: Clears all seams and marks every sharp edge (60°d) as a Seam
- `Write Source UV`: Doesn't do much by itself, but decides if the Source UV map should be modified
- `Write Baking UV`: Scale the Source UV and align it in a grid (based on the index of the material)
- `Cube Project Source UV`: Cube Projects the Source UV scaled and clipped to bounds (if `Write Source UV` is enabled)
- `Cube Project Baking UV`: Cube Projects the Baking UV before transforming it to the correct spot (if `Write Baking UV` is enabled)
- `Source Texture Size`: Not yet implemented. Will be used to calculate the size of the baking texture

## is it done?
No. There are still a few things that I'd like to add is:
1. Bulk-adding Image Textures/Nodes to all Materials (this is done)
2. Selecting said Nodes to be used as an output for baking (this is also done)
3. Update the README to include documentation on the new features
4. Add pretty images to this README
5. Delete unused code
6. (maybe) select all Mesh that don't have a Material yet

## is it stable?
It worked the last time I tested it, but I wouldn't trust this thing.

**PLEASE make backups before using this!!!**

## can I use this code for my own addon/sell it/whatever?
Feel free to do anything your heart desires. Not like I can stop you. (check the License for more info)