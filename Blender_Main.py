import bpy
import ConfigParser
import logging
import os
import json

#Read Settings.ini
config = ConfigParser()
config.read("Settings.ini")

AUTO_LOCATE_PATH    = config["Options"]["AUTO_LOCATE_PATH"]
MAIN_PATH           = config["Options"]["MAIN_PATH"]
UE_AES              = config["Options"]["UE_AES"]
UE_VERSION          = config["Options"]["UE_VERSION"]
EXPORT_TEXTURES     = config["Options"]["EXPORT_TEXTURES"]
TEXTURE_FORMAT      = config["Options"]["TEXTURE_FORMAT"]
UPSCALE             = config["Options"]["UPSCALE"]
MODE                = config["Options"]["MODE"]
PACK_FILES          = config["Options"]["PACK_FILES"]
OVERWRITE           = config["Options"]["OVERWRITE"]

#Define Colors
GREEN_RGB           = (0, 255, 0, 1)
WHITE_RGB           = (1, 1, 1, 1)
BLACK_RGB           = (0, 0, 0, 0,)
RED_RGB             = (255, 0, 0, 1)
YELLOW_RGB          = (255, 255, 0, 1)

#Enable nodes
bpy.context.scene.use_nodes = True

#Create node groups
#def create_hair_shader_node(context, operator, group_name)

#Body Shader Node (Not sure if needed)
def create_body_shader_node(context, operator, group_name) :
    body_shader_node = bpy.data.node_groups.new(group_name, "CompositorNodeTree")
    #Group Input
    group_in = body_shader_node.nodes.new("NodeGroupInput")
    body_shader_node.inputs.new("NodeSocketImage","Diffuse")
    body_shader_node.inputs.new("NodeSocketImage","MRS")
    body_shader_node.inputs.new("NodeSocketImage","Normal")
    #Group Output
    group_out = body_shader_node.nodes.new("NodeGroupOutput")
    body_shader_node.Outputs.new("NodeSocketColor","Output")
    #Nodes
    seperate_rgb    = body_shader_node.nodes.new(type= "CompositorNodeSeperateRGB")
    seperate_rgb    = body_shader_node.nodes.new(type= "CompositorNodeSeperateRGB")
    invert          = body_shader_node.nodes.new(type= "CompositorNodeInvert")
    combine_rgb     = body_shader_node.nodes.new(type= "CompositorNodeCombineRGB")
    normal_map      = body_shader_node.nodes.new(type= "CompositorNodeNormalMap")
    principled_bdsf = body_shader_node.nodes.new(type= "CompositorNodePrincipledBDSF")
    shader_to_rgb   = body_shader_node.nodes.new(type= "CompositorNodeShaderToRGB")         #Due to this only eevee is supported
    #Connections
    Link = body_shader_node.links.new
    Link(group_in.outputs[0], principled_bdsf.inputs[1])
    Link(group_in.outputs[1], seperate_rgb.inputs[0])
    Link(seperate_rgb.outputs[0], principled_bdsf.inputs[4])
    Link(seperate_rgb.outputs[1], principled_bdsf.inputs[5])
    Link(seperate_rgb.outputs[2], principled_bdsf.inputs[7])
    Link(group_in.outputs[2], seperate_rgb.inputs[0])
    Link(seperate_rgb.outputs[0], combine_rgb.inputs[0])
    Link(seperate_rgb.outputs[1], invert.inputs[1])
    Link(seperate_rgb.outputs[2], combine_rgb.inputs[2])
    Link(combine_rgb.outputs[0], normal_map.inputs[1])
    Link(normal_map.outputs[0], principled_bdsf.inputs[20])
    Link(principled_bdsf.outputs[0], shader_to_rgb.inputs[0])
    Link(shader_to_rgb.outputs[0], group_out.inputs[0])
    return body_shader_node
custom_node_name = "Body Shader"
my_group = create_body_shader_node(self, context, custom_node_name)
body_shader_node = context.scene.node_tree.nodes.new("CompositorNodeGroup")
body_shader_node.node_tree = bpy.data.node_groups[my_group.name]

#def create_eye_shader_node(context, operator, group_name)