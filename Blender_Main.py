import bpy
import ConfigParser
import logging
import os
import os.path #For Auto Locate
import json #I pray to god that I wont have to use this

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

#Create node groups @Note: Due to the use of the Shader To RGB Node eevee is only supported 
#Hair Shader Node
def create_hair_shader_node(context, operator, group_name) :
    hair_shader_node = bpy.data.node_groups.new(group_name, "CompositorNodeTree")
    #Group Input
    group_in = hair_shader_node.nodes.new("NodeGroupInput")
    hair_shader_node.inputs.new("NodeSocketImage","Diffuse")
    hair_shader_node.inputs.new("NodeSocketImage","MRS")
    hair_shader_node.inputs.new("NodeSocketImage","Normal")
    #Group Output
    group_out = hair_shader_node.nodes.new("NodeGroupOutput")
    hair_shader_node.Outputs.new("NodeSocketColor","Output")
    #Nodes
    seperate_rgb    = hair_shader_node.nodes.new(type= "CompositorNodeSeperateRGB")
    greater_than    = hair_shader_node.nodes.new(type= "CompositorNodeGreaterThan")
    greater_than2   = hair_shader_node.nodes.new(type= "CompositorNodeGreaterThan")
    mix_rgb         = hair_shader_node.nodes.new(type= "CompositorNodeMixRGB")
    mix_rgb2        = hair_shader_node.nodes.new(type= "CompositorNodeMixRGB")
    color_ramp      = hair_shader_node.nodes.new(type= "CompositorNodeColorRamp")
    color_ramp2     = hair_shader_node.nodes.new(type= "CompositorNodeColorRamp")
    rgb_curves      = hair_shader_node.nodes.new(type= "CompositorNodeRGBCurves")
    normal_map      = hair_shader_node.nodes.new(type= "CompositorNodeNormalMap")
    bump            = hair_shader_node.nodes.new(type= "CompositorNodeBump")
    mix_rgb3        = hair_shader_node.nodes.new(type= "CompositorNodeMixRGB")
    seperate_rgb    = hair_shader_node.nodes.new(type= "CompositorNodeSeperateRGB")
    multiply        = hair_shader_node.nodes.new(type= "CompositorNodeMultiply")
    multiply2       = hair_shader_node.nodes.new(type= "CompositorNodeMultiply")
    principled_bdsf = hair_shader_node.nodes.new(type= "CompositorNodePrincipledBDSF")
    shader_to_rgb   = hair_shader_node.nodes.new(type= "CompositorNodeShaderToRGB")
    #Connections
    Link = hair_shader_node.links.new
    Link(group_in.outputs[0], multiply2.inputs[1])
    Link(multiply2.outputs[0], principled_bdsf.inputs[0])
    Link(multiply2.outputs[0], principled_bdsf.inputs[3])
    Link(group_in.outputs[1], seperate_rgb.inputs[0])
    Link(seperate_rgb.outputs[0], color_ramp.inputs[0])
    Link(color_ramp.outputs[0], multiply.inputs[2])
    Link(greater_than.outputs[0], mix_rgb.inputs[0])
    Link(mix_rgb.outputs[0], principled_bdsf.inputs[6])
    Link(seperate_rgb.outputs[1], mix_rgb.inputs[2])
    Link(greater_than2.outputs[0], mix_rgb2.inputs[0])
    Link(mix_rgb2.outputs[0], principled_bdsf.inputs[9])
    Link(seperate_rgb.outputs[2], mix_rgb2.inputs[2])
    Link(group_in.outputs[2], seperate_rgb2.inputs[0])
    Link(seperate_rgb2.outputs[2], color_ramp2.inputs[1])
    Link(color_ramp2.outputs[0], multiply.inputs[1])
    Link(multiply.outputs[0], multiply2.inputs[2])
    Link(group_in.outputs[2], rgb_curves.inputs[1])
    Link(rgb_curves.outputs[0], normal_map.inputs[1])
    Link(normal_map.outputs[0], bump.inputs[3])
    Link(bump.outputs[0], mix_rgb3.inputs[1])
    Link(normal_map.outputs[0], mix_rgb3.inputs[2])
    Link(mix_rgb3.outputs[0], principled_bdsf.inputs[22])
    Link(principled_bdsf.outputs[0], shader_to_rgb.inputs[0])
    Link(shader_to_rgb.outputs[0], group_out.inputs[0])
    return hair_shader_node
custom_node_name = "Hair Shader"
my_group = create_hair_shader_node(self, context, custom_node_name)
hair_shader_node = context.scene.node_tree.nodes.new("CompositorNodeGroup")
hair_shader_node.node_tree = bpy.data.node_groups[my_group.name]

#Body Shader Node
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
    seperate_rgb2   = body_shader_node.nodes.new(type= "CompositorNodeSeperateRGB")
    invert          = body_shader_node.nodes.new(type= "CompositorNodeInvert")
    combine_rgb     = body_shader_node.nodes.new(type= "CompositorNodeCombineRGB")
    normal_map      = body_shader_node.nodes.new(type= "CompositorNodeNormalMap")
    principled_bdsf = body_shader_node.nodes.new(type= "CompositorNodePrincipledBDSF")
    shader_to_rgb   = body_shader_node.nodes.new(type= "CompositorNodeShaderToRGB")
    #Connections
    Link = body_shader_node.links.new
    Link(group_in.outputs[0], principled_bdsf.inputs[1])
    Link(group_in.outputs[1], seperate_rgb.inputs[0])
    Link(seperate_rgb.outputs[0], principled_bdsf.inputs[4])
    Link(seperate_rgb.outputs[1], principled_bdsf.inputs[5])
    Link(seperate_rgb.outputs[2], principled_bdsf.inputs[7])
    Link(group_in.outputs[2], seperate_rgb2.inputs[0])
    Link(seperate_rgb2.outputs[0], combine_rgb.inputs[0])
    Link(seperate_rgb2.outputs[1], invert.inputs[1])
    Link(seperate_rgb2.outputs[2], combine_rgb.inputs[2])
    Link(combine_rgb.outputs[0], normal_map.inputs[1])
    Link(normal_map.outputs[0], principled_bdsf.inputs[20])
    Link(principled_bdsf.outputs[0], shader_to_rgb.inputs[0])
    Link(shader_to_rgb.outputs[0], group_out.inputs[0])
    return body_shader_node
custom_node_name = "Body Shader"
my_group = create_body_shader_node(self, context, custom_node_name)
body_shader_node = context.scene.node_tree.nodes.new("CompositorNodeGroup")
body_shader_node.node_tree = bpy.data.node_groups[my_group.name]

#Eye Shader Node
def create_eye_shader_node(context, operator, group_name) :
    eye_shader_node = bpy.data.node_groups.new(group_name, "CompositorNodeTree")
    #Group Input
    group_in = eye_shader_node.nodes.new("NodeGroupInput")
    eye_shader_node.inputs.new("NodeSocketImage","Diffuse")
    eye_shader_node.inputs.new("NodeSocketFactor","Alpha")
    #Group Output
    group_out = eye_shader_node.nodes.new("NodeGroupOutput")
    eye_shader_node.Outputs.new("NodeSocketColor", "Output")
    #Nodes
    diffuse_bdsf      = eye_shader_node.nodes.new(type= "CompositorNodeDiffuseBDSF")
    transparent_bdsf  = eye_shader_node.nodes.new(type= "CompositorNodeTransparentBDSF")
    mix_shader        = eye_shader_node.nodes.new(type= "CompositorNodeMixShader")
    shader_to_rgb     = eye_shader_node.nodes.new(type= "CompositorNodeShaderToRGB")
    #Connections
    Link = eye_shader_node.links.new
    Link(group_in.outputs[0], diffuse_bdsf.inputs[0])
    Link(group_in.outputs[1], mix_shader.inputs[0])
    Link(transparent_bdsf.outputs[1], mix_shader.inputs[1])
    Link(diffuse_bdsf.outputs[0], mix_shader.inputs[2])
    Link(mix_shader.outputs[0], shader_to_rgb.inputs[0])
    Link(shader_to_rgb.outputs[0], group_out.inputs[0])
    return eye_shader_node
custom_node_name = "Eye Shader"
my_group = create_eye_shader_node(self, context, custom_node_name)
eye_shader_node = context.scene.node_tree.nodes.new("CompositorNodeGroup")
eye_shader_node.node_tree = bpy.data.node_groups[my_group.name]

#VFX Shader Node TODO

#Upscale TODO

#Auto Path Location
def auto_locate_path() :                                    #Fuck me this is hard kill me now
    drive_letter = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    if os.path.exists(os.path.join(drive_letter + ":/")):
        return auto_locate_path