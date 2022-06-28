import configparser
import threading
import logging
import datetime
import os

config = configparser()
config.read("Settings.ini")

MAIN_PATH       = config["Options"]["MAIN_PATH"]
UE_AES          = config["Options"]["UE_AES"]
UE_VERSION      = config["Options"]["UE_VERSION"]
MODE            = config["Options"]["MODE"]
TEXTURE_FORMAT  = config["Options"]["TEXTURE_FORMAT"]
UPSCALE         = config["Options"]["UPSCALE"]
PACK_FILES      = config["Options"]["PACK_FILES"]

GREEN_RGB       = (0, 255, 0, 1)
WHITE_RGB       = (1, 1, 1, 1)
BLACK_RGB       = (0, 0, 0, 0,)
RED_RGB         = (255, 0, 0, 1)
YELLOW_RGB      = (255, 255, 0, 1)

EXPORT_FOLDER   = os.path
TEMP_FOLDER     = os.path

def log():
    filename = datetime.now().strftime("%m-%d-%y-%H-%M-%S.log")
    

def exportmodels():

def exporttextures():

def initializeblendermain():