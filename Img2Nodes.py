"""
Copyright (C) 2018 Grant Wilk

Img2Nodes is free software: you can redistribute
it and/or modify it under the terms of the GNU General Public License
as published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.

Img2Nodes is distributed in the hope that it will
be useful, but WITHOUT ANY WARRANTY; without even the implied warranty
of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
General Public License for more details.

You should have received a copy of the GNU General Public License along
with Img2Nodes.  If not, see <https://www.gnu.org/licenses/>.
"""


bl_info = {
    "name": "Img2Nodes",
    "author": "Grant Wilk",
    "blender": (2, 79),
    "version": (1, 0, 0),
    "location": "UV/Image Editor",
    "category": "Compositing",
    "description": "An add-on that converts a bunch of images to nodes.",
}

import bpy


class ConvertImage(bpy.types.Operator):
    bl_idname = "img2nodes.convert_image"
    bl_label = "Convert Image"

    def execute(self, context):
        image = bpy.context.space_data.image

        if image is not None:
            pixels = image.pixels
            bpy.context.scene.use_nodes = True
            tree = bpy.context.scene.node_tree
            node_dict = {}
            width = image.size[0]

            for y in range(width):
                for x in range(width):
                    pixel_num = (x + y * width) * 4

                    key = 'node' + str(pixel_num)
                    node_dict[key] = tree.nodes.new(type='CompositorNodeValue')
                    node_dict[key].hide = False

                    node_dict[key].use_custom_color = True
                    node_dict[key].color = (pixels[pixel_num], pixels[pixel_num + 1], pixels[pixel_num + 2])

                    node_dict[key].width = 0
                    node_dict[key].location = (x * 80, y * 80)

        return {'FINISHED'}


def appendto_image_ht_header(self, context):
    """UI code to append to the IMAGE_HT_HEADER space"""
    layout = self.layout
    layout.separator()
    row = layout.row(align=True)
    row.operator(
        "img2nodes.convert_image",
        text="Convert Image",)


def register():
    bpy.utils.register_class(ConvertImage)
    bpy.types.IMAGE_HT_header.append(appendto_image_ht_header)


def unregister():
    bpy.utils.unregister_class(ConvertImage)
    bpy.types.IMAGE_HT_header.remove(appendto_image_ht_header)
