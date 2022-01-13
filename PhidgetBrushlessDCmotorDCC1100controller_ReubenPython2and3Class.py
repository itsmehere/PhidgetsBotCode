# -*- coding: utf-8 -*-

'''
Reuben Brewer, Ph.D.
reuben.brewer@gmail.com
www.reubotics.com

Apache 2 License
Software Revision D, 11/12/2021

Verified working on: Python 2.7, 3.8 for Windows 8.1, 10 64-bit and Raspberry Pi Buster (no Mac testing yet).
'''

__author__ = 'reuben.brewer'

from LowPassFilter_ReubenPython2and3Class import *

import os, sys, platform
import time, datetime
import math
import collections
import inspect #To enable 'TellWhichFileWereIn'
import threading
import traceback

###############
if sys.version_info[0] < 3:
    from Tkinter import * #Python 2
    import tkFont
    import ttk
else:
    from tkinter import * #Python 3
    import tkinter.font as tkFont #Python 3
    from tkinter import ttk
###############

###############
if sys.version_info[0] < 3:
    import Queue  # Python 2
else:
    import queue as Queue  # Python 3
###############

###############
if sys.version_info[0] < 3:
    from builtins import raw_input as input
else:
    from future.builtins import input as input
############### #"sudo pip3 install future" (Python 3) AND "sudo pip install future" (Python 2)

###########################################################
###########################################################
#To install Phidget22, enter folder "Phidget22Python_1.0.0.20190107\Phidget22Python" and type "python setup.py install"
from Phidget22.PhidgetException import *
from Phidget22.Phidget import *
from Phidget22.Devices.Log import *
from Phidget22.LogLevel import *
from Phidget22.Devices.TemperatureSensor import *
from Phidget22.Devices.BLDCMotor import *
from Phidget22.Devices.MotorPositionController import *
###########################################################
###########################################################

#http://stackoverflow.com/questions/19087515/subclassing-tkinter-to-create-a-custom-widget
class PhidgetBrushlessDCmotorDCC1100controller_ReubenPython2and3Class(Frame): #Subclass the Tkinter Frame

    ##########################################################################################################
    ##########################################################################################################
    def __init__(self, setup_dict):

        print("#################### PhidgetBrushlessDCmotorDCC1100controller_ReubenPython2and3Class __init__ starting. ####################")

        self.EXIT_PROGRAM_FLAG = 0
        self.OBJECT_CREATED_SUCCESSFULLY_FLAG = -1
        self.EnableInternal_MyPrint_Flag = 0

        self.ThisIsFirstTimeEverAttachingFlag = 1
        self.device_connected_flag = 0
        self.MainThread_still_running_flag = 0

        ##########################################
        ##########################################
        if platform.system() == "Linux":

            if "raspberrypi" in platform.uname(): #os.uname() doesn't work in windows
                self.my_platform = "pi"
            else:
                self.my_platform = "linux"

        elif platform.system() == "Windows":
            self.my_platform = "windows"

        elif platform.system() == "Darwin":
            self.my_platform = "mac"

        else:
            self.my_platform = "other"

        print("The OS platform is: " + self.my_platform)
        ##########################################
        ##########################################

        ##########################################
        ##########################################
        if "GUIparametersDict" in setup_dict:
            self.GUIparametersDict = setup_dict["GUIparametersDict"]

            ##########################################
            if "USE_GUI_FLAG" in self.GUIparametersDict:
                self.USE_GUI_FLAG = self.PassThrough0and1values_ExitProgramOtherwise("USE_GUI_FLAG", self.GUIparametersDict["USE_GUI_FLAG"])
            else:
                self.USE_GUI_FLAG = 0

            print("USE_GUI_FLAG = " + str(self.USE_GUI_FLAG))
            ##########################################

            ##########################################
            if "root" in self.GUIparametersDict:
                self.root = self.GUIparametersDict["root"]
                self.RootIsOwnedExternallyFlag = 1
            else:
                self.root = None
                self.RootIsOwnedExternallyFlag = 0

            print("RootIsOwnedExternallyFlag = " + str(self.RootIsOwnedExternallyFlag))
            ##########################################

            ##########################################
            if "GUI_RootAfterCallbackInterval_Milliseconds" in self.GUIparametersDict:
                self.GUI_RootAfterCallbackInterval_Milliseconds = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("GUI_RootAfterCallbackInterval_Milliseconds", self.GUIparametersDict["GUI_RootAfterCallbackInterval_Milliseconds"], 0.0, 1000.0))
            else:
                self.GUI_RootAfterCallbackInterval_Milliseconds = 30

            print("GUI_RootAfterCallbackInterval_Milliseconds = " + str(self.GUI_RootAfterCallbackInterval_Milliseconds))
            ##########################################

            ##########################################
            if "EnableInternal_MyPrint_Flag" in self.GUIparametersDict:
                self.EnableInternal_MyPrint_Flag = self.PassThrough0and1values_ExitProgramOtherwise("EnableInternal_MyPrint_Flag", self.GUIparametersDict["EnableInternal_MyPrint_Flag"])
            else:
                self.EnableInternal_MyPrint_Flag = 0

            print("EnableInternal_MyPrint_Flag: " + str(self.EnableInternal_MyPrint_Flag))
            ##########################################

            ##########################################
            if "PrintToConsoleFlag" in self.GUIparametersDict:
                self.PrintToConsoleFlag = self.PassThrough0and1values_ExitProgramOtherwise("PrintToConsoleFlag", self.GUIparametersDict["PrintToConsoleFlag"])
            else:
                self.PrintToConsoleFlag = 1

            print("PrintToConsoleFlag: " + str(self.PrintToConsoleFlag))
            ##########################################

            ##########################################
            if "NumberOfPrintLines" in self.GUIparametersDict:
                self.NumberOfPrintLines = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("NumberOfPrintLines", self.GUIparametersDict["NumberOfPrintLines"], 0.0, 50.0))
            else:
                self.NumberOfPrintLines = 10

            print("NumberOfPrintLines = " + str(self.NumberOfPrintLines))
            ##########################################

            ##########################################
            if "UseBorderAroundThisGuiObjectFlag" in self.GUIparametersDict:
                self.UseBorderAroundThisGuiObjectFlag = self.PassThrough0and1values_ExitProgramOtherwise("UseBorderAroundThisGuiObjectFlag", self.GUIparametersDict["UseBorderAroundThisGuiObjectFlag"])
            else:
                self.UseBorderAroundThisGuiObjectFlag = 0

            print("UseBorderAroundThisGuiObjectFlag: " + str(self.UseBorderAroundThisGuiObjectFlag))
            ##########################################

            ##########################################
            if "GUI_ROW" in self.GUIparametersDict:
                self.GUI_ROW = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("GUI_ROW", self.GUIparametersDict["GUI_ROW"], 0.0, 1000.0))
            else:
                self.GUI_ROW = 0

            print("GUI_ROW = " + str(self.GUI_ROW))
            ##########################################

            ##########################################
            if "GUI_COLUMN" in self.GUIparametersDict:
                self.GUI_COLUMN = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("GUI_COLUMN", self.GUIparametersDict["GUI_COLUMN"], 0.0, 1000.0))
            else:
                self.GUI_COLUMN = 0

            print("GUI_COLUMN = " + str(self.GUI_COLUMN))
            ##########################################

            ##########################################
            if "GUI_PADX" in self.GUIparametersDict:
                self.GUI_PADX = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("GUI_PADX", self.GUIparametersDict["GUI_PADX"], 0.0, 1000.0))
            else:
                self.GUI_PADX = 0

            print("GUI_PADX = " + str(self.GUI_PADX))
            ##########################################

            ##########################################
            if "GUI_PADY" in self.GUIparametersDict:
                self.GUI_PADY = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("GUI_PADY", self.GUIparametersDict["GUI_PADY"], 0.0, 1000.0))
            else:
                self.GUI_PADY = 0

            print("GUI_PADY = " + str(self.GUI_PADY))
            ##########################################

            ##########################################
            if "GUI_ROWSPAN" in self.GUIparametersDict:
                self.GUI_ROWSPAN = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("GUI_ROWSPAN", self.GUIparametersDict["GUI_ROWSPAN"], 0.0, 1000.0))
            else:
                self.GUI_ROWSPAN = 0

            print("GUI_ROWSPAN = " + str(self.GUI_ROWSPAN))
            ##########################################

            ##########################################
            if "GUI_COLUMNSPAN" in self.GUIparametersDict:
                self.GUI_COLUMNSPAN = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("GUI_COLUMNSPAN", self.GUIparametersDict["GUI_COLUMNSPAN"], 0.0, 1000.0))
            else:
                self.GUI_COLUMNSPAN = 0

            print("GUI_COLUMNSPAN = " + str(self.GUI_COLUMNSPAN))
            ##########################################

        else:
            self.GUIparametersDict = dict()
            self.USE_GUI_FLAG = 0
            print("No GUIparametersDict present, setting USE_GUI_FLAG = " + str(self.USE_GUI_FLAG))

        print("GUIparametersDict = " + str(self.GUIparametersDict))
        ##########################################
        ##########################################

        ##########################################
        if "UsePhidgetsLoggingInternalToThisClassObjectFlag" in setup_dict:
            self.UsePhidgetsLoggingInternalToThisClassObjectFlag = self.PassThrough0and1values_ExitProgramOtherwise("UsePhidgetsLoggingInternalToThisClassObjectFlag", setup_dict["UsePhidgetsLoggingInternalToThisClassObjectFlag"])
        else:
            self.UsePhidgetsLoggingInternalToThisClassObjectFlag = 1

        print("UsePhidgetsLoggingInternalToThisClassObjectFlag: " + str(self.UsePhidgetsLoggingInternalToThisClassObjectFlag))
        ##########################################

        ##########################################
        if "WaitForAttached_TimeoutDuration_Milliseconds" in setup_dict:
            self.WaitForAttached_TimeoutDuration_Milliseconds = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("WaitForAttached_TimeoutDuration_Milliseconds", setup_dict["WaitForAttached_TimeoutDuration_Milliseconds"], 0.0, 60000.0))

        else:
            self.WaitForAttached_TimeoutDuration_Milliseconds = 5000

        print("WaitForAttached_TimeoutDuration_Milliseconds: " + str(self.WaitForAttached_TimeoutDuration_Milliseconds))
        ##########################################

        #########################################################
        if "VINT_DesiredSerialNumber" in setup_dict:
            try:
                self.VINT_DesiredSerialNumber = int(setup_dict["VINT_DesiredSerialNumber"])
            except:
                print("PhidgetBrushlessDCmotorDCC1100controller_ReubenPython2and3Class __init__ ERROR:: VINT_DesiredSerialNumber invalid.")
        else:
            self.OBJECT_CREATED_SUCCESSFULLY_FLAG = 0
            print("PhidgetBrushlessDCmotorDCC1100controller_ReubenPython2and3Class __init__ ERROR: Must initialize object with 'VINT_DesiredSerialNumber' argument.")
            return

        print("VINT_DesiredSerialNumber: " + str(self.VINT_DesiredSerialNumber))
        #########################################################

        #########################################################
        if "VINT_DesiredPortNumber" in setup_dict:
            try:
                self.VINT_DesiredPortNumber = int(setup_dict["VINT_DesiredPortNumber"])
            except:
                print("PhidgetBrushlessDCmotorDCC1100controller_ReubenPython2and3Class __init__ ERROR:: VINT_DesiredPortNumber invalid.")
        else:
            self.OBJECT_CREATED_SUCCESSFULLY_FLAG = 0
            print("PhidgetBrushlessDCmotorDCC1100controller_ReubenPython2and3Class __init__ ERROR: Must initialize object with 'VINT_DesiredPortNumber' argument.")
            return

        print("VINT_DesiredPortNumber: " + str(self.VINT_DesiredPortNumber))
        #########################################################

        #########################################################
        if "DesiredDeviceID" in setup_dict:
            try:
                self.DesiredDeviceID = int(setup_dict["DesiredDeviceID"])
            except:
                print("PhidgetBrushlessDCmotorDCC1100controller_ReubenPython2and3Class __init__ ERROR: DesiredDeviceID invalid.")
        else:
            self.OBJECT_CREATED_SUCCESSFULLY_FLAG = 0
            print("PhidgetBrushlessDCmotorDCC1100controller_ReubenPython2and3Class __init__ ERROR: Must initialize object with 'DesiredDeviceID' argument.")
            return

        print("DesiredDeviceID: " + str(self.DesiredDeviceID))
        #########################################################

        #########################################################
        if "NameToDisplay_UserSet" in setup_dict:
            self.NameToDisplay_UserSet = str(setup_dict["NameToDisplay_UserSet"])
        else:
            self.NameToDisplay_UserSet = ""

        print("NameToDisplay_UserSet: " + str(self.NameToDisplay_UserSet))
        #########################################################

        ##########################################
        if "MainThread_TimeToSleepEachLoop" in setup_dict:
            self.MainThread_TimeToSleepEachLoop = self.PassThroughFloatValuesInRange_ExitProgramOtherwise("MainThread_TimeToSleepEachLoop", setup_dict["MainThread_TimeToSleepEachLoop"], 0.001, 100000)

        else:
            self.MainThread_TimeToSleepEachLoop = 0.005

        print("MainThread_TimeToSleepEachLoop: " + str(self.MainThread_TimeToSleepEachLoop))
        ##########################################

        #########################################################
        if "ENABLE_GETS_MAINTHREAD" in setup_dict:
            self.ENABLE_GETS_MAINTHREAD = int(setup_dict["ENABLE_GETS_MAINTHREAD"])

            if self.ENABLE_GETS_MAINTHREAD != 0 and self.ENABLE_GETS_MAINTHREAD != 1:
                self.OBJECT_CREATED_SUCCESSFULLY_FLAG = 0
                print("PhidgetBrushlessDCmotorDCC1100controller_ReubenPython2and3Class __init__ ERROR: ENABLE_GETS_MAINTHREAD in setup dict must be 0 or 1.")
                return
        else:
            self.ENABLE_GETS_MAINTHREAD = 0

        print("ENABLE_GETS_MAINTHREAD: " + str(self.ENABLE_GETS_MAINTHREAD))
        #########################################################

        #########################################################
        if "ControlMode" in setup_dict:
            self.ControlMode = str(setup_dict["ControlMode"]).lower()

            if self.ControlMode != "position" and self.ControlMode != "velocity":
                self.OBJECT_CREATED_SUCCESSFULLY_FLAG = 0
                print("PhidgetBrushlessDCmotorDCC1100controller_ReubenPython2and3Class __init__ ERROR: ControlMode in setup dict must be 'position' or 'velocity'.")
                return
        else:
            self.ControlMode = "velocity"

        print("ControlMode: " + self.ControlMode)
        #########################################################

        ##########################################
        if "UpdateDeltaT_ms" in setup_dict:
            if self.ControlMode == "position":
                self.UpdateDeltaT_ms = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("UpdateDeltaT_ms", setup_dict["UpdateDeltaT_ms"], 20.0, 60000.0))

            elif self.ControlMode == "velocity":
                self.UpdateDeltaT_ms = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("UpdateDeltaT_ms", setup_dict["UpdateDeltaT_ms"], 100.0, 60000.0))

        else:
            if self.ControlMode == "position":
                self.UpdateDeltaT_ms = int(20.0)
            elif self.ControlMode == "velocity":
                self.UpdateDeltaT_ms = int(100.0)

        print("UpdateDeltaT_ms: " + str(self.UpdateDeltaT_ms))
        ##########################################

        ##########################################
        if "FailsafeTime_Milliseconds" in setup_dict:
                self.FailsafeTime_Milliseconds = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("FailsafeTime_Milliseconds", setup_dict["FailsafeTime_Milliseconds"], 500.0, 30000.0))
        else:
            if self.ControlMode == "position":
                self.FailsafeTime_Milliseconds = int(1000.0)

        print("FailsafeTime_Milliseconds: " + str(self.FailsafeTime_Milliseconds))
        ##########################################

        #########################################################
        if "PositionMinLimit_PhidgetsUnits_UserSet" in setup_dict:
            self.PositionMinLimit_PhidgetsUnits_UserSet = setup_dict["PositionMinLimit_PhidgetsUnits_UserSet"]
        else:
            self.PositionMinLimit_PhidgetsUnits_UserSet = -7.24637681159e+12

        print("PositionMinLimit_PhidgetsUnits_UserSet: " + str(self.PositionMinLimit_PhidgetsUnits_UserSet))
        #########################################################

        #########################################################
        if "PositionMaxLimit_PhidgetsUnits_UserSet" in setup_dict:
            self.PositionMaxLimit_PhidgetsUnits_UserSet = setup_dict["PositionMaxLimit_PhidgetsUnits_UserSet"]
        else:
            self.PositionMaxLimit_PhidgetsUnits_UserSet = 7.24637681159e+12

        print("PositionMaxLimit_PhidgetsUnits_UserSet: " + str(self.PositionMaxLimit_PhidgetsUnits_UserSet))
        #########################################################

        #########################################################
        if self.PositionMaxLimit_PhidgetsUnits_UserSet < self.PositionMinLimit_PhidgetsUnits_UserSet:
            print("PhidgetBrushlessDCmotorDCC1100controller_ReubenPython2and3Class __init__ ERROR: PositionMinLimit_PhidgetsUnits_UserSet must be smaller than PositionMaxLimit_PhidgetsUnits_UserSet!")
            return
        #########################################################

        #########################################################
        if "VelocityMinLimit_PhidgetsUnits_UserSet" in setup_dict:

            if self.ControlMode == "position":
                if setup_dict["VelocityMinLimit_PhidgetsUnits_UserSet"] > 0:
                    self.VelocityMinLimit_PhidgetsUnits_UserSet = self.PassThroughFloatValuesInRange_ExitProgramOtherwise("VelocityMinLimit_PhidgetsUnits_UserSet", setup_dict["VelocityMinLimit_PhidgetsUnits_UserSet"], 0.0, 10000.0)
                else:
                    self.VelocityMinLimit_PhidgetsUnits_UserSet = self.PassThroughFloatValuesInRange_ExitProgramOtherwise("VelocityMinLimit_PhidgetsUnits_UserSet", setup_dict["VelocityMinLimit_PhidgetsUnits_UserSet"], -10000.0, 0.0)

            elif self.ControlMode == "velocity":
                if setup_dict["VelocityMinLimit_PhidgetsUnits_UserSet"] > 0:
                    self.VelocityMinLimit_PhidgetsUnits_UserSet = self.PassThroughFloatValuesInRange_ExitProgramOtherwise("VelocityMinLimit_PhidgetsUnits_UserSet", setup_dict["VelocityMinLimit_PhidgetsUnits_UserSet"], 0.0, 1.0)
                else:
                    self.VelocityMinLimit_PhidgetsUnits_UserSet = self.PassThroughFloatValuesInRange_ExitProgramOtherwise("VelocityMinLimit_PhidgetsUnits_UserSet", setup_dict["VelocityMinLimit_PhidgetsUnits_UserSet"], -1.0, 0.0)

        else:
            if self.ControlMode == "position":
                self.VelocityMinLimit_PhidgetsUnits_UserSet = -10000.0

            elif self.ControlMode == "velocity":
                self.VelocityMinLimit_PhidgetsUnits_UserSet = -1.0

        print("VelocityMinLimit_PhidgetsUnits_UserSet: " + str(self.VelocityMinLimit_PhidgetsUnits_UserSet))
        #########################################################

        #########################################################
        if "VelocityMaxLimit_PhidgetsUnits_UserSet" in setup_dict:

            if self.ControlMode == "position":
                if setup_dict["VelocityMaxLimit_PhidgetsUnits_UserSet"] > 0:
                    self.VelocityMaxLimit_PhidgetsUnits_UserSet = self.PassThroughFloatValuesInRange_ExitProgramOtherwise("VelocityMaxLimit_PhidgetsUnits_UserSet", setup_dict["VelocityMaxLimit_PhidgetsUnits_UserSet"], 0.0, 10000.0)
                else:
                    self.VelocityMaxLimit_PhidgetsUnits_UserSet = self.PassThroughFloatValuesInRange_ExitProgramOtherwise("VelocityMaxLimit_PhidgetsUnits_UserSet", setup_dict["VelocityMaxLimit_PhidgetsUnits_UserSet"], -10000.0, 0.0)

            elif self.ControlMode == "velocity":
                if setup_dict["VelocityMaxLimit_PhidgetsUnits_UserSet"] > 0:
                    self.VelocityMaxLimit_PhidgetsUnits_UserSet = self.PassThroughFloatValuesInRange_ExitProgramOtherwise("VelocityMaxLimit_PhidgetsUnits_UserSet", setup_dict["VelocityMaxLimit_PhidgetsUnits_UserSet"], 0.0, 1.0)
                else:
                    self.VelocityMaxLimit_PhidgetsUnits_UserSet = self.PassThroughFloatValuesInRange_ExitProgramOtherwise("VelocityMaxLimit_PhidgetsUnits_UserSet", setup_dict["VelocityMaxLimit_PhidgetsUnits_UserSet"], -1.0, 0.0)

        else:
            if self.ControlMode == "position":
                self.VelocityMaxLimit_PhidgetsUnits_UserSet = 10000.0

            elif self.ControlMode == "velocity":
                self.VelocityMaxLimit_PhidgetsUnits_UserSet = 1.0

        print("VelocityMaxLimit_PhidgetsUnits_UserSet: " + str(self.VelocityMaxLimit_PhidgetsUnits_UserSet))
        #########################################################

        #########################################################
        if self.VelocityMaxLimit_PhidgetsUnits_UserSet < self.VelocityMinLimit_PhidgetsUnits_UserSet:
            print("PhidgetBrushlessDCmotorDCC1100controller_ReubenPython2and3Class __init__ ERROR: VelocityMinLimit_PhidgetsUnits_UserSet must be smaller than VelocityMaxLimit_PhidgetsUnits_UserSet!")
            return
        #########################################################

        #########################################################
        if "VelocityStallLimit_PhidgetsUnits_UserSet" in setup_dict:

            if self.ControlMode == "position":
                self.VelocityStallLimit_PhidgetsUnits_UserSet = self.PassThroughFloatValuesInRange_ExitProgramOtherwise("VelocityStallLimit_PhidgetsUnits_UserSet", setup_dict["VelocityStallLimit_PhidgetsUnits_UserSet"], 0.0, 2000.0)

            elif self.ControlMode == "velocity":
                self.VelocityStallLimit_PhidgetsUnits_UserSet = self.PassThroughFloatValuesInRange_ExitProgramOtherwise("VelocityStallLimit_PhidgetsUnits_UserSet", setup_dict["VelocityStallLimit_PhidgetsUnits_UserSet"], 0.0, 2000.0)

        else:
            if self.ControlMode == "position":
                self.VelocityStallLimit_PhidgetsUnits_UserSet = 2000.0

            elif self.ControlMode == "velocity":
                self.VelocityStallLimit_PhidgetsUnits_UserSet = 2000.0

        print("VelocityStallLimit_PhidgetsUnits_UserSet: " + str(self.VelocityStallLimit_PhidgetsUnits_UserSet))
        #########################################################

        #########################################################
        if "BrakingStrengthLimit_VelControl_Percent_UserSet" in setup_dict:
            self.BrakingStrengthLimit_VelControl_Percent_UserSet = float(setup_dict["BrakingStrengthLimit_VelControl_Percent_UserSet"])

            if self.BrakingStrengthLimit_VelControl_Percent_UserSet < 0.0 or self.BrakingStrengthLimit_VelControl_Percent_UserSet > 100.0:
                self.OBJECT_CREATED_SUCCESSFULLY_FLAG = 0
                print("ERROR: BrakingStrengthLimit_VelControl_Percent_UserSet must be between 0.0 an 100.0 percent.")
                return

        else:
            self.BrakingStrengthLimit_VelControl_Percent_UserSet = 50.0

        print("BrakingStrengthLimit_VelControl_Percent_UserSet: " + str(self.BrakingStrengthLimit_VelControl_Percent_UserSet))
        #########################################################

        #########################################################
        if "DeadBand_PosControl_PhidgetsUnits_UserSet" in setup_dict:
            self.DeadBand_PosControl_PhidgetsUnits_UserSet = float(setup_dict["DeadBand_PosControl_PhidgetsUnits_UserSet"])

            if self.DeadBand_PosControl_PhidgetsUnits_UserSet < 0.0:
                self.OBJECT_CREATED_SUCCESSFULLY_FLAG = 0
                print("ERROR: self.DeadBand_PosControl_PhidgetsUnits_UserSet must be grater than 0.")
                return

        else:
            self.DeadBand_PosControl_PhidgetsUnits_UserSet = 0.0

        print("DeadBand_PosControl_PhidgetsUnits_UserSet: " + str(self.DeadBand_PosControl_PhidgetsUnits_UserSet))
        #########################################################

        #########################################################
        if "AccelerationMaxLimit_PhidgetsUnits_UserSet" in setup_dict:

            if self.ControlMode == "position":
                self.AccelerationMaxLimit_PhidgetsUnits_UserSet = self.PassThroughFloatValuesInRange_ExitProgramOtherwise("AccelerationMaxLimit_PhidgetsUnits_UserSet", setup_dict["AccelerationMaxLimit_PhidgetsUnits_UserSet"], 0.1, 100000.0)

            elif self.ControlMode == "velocity":
                self.AccelerationMaxLimit_PhidgetsUnits_UserSet = self.PassThroughFloatValuesInRange_ExitProgramOtherwise("AccelerationMaxLimit_PhidgetsUnits_UserSet", setup_dict["AccelerationMaxLimit_PhidgetsUnits_UserSet"], 0.1, 100.0)

        else:
            if self.ControlMode == "position":
                self.AccelerationMaxLimit_PhidgetsUnits_UserSet = 50000.0

            elif self.ControlMode == "velocity":
                self.AccelerationMaxLimit_PhidgetsUnits_UserSet = 50.0

        print("AccelerationMaxLimit_PhidgetsUnits_UserSet: " + str(self.AccelerationMaxLimit_PhidgetsUnits_UserSet))
        #########################################################

        #########################################################
        if "Kp_PosControl_Gain_UserSet" in setup_dict:
            self.Kp_PosControl_Gain_UserSet = float(setup_dict["Kp_PosControl_Gain_UserSet"])
        else:
            self.Kp_PosControl_Gain_UserSet = 20000.0

        print("Kp_PosControl_Gain_UserSet: " + str(self.Kp_PosControl_Gain_UserSet))
        #########################################################

        #########################################################
        if "Ki_PosControl_Gain_UserSet" in setup_dict:
            self.Ki_PosControl_Gain_UserSet = float(setup_dict["Ki_PosControl_Gain_UserSet"])
        else:
            self.Ki_PosControl_Gain_UserSet = 2.0

        print("Ki_PosControl_Gain_UserSet: " + str(self.Ki_PosControl_Gain_UserSet))
        #########################################################
        
        #########################################################
        if "Kd_PosControl_Gain_UserSet" in setup_dict:
            self.Kd_PosControl_Gain_UserSet = float(setup_dict["Kd_PosControl_Gain_UserSet"])
        else:
            self.Kd_PosControl_Gain_UserSet = 40000.0

        print("Kd_PosControl_Gain_UserSet: " + str(self.Kd_PosControl_Gain_UserSet))
        #########################################################

        #########################################################
        if "RescaleFactor_MultipliesPhidgetsUnits_UserSet" in setup_dict:
            self.RescaleFactor_MultipliesPhidgetsUnits_UserSet = float(setup_dict["RescaleFactor_MultipliesPhidgetsUnits_UserSet"])

            if self.RescaleFactor_MultipliesPhidgetsUnits_UserSet < 0.0:
                self.OBJECT_CREATED_SUCCESSFULLY_FLAG = 0
                print("ERROR: self.RescaleFactor_MultipliesPhidgetsUnits_UserSet must be grater than 0.")
                return

        else:
            self.RescaleFactor_MultipliesPhidgetsUnits_UserSet = 1.0

        print("RescaleFactor_MultipliesPhidgetsUnits_UserSet: " + str(self.RescaleFactor_MultipliesPhidgetsUnits_UserSet))

        print("-----------------------------------------------------------------------"
                "\nFROM PHIDGETS BRUSHLESS DC MOTOR CONTROLLER USER'S GUIDE:"
                "\nInstead of steps, brushless DC motors work in commutations. "
                "\nThe number of commutations per rotation is equal to the number of poles multiplied by the number of phases. "
                "\nSo, if you have an 8-Pole, 3-Phase motor, the motor will have 24 commutations per rotation. "
                "\nFor this motor, to change the target position units from communications to rotations, you would set the rescale factor to 1/24, or 0.0416."
                "\n-----------------------------------------------------------------------")
        #########################################################

        #########################################################
        self.PrintToGui_Label_TextInputHistory_List = [" "]*self.NumberOfPrintLines
        self.PrintToGui_Label_TextInput_Str = ""
        self.GUI_ready_to_be_updated_flag = 0
        #########################################################

        #########################################################
        self.CurrentTime_CalculatedFromMainThread = -11111.0
        self.LastTime_CalculatedFromMainThread = -11111.0
        self.StartingTime_CalculatedFromMainThread = -11111.0
        self.DataStreamingFrequency_CalculatedFromMainThread = -11111.0
        self.DataStreamingDeltaT_CalculatedFromMainThread = -11111.0

        self.CurrentTime_OnPositionChangeCallbackFunction = -11111.0
        self.LastTime_OnPositionChangeCallbackFunction = -11111.0
        self.DataStreamingFrequency_OnPositionChangeCallbackFunction = -11111.0
        self.DataStreamingDeltaT_OnPositionChangeCallbackFunction = -11111.0

        self.LastTime_FailsafeWasReset = -11111.0

        self.DetectedDeviceName = "default"
        self.DetectedDeviceID = "default"
        self.DetectedDeviceVersion = "default"

        self.StopMotor_NeedsToBeChangedFlag = 0

        self.Temperature_DegC_FromDevice = -11111.0

        self.Position_PhidgetsUnits_FromDevice = -11111.0
        self.Position_PhidgetsUnits_FromDevice_Last = -11111.0
        self.Position_PhidgetsUnits_TO_BE_SET = 0.0
        self.Position_PhidgetsUnits_NeedsToBeChangedFlag = 1
        self.Position_PhidgetsUnits_GUI_NeedsToBeChangedFlag = 1

        self.VelocityStall_PhidgetsUnits_FromDevice = -11111.0

        self.Velocity_PhidgetsUnits_FromDevice = -11111.0
        self.Velocity_PhidgetsUnits_TO_BE_SET = 0.0
        self.Velocity_PhidgetsUnits_NeedsToBeChangedFlag = 1
        self.Velocity_PhidgetsUnits_GUI_NeedsToBeChangedFlag = 1

        self.Velocity_PhidgetsUnits_DifferentiatedRaw = -11111.0
        self.Velocity_PhidgetsUnits_DifferentiatedSmoothed = -11111.0

        self.DutyCycle_PhidgetsUnits_FromDevice = -11111

        self.Acceleration_PhidgetsUnits_FromDevice = -11111
        self.Acceleration_PhidgetsUnits_TO_BE_SET = 0.0
        self.Acceleration_PhidgetsUnits_NeedsToBeChangedFlag = 1
        self.Acceleration_PhidgetsUnits_GUI_NeedsToBeChangedFlag = 1

        self.DeadBand_PosControl_PhidgetsUnits_FromDevice = -11111
        self.DeadBand_PosControl_PhidgetsUnits_TO_BE_SET = 0.0
        self.DeadBand_PosControl_PhidgetsUnits_NeedsToBeChangedFlag = 0
        self.DeadBand_PosControl_PhidgetsUnits_GUI_NeedsToBeChangedFlag = 0

        self.EngagedState_PhidgetsUnits_FromDevice = -11111
        self.EngagedState_TO_BE_SET = -1
        self.EngagedState_NeedsToBeChangedFlag = 0

        self.HomeMotorInPlace_NeedsToBeHomedFlag = 0

        self.ACCEPT_EXTERNAL_POSITION_COMMANDS_FLAG = 0
        #########################################################

        #########################################################
        try:
            self.Velocity_LowPassFilter_ReubenPython2and3ClassObject = LowPassFilter_ReubenPython2and3Class(dict([("UseMedianFilterFlag", 0),
                                                                                                            ("UseExponentialSmoothingFilterFlag", 1),
                                                                                                            ("ExponentialSmoothingFilterLambda", 0.2)]))
            time.sleep(0.1)
            self.VELOCITY_LOWPASSFILTER_OPEN_FLAG = self.Velocity_LowPassFilter_ReubenPython2and3ClassObject.OBJECT_CREATED_SUCCESSFULLY_FLAG

            if self.LOWPASSFILTER_OPEN_FLAG != 1:
                print("Failed to open LowPassFilter_ReubenPython2and3ClassObject.")
                self.OBJECT_CREATED_SUCCESSFULLY_FLAG = 0
                return

        except:
            exceptions = sys.exc_info()[0]
            print("LowPassFilter_ReubenPython2and3Class __init__: Exceptions: %s" % exceptions)
        #########################################################

        #########################################################
        self.BrakingStrengthLimit_VelControl_PhidgetsUnits_UserSet = 0.01 * self.BrakingStrengthLimit_VelControl_Percent_UserSet * 1.0 #self.BrakingStrengthStallLimit_PhidgetsUnits_FromDevice
        print("BrakingStrengthLimit_VelControl_PhidgetsUnits_UserSet: " + str(self.BrakingStrengthLimit_VelControl_PhidgetsUnits_UserSet))
        #########################################################

        #########################################################
        try:

            self.TemperatureObject = TemperatureSensor()
            print("Created TemperatureSensor object.")

            if self.ControlMode == "velocity":
                self.BLDCobject = BLDCMotor() #Create a BLDCMotor object for velocity control
                print("Created BLDCMotor object.")

            elif self.ControlMode == "position":
                self.BLDCobject = MotorPositionController() #Create a MotorPositionController object for position control
                print("Created MotorPositionController object.")

        except PhidgetException as e:
            print("Failed to create main motor object, exception:  %i: %s" % (e.code, e.details))
        #########################################################

        #########################################################
        try:
            self.BLDCobject.setDeviceSerialNumber(self.VINT_DesiredSerialNumber)

        except PhidgetException as e:
            print("Failed to call 'setDeviceSerialNumber()', exception:  %i: %s" % (e.code, e.details))
        #########################################################

        #########################################################
        try:
            self.BLDCobject.setHubPort(self.VINT_DesiredPortNumber)

        except PhidgetException as e:
            print("Failed to call 'setHubPort()', exception:  %i: %s" % (e.code, e.details))
        #########################################################

        #########################################################
        try:

            self.TemperatureObject.setOnAttachHandler(self.TemperatureOnAttachCallback)
            self.TemperatureObject.setOnDetachHandler(self.TemperatureOnDetachCallback)
            self.TemperatureObject.setOnTemperatureChangeHandler(self.TemperatureOnChangeCallback)
            self.TemperatureObject.setOnErrorHandler(self.TemperatureOnErrorCallback)

            if self.ControlMode == "velocity":
                self.BLDCobject.setOnAttachHandler(self.BLDConAttachCallback)
                self.BLDCobject.setOnDetachHandler(self.BLDConDetachCallback)
                self.BLDCobject.setOnVelocityUpdateHandler(self.BLDConVelocityUpdateCallback)
                self.BLDCobject.setOnPositionChangeHandler(self.BLDConPositionChangeCallback)
                self.BLDCobject.setOnErrorHandler(self.BLDConErrorCallback)

            elif self.ControlMode == "position":
                self.BLDCobject.setOnAttachHandler(self.BLDConAttachCallback)
                self.BLDCobject.setOnDetachHandler(self.BLDConDetachCallback)
                self.BLDCobject.setOnDutyCycleUpdateHandler(self.BLDConDutyCycleUpdateCallback)
                self.BLDCobject.setOnPositionChangeHandler(self.BLDConPositionChangeCallback)
                self.BLDCobject.setOnErrorHandler(self.BLDConErrorCallback)

            print("Set callback functions.")

            self.BLDCobject.openWaitForAttachment(self.WaitForAttached_TimeoutDuration_Milliseconds)

            self.TemperatureObject.openWaitForAttachment(self.WaitForAttached_TimeoutDuration_Milliseconds)

            self.device_connected_flag = 1
            print("Attached the BLDC object.")

        except PhidgetException as e:
            self.device_connected_flag = 0
            print("Failed to call 'openWaitForAttachment()', exception:  %i: %s" % (e.code, e.details))

            try:
                self.BLDCobject.close()
                print("Closed the BLDC object.")

            except PhidgetException as e:
                print("Failed to call 'close()', exception:  %i: %s" % (e.code, e.details))
        #########################################################


        #########################################################
        #########################################################

        if self.device_connected_flag == 1:

            #########################################################
            if self.UsePhidgetsLoggingInternalToThisClassObjectFlag == 1:
                try:
                    Log.enable(LogLevel.PHIDGET_LOG_INFO, os.getcwd() + "\PhidgetBrushlessDCmotorDCC1100controller_ReubenPython2and3Class_PhidgetLog_INFO.txt")
                    print("PhidgetBrushlessDCmotorDCC1100controller_ReubenPython2and3Class __init__Enabled Phidget Logging.")
                except PhidgetException as e:
                    print("PhidgetBrushlessDCmotorDCC1100controller_ReubenPython2and3Class __init__Failed to enable Phidget Logging, Phidget Exception %i: %s" % (e.code, e.details))
            #########################################################

            #########################################################
            try:
                self.DetectedDeviceName = self.BLDCobject.getDeviceName()
                print("DetectedDeviceName: " + self.DetectedDeviceName)

            except PhidgetException as e:
                print("Failed to call 'getDeviceName', Phidget Exception %i: %s" % (e.code, e.details))
            #########################################################

            #########################################################
            try:
                self.VINT_DetectedSerialNumber = self.BLDCobject.getDeviceSerialNumber()
                print("VINT_DetectedSerialNumber: " + str(self.VINT_DetectedSerialNumber))

            except PhidgetException as e:
                print("Failed to call 'getDeviceSerialNumber', Phidget Exception %i: %s" % (e.code, e.details))
            #########################################################

            #########################################################
            try:
                self.DetectedDeviceID = self.BLDCobject.getDeviceID()
                print("DetectedDeviceID: " + str(self.DetectedDeviceID))

            except PhidgetException as e:
                print("Failed to call 'getDeviceID', Phidget Exception %i: %s" % (e.code, e.details))
            #########################################################

            #########################################################
            try:
                self.DetectedDeviceVersion = self.BLDCobject.getDeviceVersion()
                print("DetectedDeviceVersion: " + str(self.DetectedDeviceVersion))

            except PhidgetException as e:
                print("Failed to call 'getDeviceVersion', Phidget Exception %i: %s" % (e.code, e.details))
            #########################################################

            #########################################################
            try:
                self.DetectedDeviceLibraryVersion = self.BLDCobject.getLibraryVersion()
                print("DetectedDeviceLibraryVersion: " + str(self.DetectedDeviceLibraryVersion))

            except PhidgetException as e:
                print("Failed to call 'getLibraryVersion', Phidget Exception %i: %s" % (e.code, e.details))
            #########################################################

            #########################################################
            if self.VINT_DetectedSerialNumber != self.VINT_DesiredSerialNumber:
                print("The desired VINT_DesiredSerialNumber (" + str(self.VINT_DesiredSerialNumber) + ") does not match the detected serial number (" + str(self.VINT_DetectedSerialNumber) + ").")
                input("Press any key (and enter) to exit.")
                sys.exit()
            #########################################################

            #########################################################
            if self.DetectedDeviceID != self.DesiredDeviceID:
                print("The DesiredDeviceID (" + str(self.DesiredDeviceID) + ") does not match the detected Device ID (" + str(self.DetectedDeviceID) + ").")
                input("Press any key (and enter) to exit.")
                sys.exit()
            #########################################################

            #########################################################
            try:

                ############################
                self.FailsafeTimeMinLimit_PhidgetsUnits_FromDevice = self.BLDCobject.getMinFailsafeTime()
                print("FailsafeTimeMinLimit_PhidgetsUnits_FromDevice: " + str(self.FailsafeTimeMinLimit_PhidgetsUnits_FromDevice))

                self.FailsafeTimeMaxLimit_PhidgetsUnits_FromDevice = self.BLDCobject.getMaxFailsafeTime()
                print("FailsafeTimeMaxLimit_PhidgetsUnits_FromDevice: " + str(self.FailsafeTimeMaxLimit_PhidgetsUnits_FromDevice))
                ############################

                ############################
                self.PositionMinLimit_PhidgetsUnits_FromDevice = self.BLDCobject.getMinPosition()
                print("PositionMinLimit_PhidgetsUnits_FromDevice: " + str(self.PositionMinLimit_PhidgetsUnits_FromDevice))

                self.PositionMaxLimit_PhidgetsUnits_FromDevice = self.BLDCobject.getMaxPosition()
                print("PositionMaxLimit_PhidgetsUnits_FromDevice: " + str(self.PositionMaxLimit_PhidgetsUnits_FromDevice))
                ############################

                ############################
                if self.ControlMode == "velocity":
                    self.VelocityMinLimit_PhidgetsUnits_FromDevice = self.BLDCobject.getMinVelocity()
                    self.VelocityMaxLimit_PhidgetsUnits_FromDevice = self.BLDCobject.getMaxVelocity()

                elif self.ControlMode == "position":
                    self.VelocityMinLimit_PhidgetsUnits_FromDevice = self.BLDCobject.getMinVelocityLimit()
                    self.VelocityMaxLimit_PhidgetsUnits_FromDevice = self.BLDCobject.getMaxVelocityLimit()

                print("VelocityMinLimit_PhidgetsUnits_FromDevice: " + str(self.VelocityMinLimit_PhidgetsUnits_FromDevice))
                print("VelocityMaxLimit_PhidgetsUnits_FromDevice: " + str(self.VelocityMaxLimit_PhidgetsUnits_FromDevice))
                ############################

                ############################
                self.VelocityMinStallLimit_PhidgetsUnits_FromDevice = self.BLDCobject.getMinStallVelocity()
                self.VelocityMaxStallLimit_PhidgetsUnits_FromDevice = self.BLDCobject.getMaxStallVelocity()

                print("VelocityMinStallLimit_PhidgetsUnits_FromDevice: " + str(self.VelocityMinStallLimit_PhidgetsUnits_FromDevice))
                print("VelocityMaxStallLimit_PhidgetsUnits_FromDevice: " + str(self.VelocityMaxStallLimit_PhidgetsUnits_FromDevice))
                ############################

                ############################
                self.AccelerationMinLimit_PhidgetsUnits_FromDevice = self.BLDCobject.getMinAcceleration()
                print("AccelerationMinLimit_PhidgetsUnits_FromDevice: " + str(self.AccelerationMinLimit_PhidgetsUnits_FromDevice))

                self.AccelerationMaxLimit_PhidgetsUnits_FromDevice = self.BLDCobject.getMaxAcceleration()
                print("AccelerationMaxLimit_PhidgetsUnits_FromDevice: " + str(self.AccelerationMaxLimit_PhidgetsUnits_FromDevice))
                ############################

                ############################
                self.DataIntervalMin = self.BLDCobject.getMinDataInterval()
                print("DataIntervalMin: " + str(self.DataIntervalMin))

                self.DataIntervalMax = self.BLDCobject.getMaxDataInterval()
                print("DataIntervalMax: " + str(self.DataIntervalMax))
                ############################

                ############################
                if self.ControlMode == "velocity":
                    self.BrakingStrengthMinLimit_PhidgetsUnits_FromDevice = self.BLDCobject.getMinBrakingStrength()
                    self.BrakingStrengthMaxLimit_PhidgetsUnits_FromDevice = self.BLDCobject.getMaxBrakingStrength()
                    print("BrakingStrengthMinLimit_PhidgetsUnits_FromDevice: " + str(self.BrakingStrengthMinLimit_PhidgetsUnits_FromDevice))
                    print("BrakingStrengthMaxLimit_PhidgetsUnits_FromDevice: " + str(self.BrakingStrengthMaxLimit_PhidgetsUnits_FromDevice))
                ############################

            except PhidgetException as e:
                print("Failed to motor limits, Phidget Exception %i: %s" % (e.code, e.details))
                traceback.print_exc()
                return

            self.MostRecentDataDict = dict([("Position_PhidgetsUnits_FromDevice", self.Position_PhidgetsUnits_FromDevice),
                                            ("Velocity_PhidgetsUnits_FromDevice", self.Velocity_PhidgetsUnits_FromDevice),
                                            ("Velocity_PhidgetsUnits_DifferentiatedRaw", self.Velocity_PhidgetsUnits_DifferentiatedRaw),
                                            ("Velocity_PhidgetsUnits_DifferentiatedSmoothed", self.Velocity_PhidgetsUnits_DifferentiatedSmoothed),
                                            ("DutyCycle_PhidgetsUnits_FromDevice", self.DutyCycle_PhidgetsUnits_FromDevice),
                                            ("Temperature_DegC_FromDevice", self.Temperature_DegC_FromDevice),
                                            ("Time", self.CurrentTime_CalculatedFromMainThread)])

            #########################################################

            ##########################################
            self.MainThread_ThreadingObject = threading.Thread(target=self.MainThread, args=())
            self.MainThread_ThreadingObject.start()
            ##########################################

            ##########################################
            if self.USE_GUI_FLAG == 1:
                self.StartGUI(self.root)
            ##########################################

            self.OBJECT_CREATED_SUCCESSFULLY_FLAG = 1

        else:
            print("---------- Failed to open PhidgetBrushlessDCmotorDCC1100controller_ReubenPython2and3Class for serial number " + str(self.VINT_DesiredSerialNumber) + " ----------")
            self.OBJECT_CREATED_SUCCESSFULLY_FLAG = 0
            return
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def __del__(self):
        pass
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def IsNumber0or1(self, InputNumber):

        if float(InputNumber) == 0.0 or float(InputNumber) == 1:
            return 1
        else:
            return 0
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def PassThrough0and1values_ExitProgramOtherwise(self, InputNameString, InputNumber):

        try:
            InputNumber_ConvertedToFloat = float(InputNumber)
        except:
            exceptions = sys.exc_info()[0]
            print("PassThrough0and1values_ExitProgramOtherwise Error. InputNumber must be a float value, Exceptions: %s" % exceptions)
            input("Press any key to continue")
            sys.exit()

        try:
            if InputNumber_ConvertedToFloat == 0.0 or InputNumber_ConvertedToFloat == 1:
                return InputNumber_ConvertedToFloat
            else:
                input("PassThrough0and1values_ExitProgramOtherwise Error. '" +
                          InputNameString +
                          "' must be 0 or 1 (value was " +
                          str(InputNumber_ConvertedToFloat) +
                          "). Press any key (and enter) to exit.")

                sys.exit()
        except:
            exceptions = sys.exc_info()[0]
            print("PassThrough0and1values_ExitProgramOtherwise Error, Exceptions: %s" % exceptions)
            input("Press any key to continue")
            sys.exit()
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def PassThroughFloatValuesInRange_ExitProgramOtherwise(self, InputNameString, InputNumber, RangeMinValue, RangeMaxValue):
        try:
            InputNumber_ConvertedToFloat = float(InputNumber)
        except:
            exceptions = sys.exc_info()[0]
            print("PassThroughFloatValuesInRange_ExitProgramOtherwise Error. InputNumber must be a float value, Exceptions: %s" % exceptions)
            input("Press any key to continue")
            sys.exit()

        try:
            if InputNumber_ConvertedToFloat >= RangeMinValue and InputNumber_ConvertedToFloat <= RangeMaxValue:
                return InputNumber_ConvertedToFloat
            else:
                input("PassThroughFloatValuesInRange_ExitProgramOtherwise Error. '" +
                          InputNameString +
                          "' must be in the range [" +
                          str(RangeMinValue) +
                          ", " +
                          str(RangeMaxValue) +
                          "] (value was " +
                          str(InputNumber_ConvertedToFloat) + "). Press any key (and enter) to exit.")

                sys.exit()
        except:
            exceptions = sys.exc_info()[0]
            print("PassThroughFloatValuesInRange_ExitProgramOtherwise Error, Exceptions: %s" % exceptions)
            input("Press any key to continue")
            sys.exit()
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def TellWhichFileWereIn(self):

        #We used to use this method, but it gave us the root calling file, not the class calling file
        #absolute_file_path = os.path.dirname(os.path.realpath(sys.argv[0]))
        #filename = absolute_file_path[absolute_file_path.rfind("\\") + 1:]

        frame = inspect.stack()[1]
        filename = frame[1][frame[1].rfind("\\") + 1:]
        filename = filename.replace(".py","")

        return filename
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def BLDConAttachCallback(self, HandlerSelf):

        try:

            ##############################
            self.BLDCobject.setDataInterval(self.UpdateDeltaT_ms)
            self.MyPrint_WithoutLogFile("The device currently has DataInterval: " + str(self.BLDCobject.getDataInterval()))
            ##############################

            ##############################
            self.BLDCobject.setRescaleFactor(self.RescaleFactor_MultipliesPhidgetsUnits_UserSet)
            self.MyPrint_WithoutLogFile("The device currently has RescaleFactor: " + str(self.BLDCobject.getRescaleFactor()))
            ##############################

            ############################## Setting StallVelocity to 0 will turn off stall protection functionality
            self.BLDCobject.setStallVelocity(self.VelocityStallLimit_PhidgetsUnits_UserSet)
            self.MyPrint_WithoutLogFile("The device currently has StallVelocity: " + str(self.BLDCobject.getStallVelocity()))
            ##############################

            ##############################
            self.Acceleration_PhidgetsUnits_TO_BE_SET = self.AccelerationMaxLimit_PhidgetsUnits_UserSet
            self.Acceleration_PhidgetsUnits_NeedsToBeChangedFlag = 1
            self.Acceleration_PhidgetsUnits_GUI_NeedsToBeChangedFlag = 0
            ##############################

            ##############################
            if self.ControlMode == "velocity":

                ##############################
                self.BLDCobject.setTargetBrakingStrength(self.BrakingStrengthLimit_VelControl_PhidgetsUnits_UserSet)
                self.MyPrint_WithoutLogFile("The device currently has BrakingStrength: " + str(self.BLDCobject.getTargetBrakingStrength()))
                ##############################

                ##############################
                if self.ThisIsFirstTimeEverAttachingFlag == 1:
                    self.Velocity_PhidgetsUnits_TO_BE_SET = 0.0
                else:
                    self.Velocity_PhidgetsUnits_TO_BE_SET = self.Velocity_PhidgetsUnits_FromDevice #Stay wherever you were when you detached

                self.Velocity_PhidgetsUnits_NeedsToBeChangedFlag = 1
                self.Velocity_PhidgetsUnits_GUI_NeedsToBeChangedFlag = 1
                ##############################

            ##############################

            ##############################
            elif self.ControlMode == "position":

                ##############################
                self.BLDCobject.setKp(self.Kp_PosControl_Gain_UserSet)
                self.MyPrint_WithoutLogFile("The device currently has Kp: " + str(self.BLDCobject.getKp()))

                self.BLDCobject.setKi(self.Ki_PosControl_Gain_UserSet)
                self.MyPrint_WithoutLogFile("The device currently has Ki: " + str(self.BLDCobject.getKi()))

                self.BLDCobject.setKd(self.Kd_PosControl_Gain_UserSet)
                self.MyPrint_WithoutLogFile("The device currently has Kd: " + str(self.BLDCobject.getKd()))
                ##############################

                ##############################
                self.EngagedState_TO_BE_SET = 1
                self.EngagedState_NeedsToBeChangedFlag = 1
                ##############################

                ##############################
                if self.ThisIsFirstTimeEverAttachingFlag == 1:
                    self.Position_PhidgetsUnits_TO_BE_SET = 0.0
                    self.DeadBand_PosControl_PhidgetsUnits_TO_BE_SET = self.DeadBand_PosControl_PhidgetsUnits_UserSet

                    self.Velocity_PhidgetsUnits_TO_BE_SET = self.VelocityMaxLimit_PhidgetsUnits_UserSet

                else:
                    self.Position_PhidgetsUnits_TO_BE_SET = self.Position_PhidgetsUnits_FromDevice #Stay wherever you were when you detached
                    self.DeadBand_PosControl_PhidgetsUnits_TO_BE_SET = self.DeadBand_PosControl_PhidgetsUnits_FromDevice

                    self.Velocity_PhidgetsUnits_TO_BE_SET = self.VelocityMaxLimit_PhidgetsUnits_UserSet

                self.Position_PhidgetsUnits_NeedsToBeChangedFlag = 1
                self.Position_PhidgetsUnits_GUI_NeedsToBeChangedFlag = 1

                self.Velocity_PhidgetsUnits_NeedsToBeChangedFlag = 1
                self.Velocity_PhidgetsUnits_GUI_NeedsToBeChangedFlag = 1

                self.DeadBand_PosControl_PhidgetsUnits_NeedsToBeChangedFlag = 1
                self.DeadBand_PosControl_PhidgetsUnits_GUI_NeedsToBeChangedFlag = 1
                ##############################

            ##############################

            ##############################
            if self.ThisIsFirstTimeEverAttachingFlag == 0:
                self.ThisIsFirstTimeEverAttachingFlag = 1
            ##############################

            self.device_connected_flag = 1
            self.MyPrint_WithoutLogFile("$$$$$$$$$$ BLDConAttachCallback Attached Event! $$$$$$$$$$")

        except PhidgetException as e:
            self.device_connected_flag = 0
            self.MyPrint_WithoutLogFile("BLDConAttachCallback ERROR: Failed to initialize the BLDC, Phidget Exception %i: %s" % (e.code, e.details))
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def BLDConDetachCallback(self, HandlerSelf):
        self.device_connected_flag = 0

        self.MyPrint_WithoutLogFile("$$$$$$$$$$ BLDConDetachCallback Detached Event! $$$$$$$$$$")

        try:
            self.BLDCobject.openWaitForAttachment(self.WaitForAttached_TimeoutDuration_Milliseconds)
            time.sleep(0.250)

        except PhidgetException as e:
            self.MyPrint_WithoutLogFile("BLDConDetachCallback failed to waitForAttach, Phidget Exception %i: %s" % (e.code, e.details))

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def BLDConVelocityUpdateCallback(self, HandlerSelf, VelocityUpdatedValue):

        self.Velocity_PhidgetsUnits_FromDevice = VelocityUpdatedValue

        #self.MyPrint_WithoutLogFile("BLDConVelocityUpdateCallback event: self.Velocity_PhidgetsUnits_FromDevice = " + str(self.Velocity_PhidgetsUnits_FromDevice))
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def BLDConPositionChangeCallback(self, HandlerSelf, PositionChangedValue):

        self.Position_PhidgetsUnits_FromDevice = PositionChangedValue

        self.CurrentTime_OnPositionChangeCallbackFunction = self.getPreciseSecondsTimeStampString()
        self.UpdateFrequencyCalculation_OnPositionChangeCallbackFunction()

        self.Velocity_PhidgetsUnits_DifferentiatedRaw = (self.Position_PhidgetsUnits_FromDevice - self.Position_PhidgetsUnits_FromDevice_Last)/(self.DataStreamingDeltaT_OnPositionChangeCallbackFunction)

        self.Velocity_PhidgetsUnits_DifferentiatedSmoothed = self.Velocity_LowPassFilter_ReubenPython2and3ClassObject.AddDataPointFromExternalProgram(self.Velocity_PhidgetsUnits_DifferentiatedRaw)["SignalOutSmoothed"]

        self.Position_PhidgetsUnits_FromDevice_Last = self.Position_PhidgetsUnits_FromDevice

        #self.MyPrint_WithoutLogFile("BLDConPositionChangeCallback event: self.Position_PhidgetsUnits_FromDevice = " + str(self.Position_PhidgetsUnits_FromDevice))
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def BLDConDutyCycleUpdateCallback(self, HandlerSelf, DutyCycleUpdatedValue):

        self.DutyCycle_PhidgetsUnits_FromDevice = DutyCycleUpdatedValue

        #self.MyPrint_WithoutLogFile("BLDConDutyCycleUpdateCallback event: self.DutyCycle_PhidgetsUnits_FromDevice = " + str(self.DutyCycle_PhidgetsUnits_FromDevice))
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def BLDConErrorCallback(self, HandlerSelf, code, description):
        self.MyPrint_WithoutLogFile("----------")
        self.MyPrint_WithoutLogFile("BLDConErrorCallback Code: " + ErrorEventCode.getName(code) + ", Description: " + str(description))
        self.MyPrint_WithoutLogFile("----------")
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def TemperatureOnAttachCallback(self, HandlerSelf):

        self.MyPrint_WithoutLogFile("$$$$$$$$$$ TemperatureOnAttachCallback Attached Event! $$$$$$$$$$")

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def TemperatureOnDetachCallback(self, HandlerSelf):

        self.MyPrint_WithoutLogFile("$$$$$$$$$$ TemperatureOnDetachCallback Detached Event! $$$$$$$$$$")

        try:
            self.TemperatureObject.openWaitForAttachment(self.WaitForAttached_TimeoutDuration_Milliseconds)
            time.sleep(0.250)

        except PhidgetException as e:
            self.MyPrint_WithoutLogFile("TemperatureOnDetachCallback failed to waitForAttach, Phidget Exception %i: %s" % (e.code, e.details))
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def TemperatureOnChangeCallback(self, HandlerSelf, TemperatureChangedValue):

        self.Temperature_DegC_FromDevice = TemperatureChangedValue

        #self.MyPrint_WithoutLogFile("TemperatureOnChangeCallback event: self.Temperature_DegC_FromDevice = " + str(self.Temperature_DegC_FromDevice))
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def TemperatureOnErrorCallback(self, HandlerSelf, code, description):
        self.MyPrint_WithoutLogFile("----------")
        self.MyPrint_WithoutLogFile("TemperatureOnErrorCallback Code: " + ErrorEventCode.getName(code) + ", Description: " + str(description))
        self.MyPrint_WithoutLogFile("----------")
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def getTimeStampString(self):

        ts = time.time()
        st = datetime.datetime.fromtimestamp(ts).strftime('date-%m-%d-%Y---time-%H-%M-%S')

        return st
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def getPreciseSecondsTimeStampString(self):
        ts = time.time()

        return ts
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def UpdateFrequencyCalculation_MainThread(self):

        try:
            self.DataStreamingDeltaT_CalculatedFromMainThread = self.CurrentTime_CalculatedFromMainThread - self.LastTime_CalculatedFromMainThread

            if self.DataStreamingDeltaT_CalculatedFromMainThread != 0.0:
                self.DataStreamingFrequency_CalculatedFromMainThread = 1.0/self.DataStreamingDeltaT_CalculatedFromMainThread

            self.LastTime_CalculatedFromMainThread = self.CurrentTime_CalculatedFromMainThread
        except:
            exceptions = sys.exc_info()[0]
            print("UpdateFrequencyCalculation_MainThread ERROR with Exceptions: %s" % exceptions)
            traceback.print_exc()
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def UpdateFrequencyCalculation_OnPositionChangeCallbackFunction(self):

        try:
            self.DataStreamingDeltaT_OnPositionChangeCallbackFunction = self.CurrentTime_OnPositionChangeCallbackFunction - self.LastTime_OnPositionChangeCallbackFunction

            if self.DataStreamingDeltaT_OnPositionChangeCallbackFunction != 0.0:
                self.DataStreamingFrequency_OnPositionChangeCallbackFunction = 1.0/self.DataStreamingDeltaT_OnPositionChangeCallbackFunction

            self.LastTime_OnPositionChangeCallbackFunction = self.CurrentTime_OnPositionChangeCallbackFunction
        except:
            exceptions = sys.exc_info()[0]
            print("UpdateFrequencyCalculation_OnPositionChangeCallbackFunction ERROR with Exceptions: %s" % exceptions)
            traceback.print_exc()
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ########################################################################################################## unicorn
    def CommandMotorFromExternalProgram_PositionControl(self, commanded_position_PhidgetsUnits, commanded_velocity_limit_PhidgetsUnits = -11111.0):

        ######################
        if self.ACCEPT_EXTERNAL_POSITION_COMMANDS_FLAG == 0:
            self.MyPrint_WithoutLogFile("CommandMotorFromExternalProgram ERROR: ACCEPT_EXTERNAL_POSITION_COMMANDS_FLAG = 0")
            return 0
        ######################

        ######################
        if self.ControlMode != "position":
            self.MyPrint_WithoutLogFile("CommandMotorFromExternalProgram ERROR: self.ControlMode must be 'position'")
            return 0
        ######################

        ######################
        self.Position_PhidgetsUnits_TO_BE_SET = self.limitNumber(self.PositionMinLimit_PhidgetsUnits_UserSet, self.PositionMaxLimit_PhidgetsUnits_UserSet, commanded_position_PhidgetsUnits)
        self.Position_PhidgetsUnits_NeedsToBeChangedFlag = 1
        self.Position_PhidgetsUnits_GUI_NeedsToBeChangedFlag = 1
        ######################

        ######################
        if commanded_velocity_limit_PhidgetsUnits != -11111.0:
            if commanded_velocity_limit_PhidgetsUnits != self.Velocity_PhidgetsUnits_TO_BE_SET:
                self.Velocity_PhidgetsUnits_TO_BE_SET = self.limitNumber(self.VelocityMinLimit_PhidgetsUnits_UserSet, self.VelocityMaxLimit_PhidgetsUnits_UserSet, commanded_velocity_limit_PhidgetsUnits)
                self.Velocity_PhidgetsUnits_NeedsToBeChangedFlag = 1
                self.Velocity_PhidgetsUnits_GUI_NeedsToBeChangedFlag = 1
        ######################

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def CommandMotorFromExternalProgram_VelocityControl(self, commanded_velocity_PhidgetsUnits):

        ######################
        if self.ACCEPT_EXTERNAL_POSITION_COMMANDS_FLAG == 0:
            self.MyPrint_WithoutLogFile("CommandMotorFromExternalProgram ERROR: ACCEPT_EXTERNAL_POSITION_COMMANDS_FLAG = 0")
            return 0
        ######################
        
        ######################
        if self.ControlMode != "velocity":
            self.MyPrint_WithoutLogFile("CommandMotorFromExternalProgram ERROR: self.ControlMode must be 'velocity'")
            return 0
        ######################

        ######################
        self.Velocity_PhidgetsUnits_TO_BE_SET = self.limitNumber(self.VelocityMinLimit_PhidgetsUnits_UserSet, self.VelocityMaxLimit_PhidgetsUnits_UserSet, commanded_velocity_PhidgetsUnits)
        self.Velocity_PhidgetsUnits_NeedsToBeChangedFlag = 1
        self.Velocity_PhidgetsUnits_GUI_NeedsToBeChangedFlag = 1
        ######################
        
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def StopMotor(self):

        if self.ControlMode == "velocity":
            self.Velocity_PhidgetsUnits_TO_BE_SET = 0
            self.Velocity_PhidgetsUnits_NeedsToBeChangedFlag = 1
            self.Velocity_PhidgetsUnits_GUI_NeedsToBeChangedFlag = 1

        elif self.ControlMode == "position":
            self.EngagedState_TO_BE_SET = 0
            self.EngagedState_NeedsToBeChangedFlag = 1

        self.MyPrint_WithoutLogFile("StopMotor function called!")
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def SetPositionOffsetOnBoardWithoutMoving(self, commanded_position_offset_value_PhidgetsUnits):

        commanded_position_offset_value_PhidgetsUnits_LIMITED = self.limitNumber(self.PositionMinLimit_PhidgetsUnits_UserSet, self.PositionMaxLimit_PhidgetsUnits_UserSet, commanded_position_offset_value_PhidgetsUnits)

        try:
            self.BLDCobject.addPositionOffset(commanded_position_offset_value_PhidgetsUnits_LIMITED)
            self.MyPrint_WithoutLogFile("SetPositionOffsetOnBoardWithoutMoving issued addPositionOffset for value of " + str(commanded_position_offset_value_PhidgetsUnits_LIMITED))
            return 1

        except PhidgetException as e:
            self.MyPrint_WithoutLogFile("SetPositionOffsetOnBoardWithoutMoving ERROR, Phidget Exception %i: %s" % (e.code, e.details))
            return 0

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ########################################################################################################## unicorn
    def HomeMotorInPlace(self):

        Position_PhidgetsUnits_FromDevice_JUST_QUERIED = self.BLDCobject.getPosition()
        self.MyPrint_WithoutLogFile("HomeMotorInPlace Position_PhidgetsUnits_FromDevice_JUST_QUERIED BEFORE adding offset: " + str(Position_PhidgetsUnits_FromDevice_JUST_QUERIED))

        self.BLDCobject.addPositionOffset(-1.0*Position_PhidgetsUnits_FromDevice_JUST_QUERIED) #MUST HAVE THE MINUS SIGN, OR ELSE THE OFFSET DOESN'T SET UT TO ZERO.

        Position_PhidgetsUnits_FromDevice_JUST_QUERIED = self.BLDCobject.getPosition()
        self.MyPrint_WithoutLogFile("HomeMotorInPlace Position_PhidgetsUnits_FromDevice_JUST_QUERIED AFTER adding offset: " + str(Position_PhidgetsUnits_FromDevice_JUST_QUERIED))

        if self.ControlMode == "position":
            for counter in range(0, 4): #SEND COMMAND MULTIPLE TIMES TO MAKE SURE THAT IT TAKES!
                self.Position_PhidgetsUnits_TO_BE_SET = 0.0
                self.Position_PhidgetsUnits_NeedsToBeChangedFlag = 1
                self.Position_PhidgetsUnits_GUI_NeedsToBeChangedFlag = 1
                time.sleep(0.005)

        self.MyPrint_WithoutLogFile("----- HomeMotorInPlace just performed! -----")

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def MainThread(self): #unicorn

        self.MyPrint_WithoutLogFile("Started MainThread for PhidgetBrushlessDCmotorDCC1100controller_ReubenPython2and3Class.")

        self.MainThread_still_running_flag = 1

        self.ACCEPT_EXTERNAL_POSITION_COMMANDS_FLAG = 1

        self.BLDCobject.enableFailsafe(self.FailsafeTime_Milliseconds)

        self.StartingTime_CalculatedFromMainThread = self.getPreciseSecondsTimeStampString()

        ###############################################
        while self.EXIT_PROGRAM_FLAG == 0:

            ###############################################
            self.CurrentTime_CalculatedFromMainThread = self.getPreciseSecondsTimeStampString() - self.StartingTime_CalculatedFromMainThread
            ###############################################

            ###############################################
            if self.CurrentTime_CalculatedFromMainThread - self.LastTime_FailsafeWasReset >= 0.5*self.FailsafeTime_Milliseconds/1000.0: #IF YOU CALL resetFailsafe every PID loop, it'll kill your loop frequency
                #self.MyPrint_WithoutLogFile("RESET FAILSAFE AT TIME = " + str(self.CurrentTime_CalculatedFromMainThread))
                self.BLDCobject.resetFailsafe() #resetFailsafe is faster than enableFailsafe
                self.LastTime_FailsafeWasReset = self.CurrentTime_CalculatedFromMainThread
            ###############################################

            ###############################################
            ############################################### Start SETs

            ###############################################
            if self.StopMotor_NeedsToBeChangedFlag == 1:
                self.StopMotor()
                self.StopMotor_NeedsToBeChangedFlag = 0
            ###############################################

            ###############################################
            if self.HomeMotorInPlace_NeedsToBeHomedFlag == 1:
                self.HomeMotorInPlace()
                self.HomeMotorInPlace_NeedsToBeHomedFlag = 0
            ###############################################

            ###############################################
            if self.EngagedState_NeedsToBeChangedFlag == 1 and self.ControlMode == "position":
                try:
                    #self.MyPrint_WithoutLogFile("Sending Engaged State to the Phidget.")
                    self.BLDCobject.setEngaged(self.EngagedState_TO_BE_SET)
                    if self.BLDCobject.getEngaged() == 1:
                        self.EngagedState_NeedsToBeChangedFlag = 0
                except:
                    self.MyPrint_WithoutLogFile("ERROR: Failed to change EngagedState!")
            ###############################################

            ############################################### Tx portion
            if self.Position_PhidgetsUnits_NeedsToBeChangedFlag == 1 and self.ControlMode == "position":
                try:
                    #self.MyPrint_WithoutLogFile("Sending Position to the Phidget, value of " + str(self.Position_PhidgetsUnits_TO_BE_SET))
                    self.Position_PhidgetsUnits_TO_BE_SET = self.limitNumber(self.PositionMinLimit_PhidgetsUnits_UserSet, self.PositionMaxLimit_PhidgetsUnits_UserSet, self.Position_PhidgetsUnits_TO_BE_SET)
                    self.BLDCobject.setTargetPosition(float(self.Position_PhidgetsUnits_TO_BE_SET))
                    self.Position_PhidgetsUnits_NeedsToBeChangedFlag = 0

                except PhidgetException as e:
                    self.MyPrint_WithoutLogFile("Failed setTargetPosition, Phidget Exception %i: %s" % (e.code, e.details))
            ###############################################

            ###############################################
            if self.Velocity_PhidgetsUnits_NeedsToBeChangedFlag == 1:
                try:
                    #self.MyPrint_WithoutLogFile("Sending Velocity to the Phidget.")
                    self.Velocity_PhidgetsUnits_TO_BE_SET = self.limitNumber(self.VelocityMinLimit_PhidgetsUnits_UserSet, self.VelocityMaxLimit_PhidgetsUnits_UserSet, self.Velocity_PhidgetsUnits_TO_BE_SET)

                    if self.ControlMode == "position":
                        self.BLDCobject.setVelocityLimit(float(self.Velocity_PhidgetsUnits_TO_BE_SET))

                    elif self.ControlMode == "velocity":
                        self.BLDCobject.setTargetVelocity(float(self.Velocity_PhidgetsUnits_TO_BE_SET))

                    self.Velocity_PhidgetsUnits_NeedsToBeChangedFlag = 0

                except PhidgetException as e:
                    self.MyPrint_WithoutLogFile("Failed setVelocityLimit, Phidget Exception %i: %s" % (e.code, e.details))
            ###############################################

            ###############################################
            if self.Acceleration_PhidgetsUnits_NeedsToBeChangedFlag == 1:
                try:
                    #self.MyPrint_WithoutLogFile("Sending Acceleration to the Phidget.")
                    self.Acceleration_PhidgetsUnits_TO_BE_SET = self.limitNumber(self.AccelerationMinLimit_PhidgetsUnits_FromDevice, self.AccelerationMaxLimit_PhidgetsUnits_FromDevice, self.Acceleration_PhidgetsUnits_TO_BE_SET)
                    self.BLDCobject.setAcceleration(float(self.Acceleration_PhidgetsUnits_TO_BE_SET))
                    self.Acceleration_PhidgetsUnits_NeedsToBeChangedFlag = 0

                except PhidgetException as e:
                    self.MyPrint_WithoutLogFile("Failed setAcceleration, Phidget Exception %i: %s" % (e.code, e.details))
            ###############################################

            ###############################################
            if self.DeadBand_PosControl_PhidgetsUnits_NeedsToBeChangedFlag == 1 and self.ControlMode == "position":
                try:
                    self.MyPrint_WithoutLogFile("Sending DeadBand to the Phidget, value = " + str(self.DeadBand_PosControl_PhidgetsUnits_TO_BE_SET))
                    self.DeadBand_PosControl_PhidgetsUnits_TO_BE_SET = self.limitNumber(0, self.PositionMaxLimit_PhidgetsUnits_UserSet, self.DeadBand_PosControl_PhidgetsUnits_TO_BE_SET) #Limit to max position since DeadBand is in position units
                    self.BLDCobject.setDeadBand(float(self.DeadBand_PosControl_PhidgetsUnits_TO_BE_SET))
                    #time.sleep(0.001)
                    self.DeadBand_PosControl_PhidgetsUnits_FromDevice = self.BLDCobject.getDeadBand()
                    #print("self.DeadBand_PosControl_PhidgetsUnits_TO_BE_SET: " + str(self.DeadBand_PosControl_PhidgetsUnits_TO_BE_SET))
                    if self.DeadBand_PosControl_PhidgetsUnits_FromDevice == self.DeadBand_PosControl_PhidgetsUnits_TO_BE_SET:
                        self.DeadBand_PosControl_PhidgetsUnits_NeedsToBeChangedFlag = 0

                except PhidgetException as e:
                    self.MyPrint_WithoutLogFile("Failed setTargetDeadBand, Phidget Exception %i: %s" % (e.code, e.details))
            ###############################################

            ###############################################
            ############################################### End SETs

            ###############################################
            ############################################### Start GETs
            if self.ControlMode == "position":
                self.EngagedState_PhidgetsUnits_FromDevice = self.BLDCobject.getEngaged() #NOT INCLUDING UNDER ENABLE_GETS_MAINTHREAD BECAUSE THIS IS CRITICAL TO FUNCTIONALITY

            if self.ENABLE_GETS_MAINTHREAD == 1:
                self.VelocityStall_PhidgetsUnits_FromDevice = self.BLDCobject.getStallVelocity()

                self.Acceleration_PhidgetsUnits_FromDevice = self.BLDCobject.getAcceleration()

                if self.ControlMode == "position":
                    self.DeadBand_PosControl_PhidgetsUnits_FromDevice = self.BLDCobject.getDeadBand()
                    #print(self.DeadBand_PosControl_PhidgetsUnits_FromDevice)
            ###############################################
            ############################################### End GETs

            ###############################################
            self.MostRecentDataDict = dict([("Position_PhidgetsUnits_FromDevice", self.Position_PhidgetsUnits_FromDevice),
                                            ("Velocity_PhidgetsUnits_FromDevice", self.Velocity_PhidgetsUnits_FromDevice),
                                            ("Velocity_PhidgetsUnits_DifferentiatedRaw", self.Velocity_PhidgetsUnits_DifferentiatedRaw),
                                            ("Velocity_PhidgetsUnits_DifferentiatedSmoothed", self.Velocity_PhidgetsUnits_DifferentiatedSmoothed),
                                            ("DutyCycle_PhidgetsUnits_FromDevice", self.DutyCycle_PhidgetsUnits_FromDevice),
                                            ("Temperature_DegC_FromDevice", self.Temperature_DegC_FromDevice),
                                            ("Time", self.CurrentTime_CalculatedFromMainThread)])
            ###############################################

            ############################################### USE THE TIME.SLEEP() TO SET THE LOOP FREQUENCY
            ###############################################
            ###############################################
            self.UpdateFrequencyCalculation_MainThread()

            if self.MainThread_TimeToSleepEachLoop > 0.0:
                time.sleep(self.MainThread_TimeToSleepEachLoop)

            ###############################################
            ###############################################
            ###############################################

        ###############################################

        self.MyPrint_WithoutLogFile("Finished the MainThread for PhidgetBrushlessDCmotorDCC1100controller_ReubenPython2and3Class object.")
        self.MainThread_still_running_flag = 0

        return 0
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def GetMostRecentDataDict(self):

        return self.MostRecentDataDict
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def ExitProgram_Callback(self):

        print("Exiting all threads for Phidgets4EncoderAndDInput1047_ReubenPython2and3Class object")

        self.EXIT_PROGRAM_FLAG = 1

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def StartGUI(self, GuiParent=None):

        GUI_Thread_ThreadingObject = threading.Thread(target=self.GUI_Thread, args=(GuiParent,))
        GUI_Thread_ThreadingObject.setDaemon(True) #Should mean that the GUI thread is destroyed automatically when the main thread is destroyed.
        GUI_Thread_ThreadingObject.start()
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def GUI_Thread(self, parent=None):

        print("Starting the GUI_Thread for PhidgetBrushlessDCmotorDCC1100controller_ReubenPython2and3Class object.")

        ###################################################
        if parent == None:  #This class object owns root and must handle it properly
            self.root = Tk()
            self.parent = self.root

            ################################################### SET THE DEFAULT FONT FOR ALL WIDGETS CREATED AFTTER/BELOW THIS CALL
            default_font = tkFont.nametofont("TkDefaultFont")
            default_font.configure(size=8)
            self.root.option_add("*Font", default_font)
            ###################################################

        else:
            self.root = parent
            self.parent = parent
        ###################################################

        ###################################################
        self.myFrame = Frame(self.root)

        if self.UseBorderAroundThisGuiObjectFlag == 1:
            self.myFrame["borderwidth"] = 2
            self.myFrame["relief"] = "ridge"

        self.myFrame.grid(row = self.GUI_ROW,
                          column = self.GUI_COLUMN,
                          padx = self.GUI_PADX,
                          pady = self.GUI_PADY,
                          rowspan = self.GUI_ROWSPAN,
                          columnspan= self.GUI_COLUMNSPAN)
        ###################################################

        ###################################################
        self.TKinter_LightGreenColor = '#%02x%02x%02x' % (150, 255, 150) #RGB
        self.TKinter_LightRedColor = '#%02x%02x%02x' % (255, 150, 150) #RGB
        self.TKinter_LightYellowColor = '#%02x%02x%02x' % (255, 255, 150)  # RGB
        self.TKinter_DefaultGrayColor = '#%02x%02x%02x' % (240, 240, 240)  # RGB
        self.TkinterScaleWidth = 10
        self.TkinterScaleLength = 250
        ###################################################

        ###################################################
        self.device_info_label = Label(self.myFrame, text="Device Info", width=75)

        self.device_info_label["text"] = self.NameToDisplay_UserSet + \
                                         "\nDevice Name: " + self.DetectedDeviceName + \
                                         "\nVINT SerialNumber: " + str(self.VINT_DetectedSerialNumber) + \
                                         "\nDeviceID: " + str(self.DetectedDeviceID) + \
                                         "\nFW Ver: " + str(self.DetectedDeviceVersion) + \
                                         "\nLibrary Ver: " + str(self.DetectedDeviceLibraryVersion)

        self.device_info_label.grid(row=0, column=0, padx=1, pady=1, columnspan=1, rowspan=1)
        ###################################################

        ###################################################
        self.data_label = Label(self.myFrame, text="Data Info", width=75)
        self.data_label.grid(row=1, column=0, padx=1, pady=1, columnspan=1, rowspan=1)
        ###################################################

        ########################
        self.PrintToGui_Label = Label(self.myFrame, text="PrintToGui_Label", width=75)
        if self.EnableInternal_MyPrint_Flag == 1:
            self.PrintToGui_Label.grid(row=2, column=0, padx=1, pady=1, columnspan=1, rowspan=10)
        ########################

        #################################################
        self.Position_PhidgetsUnits_ScaleLabel = Label(self.myFrame, text="Position", width=20)
        self.Position_PhidgetsUnits_ScaleLabel.grid(row=1, column=1, padx=1, pady=1, columnspan=1, rowspan=1)

        # self.PositionMinLimit_PhidgetsUnits_UserSet,\  #self.PositionMaxLimit_PhidgetsUnits_UserSet, \
        self.Position_PhidgetsUnits_ScaleValue = DoubleVar()
        self.Position_PhidgetsUnits_Scale = Scale(self.myFrame, \
                                            from_=self.PositionMinLimit_PhidgetsUnits_UserSet,\
                                            to= self.PositionMaxLimit_PhidgetsUnits_UserSet,\
                                            #tickinterval=(self.Position_PhidgetsUnits_max - self.Position_PhidgetsUnits_min) / 2.0,\
                                            orient=HORIZONTAL,\
                                            borderwidth=2,\
                                            showvalue=1,\
                                            width=self.TkinterScaleWidth,\
                                            length=self.TkinterScaleLength,\
                                            resolution=0.1,\
                                            variable=self.Position_PhidgetsUnits_ScaleValue)
        self.Position_PhidgetsUnits_Scale.bind('<Button-1>', lambda event, name="Position": self.Position_PhidgetsUnits_ScaleResponse(event, name)) #Use both '<Button-1>' or '<ButtonRelease-1>'
        self.Position_PhidgetsUnits_Scale.bind('<B1-Motion>', lambda event, name="Position": self.Position_PhidgetsUnits_ScaleResponse(event, name))
        self.Position_PhidgetsUnits_Scale.bind('<ButtonRelease-1>', lambda event, name="Position": self.Position_PhidgetsUnits_ScaleResponse(event, name)) #Use both '<Button-1>' or '<ButtonRelease-1>'
        self.Position_PhidgetsUnits_Scale.set(self.Position_PhidgetsUnits_TO_BE_SET)
        self.Position_PhidgetsUnits_Scale.grid(row=1, column=2, padx=1, pady=1, columnspan=2, rowspan=1)

        if self.ControlMode == "velocity":
            self.Position_PhidgetsUnits_Scale["state"] = "disabled"
        #################################################

        #################################################
        self.Velocity_PhidgetsUnits_ScaleLabel = Label(self.myFrame, text="Velocity", width=20)
        self.Velocity_PhidgetsUnits_ScaleLabel.grid(row=2, column=1, padx=1, pady=1, columnspan=1, rowspan=1)

        self.Velocity_PhidgetsUnits_ScaleValue = DoubleVar()
        self.Velocity_PhidgetsUnits_Scale = Scale(self.myFrame, \
                                            from_=self.VelocityMinLimit_PhidgetsUnits_UserSet,\
                                            to=self.VelocityMaxLimit_PhidgetsUnits_UserSet, \
                                            #tickinterval=(self.Velocity_PhidgetsUnits_max - self.Velocity_PhidgetsUnits_min) / 2.0,\
                                            orient=HORIZONTAL,\
                                            borderwidth=2,\
                                            showvalue=1,\
                                            width=self.TkinterScaleWidth,\
                                            length=self.TkinterScaleLength,\
                                            resolution=0.001,\
                                            variable=self.Velocity_PhidgetsUnits_ScaleValue)
        self.Velocity_PhidgetsUnits_Scale.bind('<Button-1>', lambda event, name="Velocity": self.Velocity_PhidgetsUnits_ScaleResponse(event, name)) #Use both '<Button-1>' or '<ButtonRelease-1>'
        self.Velocity_PhidgetsUnits_Scale.bind('<B1-Motion>', lambda event, name="Velocity": self.Velocity_PhidgetsUnits_ScaleResponse(event, name))
        self.Velocity_PhidgetsUnits_Scale.bind('<ButtonRelease-1>', lambda event, name="Velocity": self.Velocity_PhidgetsUnits_ScaleResponse(event, name)) #Use both '<Button-1>' or '<ButtonRelease-1>'
        self.Velocity_PhidgetsUnits_Scale.set(self.Velocity_PhidgetsUnits_TO_BE_SET)
        self.Velocity_PhidgetsUnits_Scale.grid(row=2, column=2, padx=1, pady=1, columnspan=2, rowspan=1)

        self.Velocity_PhidgetsUnits_Scale["troughcolor"] = self.TKinter_LightGreenColor

        #if self.ControlMode == "position":
        #    self.Velocity_PhidgetsUnits_Scale["state"] = "disabled"
        #elif self.ControlMode == "velocity":
        #    self.Velocity_PhidgetsUnits_Scale["troughcolor"] = self.TKinter_LightGreenColor
        #################################################

        #################################################
        self.Acceleration_PhidgetsUnits_ScaleLabel = Label(self.myFrame, text="Acceleration", width=20)
        self.Acceleration_PhidgetsUnits_ScaleLabel.grid(row=3, column=1, padx=1, pady=1, columnspan=1, rowspan=1)

        self.Acceleration_PhidgetsUnits_ScaleValue = DoubleVar()
        self.Acceleration_PhidgetsUnits_Scale = Scale(self.myFrame, \
                                            from_=self.AccelerationMinLimit_PhidgetsUnits_FromDevice,\
                                            to=self.AccelerationMaxLimit_PhidgetsUnits_UserSet, \
                                            #tickinterval=(self.Acceleration_PhidgetsUnits_max - self.Acceleration_PhidgetsUnits_min) / 2.0,\
                                            orient=HORIZONTAL,\
                                            borderwidth=2,\
                                            showvalue=1,\
                                            width=self.TkinterScaleWidth,\
                                            length=self.TkinterScaleLength,\
                                            resolution=0.001,\
                                            variable=self.Acceleration_PhidgetsUnits_ScaleValue)
        self.Acceleration_PhidgetsUnits_Scale.bind('<Button-1>', lambda event, name="Acceleration": self.Acceleration_PhidgetsUnits_ScaleResponse(event, name)) #Use both '<Button-1>' or '<ButtonRelease-1>'
        self.Acceleration_PhidgetsUnits_Scale.bind('<B1-Motion>', lambda event, name="Acceleration": self.Acceleration_PhidgetsUnits_ScaleResponse(event, name))
        self.Acceleration_PhidgetsUnits_Scale.bind('<ButtonRelease-1>', lambda event, name="Acceleration": self.Acceleration_PhidgetsUnits_ScaleResponse(event, name)) #Use both '<Button-1>' or '<ButtonRelease-1>'
        self.Acceleration_PhidgetsUnits_Scale.set(self.Acceleration_PhidgetsUnits_TO_BE_SET)
        self.Acceleration_PhidgetsUnits_Scale.grid(row=3, column=2, padx=1, pady=1, columnspan=2, rowspan=1)

        if self.ControlMode == "position":
            pass #Color gets controlled by engaged flag within the main GUI loop
        elif self.ControlMode == "velocity":
            self.Acceleration_PhidgetsUnits_Scale["troughcolor"] = self.TKinter_LightGreenColor
        #################################################

        #################################################
        self.DeadBand_PosControl_PhidgetsUnits_ScaleLabel = Label(self.myFrame, text="DeadBand", width=20)
        self.DeadBand_PosControl_PhidgetsUnits_ScaleLabel.grid(row=4, column=1, padx=1, pady=1, columnspan=1, rowspan=1)

        # self.DeadBandMinLimit_PhidgetsUnits_UserSet,\  #self.DeadBandMaxLimit_PhidgetsUnits_UserSet, \
        self.DeadBand_PosControl_PhidgetsUnits_ScaleValue = DoubleVar()
        self.DeadBand_PosControl_PhidgetsUnits_Scale = Scale(self.myFrame, \
                                            from_=0,\
                                            to= self.PositionMaxLimit_PhidgetsUnits_UserSet,\
                                            #tickinterval=(self.DeadBand_PosControl_PhidgetsUnits_max - self.DeadBand_PosControl_PhidgetsUnits_min) / 2.0,\
                                            orient=HORIZONTAL,\
                                            borderwidth=2,\
                                            showvalue=1,\
                                            width=self.TkinterScaleWidth,\
                                            length=self.TkinterScaleLength,\
                                            resolution=0.1,\
                                            variable=self.DeadBand_PosControl_PhidgetsUnits_ScaleValue)
        self.DeadBand_PosControl_PhidgetsUnits_Scale.bind('<Button-1>', lambda event, name="DeadBand": self.DeadBand_PosControl_PhidgetsUnits_ScaleResponse(event, name)) #Use both '<Button-1>' or '<ButtonRelease-1>'
        self.DeadBand_PosControl_PhidgetsUnits_Scale.bind('<B1-Motion>', lambda event, name="DeadBand": self.DeadBand_PosControl_PhidgetsUnits_ScaleResponse(event, name))
        self.DeadBand_PosControl_PhidgetsUnits_Scale.bind('<ButtonRelease-1>', lambda event, name="DeadBand": self.DeadBand_PosControl_PhidgetsUnits_ScaleResponse(event, name)) #Use both '<Button-1>' or '<ButtonRelease-1>'
        self.DeadBand_PosControl_PhidgetsUnits_Scale.set(self.DeadBand_PosControl_PhidgetsUnits_TO_BE_SET)
        self.DeadBand_PosControl_PhidgetsUnits_Scale.grid(row=4, column=2, padx=1, pady=1, columnspan=2, rowspan=1)

        if self.ControlMode == "velocity":
            self.DeadBand_PosControl_PhidgetsUnits_Scale["state"] = "disabled"
        #################################################

        '''
        ###########################################################
        ###########################################################
        self.Entry_Width = 15
        self.Entry_Label_Width = 15
        self.Entry_FontSize = 8
        self.AllEntriesFrame = Frame(self.myFrame)
        self.AllEntriesFrame["borderwidth"] = 2
        #self.AllEntriesFrame["relief"] = "ridge"
        self.AllEntriesFrame.grid(row=2, column=0, padx=1, pady=1, columnspan=10, rowspan=1, sticky="W")
        ###########################################################
        ###########################################################

        ###########################################################
        ###########################################################
        self.VelocityMaxLimit_PhidgetsUnits_label = Label(self.AllEntriesFrame, text="VelocityMax", width=self.Entry_Label_Width)
        self.VelocityMaxLimit_PhidgetsUnits_label.grid(row=0, column=0, padx=1, pady=1, columnspan=1, rowspan=1)

        self.VelocityMaxLimit_PhidgetsUnits_StringVar = StringVar()
        self.VelocityMaxLimit_PhidgetsUnits_StringVar.set(self.VelocityMaxLimit_PhidgetsUnits_UserSet)

        self.VelocityMaxLimit_PhidgetsUnits_TextInputBox = Entry(self.AllEntriesFrame,
                                            font=("Helvetica", int(self.Entry_FontSize)),
                                            state="normal",
                                            width=int(self.Entry_Width),
                                            textvariable=self.VelocityMaxLimit_PhidgetsUnits_StringVar,
                                            justify='center')

        self.VelocityMaxLimit_PhidgetsUnits_TextInputBox.bind('<Return>', lambda event, name = "<Return>": self.VelocityMaxLimit_PhidgetsUnits_TextInputBoxResponse(event, name))
        #self.VelocityMaxLimit_PhidgetsUnits_TextInputBox.bind('<Button-1>', lambda event, name = "<Button-1>": self.VelocityMaxLimit_PhidgetsUnits_TextInputBoxResponse(event, name))
        #self.VelocityMaxLimit_PhidgetsUnits_TextInputBox.bind('<Button-2>', lambda event, name = "<Button-2>": self.VelocityMaxLimit_PhidgetsUnits_TextInputBoxResponse(event, name))
        #self.VelocityMaxLimit_PhidgetsUnits_TextInputBox.bind('<Button-3>', lambda event, name = "<Button-3>": self.VelocityMaxLimit_PhidgetsUnits_TextInputBoxResponse(event, name))
        #self.VelocityMaxLimit_PhidgetsUnits_TextInputBox.bind('<Leave>', lambda event, name = "<Leave>": self.VelocityMaxLimit_PhidgetsUnits_TextInputBoxResponse(event, name))
        self.VelocityMaxLimit_PhidgetsUnits_TextInputBox.grid(row=1, column=0, padx=0, pady=0, columnspan=1, rowspan=1)
        ###########################################################
        ###########################################################
        '''

        ###########################################################
        ###########################################################
        self.Button_Width = 15
        self.AllButtonsFrame = Frame(self.myFrame)
        self.AllButtonsFrame["borderwidth"] = 2
        #self.AllButtonsFrame["relief"] = "ridge"
        self.AllButtonsFrame.grid(row=0, column=2, padx=1, pady=1, columnspan=1, rowspan=1, sticky="W")
        ###########################################################
        ###########################################################

        ###########################################################
        ###########################################################
        self.HomeMotorInPlaceButton = Button(self.AllButtonsFrame, text='HomeInPlace', state="normal", width=self.Button_Width, command=lambda i=1: self.HomeMotorInPlaceButtonResponse())
        self.HomeMotorInPlaceButton.grid(row=0, column=0, padx=1, pady=1, columnspan=1, rowspan=1)

        if self.ControlMode == "position":
            self.HomeMotorInPlaceButton["bg"] = self.TKinter_LightGreenColor
        elif self.ControlMode == "velocity":
            self.HomeMotorInPlaceButton["state"] = "disabled"
        ###########################################################
        ###########################################################

        ###########################################################
        ###########################################################
        self.EngagedStateButton = Button(self.AllButtonsFrame, text='Engaged: x', state="normal", width=self.Button_Width, command=lambda i=1: self.EngagedStateButtonResponse())
        self.EngagedStateButton.grid(row=0, column=1, padx=1, pady=1, columnspan=1, rowspan=1)
        if self.ControlMode == "velocity":
            self.EngagedStateButton["state"] = "disabled"
        ###########################################################
        ###########################################################

        ###########################################################
        ###########################################################
        self.StopMotorButton = Button(self.AllButtonsFrame, text='Stop Motor', state="normal", width=self.Button_Width, command=lambda i=1: self.StopMotorButtonResponse())
        self.StopMotorButton.grid(row=0, column=2, padx=1, pady=1, columnspan=1, rowspan=1)
        self.StopMotorButton["bg"] = self.TKinter_LightGreenColor
        ###########################################################
        ###########################################################

        ########################
        if self.RootIsOwnedExternallyFlag == 0: #This class object owns root and must handle it properly
            self.root.protocol("WM_DELETE_WINDOW", self.ExitProgram_Callback)

            self.root.after(self.GUI_RootAfterCallbackInterval_Milliseconds, self.GUI_update_clock)
            self.GUI_ready_to_be_updated_flag = 1
            self.root.mainloop()
        else:
            self.GUI_ready_to_be_updated_flag = 1
        ########################

        ########################
        if self.RootIsOwnedExternallyFlag == 0: #This class object owns root and must handle it properly
            self.root.quit()  # Stop the GUI thread, MUST BE CALLED FROM GUI_Thread
            self.root.destroy()  # Close down the GUI thread, MUST BE CALLED FROM GUI_Thread
        ########################

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def Position_PhidgetsUnits_ScaleResponse(self, event, name):

        self.Position_PhidgetsUnits_TO_BE_SET = self.Position_PhidgetsUnits_ScaleValue.get()
        self.Position_PhidgetsUnits_NeedsToBeChangedFlag = 1

        #self.MyPrint_WithoutLogFile("Position_PhidgetsUnits_ScaleResponse: Position set to: " + str(self.Position_PhidgetsUnits_TO_BE_SET))
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def Velocity_PhidgetsUnits_ScaleResponse(self, event, name):

        self.Velocity_PhidgetsUnits_TO_BE_SET = self.Velocity_PhidgetsUnits_ScaleValue.get()
        self.Velocity_PhidgetsUnits_NeedsToBeChangedFlag = 1

        #self.MyPrint_WithoutLogFile("Velocity_PhidgetsUnits_ScaleResponse: Velocity set to: " + str(self.Velocity_PhidgetsUnits_TO_BE_SET))
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def Acceleration_PhidgetsUnits_ScaleResponse(self, event, name):

        self.Acceleration_PhidgetsUnits_TO_BE_SET = self.Acceleration_PhidgetsUnits_ScaleValue.get()
        self.Acceleration_PhidgetsUnits_NeedsToBeChangedFlag = 1

        #self.MyPrint_WithoutLogFile("Acceleration_PhidgetsUnits_ScaleResponse: Acceleration set to: " + str(self.Acceleration_PhidgetsUnits_TO_BE_SET))
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def DeadBand_PosControl_PhidgetsUnits_ScaleResponse(self, event, name):

        self.DeadBand_PosControl_PhidgetsUnits_TO_BE_SET = self.DeadBand_PosControl_PhidgetsUnits_ScaleValue.get()
        self.DeadBand_PosControl_PhidgetsUnits_NeedsToBeChangedFlag = 1

        #self.MyPrint_WithoutLogFile("DeadBand_PosControl_PhidgetsUnits_ScaleResponse: DeadBand set to: " + str(self.DeadBand_PosControl_PhidgetsUnits_TO_BE_SET))
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def SetEngagedState(self, StateToBeSet):

        if StateToBeSet not in [0, 1]:
            self.MyPrint_WithoutLogFile("SetEngagedState ERROR: StateToBeSet must be 0 or 1.")
            return 0
        else:
            self.EngagedState_TO_BE_SET = StateToBeSet
            self.EngagedState_NeedsToBeChangedFlag = 1
            return 1

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def EngagedStateButtonResponse(self):

        if self.EngagedState_PhidgetsUnits_FromDevice == 1:
            self.SetEngagedState(0)
        else:
            self.SetEngagedState(1)

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def StopMotorButtonResponse(self):

        self.StopMotor_NeedsToBeChangedFlag = 1
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def HomeMotorInPlaceButtonResponse(self):

        self.HomeMotorInPlace_NeedsToBeHomedFlag = 1

    ##########################################################################################################
    ##########################################################################################################

    '''
    ##########################################################################################################
    ##########################################################################################################
    def VelocityMaxLimit_PhidgetsUnits_TextInputBoxResponse(self, event=None, name="default"):

        try:
            if name == "<Button-1>" or name == "<Button-2>" or name == "<Button-3>" or name == "<Leave>":
                pass

            elif name == "<Return>":  # When user hits 'Return'
                VelocityMaxLimit_PhidgetsUnits_UserSet_temp = float(self.VelocityMaxLimit_PhidgetsUnits_StringVar.get())
                self.VelocityMaxLimit_PhidgetsUnits_UserSet = self.LimitNumber_StringVarObject(
                    -1.0 * self.VelocityMaxLimit_PhidgetsUnits_FromDevice,
                    self.VelocityMaxLimit_PhidgetsUnits_FromDevice,
                    VelocityMaxLimit_PhidgetsUnits_UserSet_temp,
                    self.VelocityMaxLimit_PhidgetsUnits_StringVar)
                self.MyPrint_WithoutLogFile("VelocityMaxLimit_PhidgetsUnits_TextInputBoxResponse 'Return' event: \n" + str(
                    self.VelocityMaxLimit_PhidgetsUnits_UserSet))

                self.Velocity_PhidgetsUnits_TO_BE_SET = self.VelocityMaxLimit_PhidgetsUnits_UserSet
                self.Velocity_PhidgetsUnits_NeedsToBeChangedFlag = 1
        except:
            pass

    ##########################################################################################################
    ##########################################################################################################
    '''

    ##########################################################################################################
    ##########################################################################################################
    def GUI_update_clock(self):

        #######################################################
        #######################################################
        #######################################################
        #######################################################
        if self.USE_GUI_FLAG == 1 and self.EXIT_PROGRAM_FLAG == 0:

            #######################################################
            #######################################################
            #######################################################
            if self.GUI_ready_to_be_updated_flag == 1:

                #######################################################
                #######################################################
                try:
                    #########################################################
                    self.EngagedStateButton["text"] = "Engaged: " + str(self.EngagedState_PhidgetsUnits_FromDevice)
                    if self.EngagedState_PhidgetsUnits_FromDevice == 0:
                        self.EngagedStateButton["bg"] = self.TKinter_LightRedColor
                    elif self.EngagedState_PhidgetsUnits_FromDevice == 1:
                        self.EngagedStateButton["bg"] = self.TKinter_LightGreenColor
                    else:
                        self.EngagedStateButton["bg"] = self.TKinter_DefaultGrayColor
                    #########################################################

                    #########################################################
                    if self.ControlMode == "position":
                        if self.EngagedState_PhidgetsUnits_FromDevice == 1:
                            self.Position_PhidgetsUnits_Scale["troughcolor"] = self.TKinter_LightGreenColor
                            self.Acceleration_PhidgetsUnits_Scale["troughcolor"] = self.TKinter_LightGreenColor
                            self.DeadBand_PosControl_PhidgetsUnits_Scale["troughcolor"] = self.TKinter_LightGreenColor
                        else:
                            self.Position_PhidgetsUnits_Scale["troughcolor"] = self.TKinter_LightRedColor
                            self.Acceleration_PhidgetsUnits_Scale["troughcolor"] = self.TKinter_LightRedColor
                            self.DeadBand_PosControl_PhidgetsUnits_Scale["troughcolor"] = self.TKinter_LightRedColor
                    #########################################################

                    #########################################################
                    if self.Position_PhidgetsUnits_GUI_NeedsToBeChangedFlag == 1:
                        self.Position_PhidgetsUnits_Scale.set(self.Position_PhidgetsUnits_TO_BE_SET)
                        self.Position_PhidgetsUnits_GUI_NeedsToBeChangedFlag = 0
                    #########################################################

                    #########################################################
                    if self.Velocity_PhidgetsUnits_GUI_NeedsToBeChangedFlag == 1:
                        self.Velocity_PhidgetsUnits_Scale.set(self.Velocity_PhidgetsUnits_TO_BE_SET)
                        self.Velocity_PhidgetsUnits_GUI_NeedsToBeChangedFlag = 0
                    #########################################################
                    
                    #########################################################
                    if self.Acceleration_PhidgetsUnits_GUI_NeedsToBeChangedFlag == 1:
                        self.Acceleration_PhidgetsUnits_Scale.set(self.Acceleration_PhidgetsUnits_TO_BE_SET)
                        self.Acceleration_PhidgetsUnits_GUI_NeedsToBeChangedFlag = 0
                    #########################################################

                    #########################################################
                    if self.DeadBand_PosControl_PhidgetsUnits_GUI_NeedsToBeChangedFlag == 1:
                        self.DeadBand_PosControl_PhidgetsUnits_Scale.set(self.DeadBand_PosControl_PhidgetsUnits_TO_BE_SET)
                        self.DeadBand_PosControl_PhidgetsUnits_GUI_NeedsToBeChangedFlag = 0
                    #########################################################

                    #######################################################
                    self.data_label["text"] =  "*** ControlMode: " + self.ControlMode + " ***" +\
                                                "\nTime: " + self.ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(self.CurrentTime_CalculatedFromMainThread, 0, 3) + \
                                               "\nFrequency MainThread(Hz): " + self.ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(self.DataStreamingFrequency_CalculatedFromMainThread, 0, 3) + \
                                                "\nFrequency Phidgets ON CHANGE Position Rx, can slow to 0 (Hz): " + self.ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(self.DataStreamingFrequency_OnPositionChangeCallbackFunction, 0, 3) + \
                                                "\nTemperature_DegC_FromDevice: " + self.ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(self.Temperature_DegC_FromDevice, 0, 3) + \
                                                "\nPosition_PhidgetsUnits_FromDevice: " + self.ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(self.Position_PhidgetsUnits_FromDevice, 0, 3) + \
                                                "\nVelocity_PhidgetsUnits_FromDevice: " + self.ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(self.Velocity_PhidgetsUnits_FromDevice, 0, 3) + \
                                                "\nVelocityStall_PhidgetsUnits_FromDevice: " + self.ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(self.VelocityStall_PhidgetsUnits_FromDevice, 0, 3) + \
                                                "\nDutyCycle_PhidgetsUnits_FromDevice: " + self.ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(self.DutyCycle_PhidgetsUnits_FromDevice, 0, 3) + \
                                                "\nAcceleration_PhidgetsUnits_FromDevice: " + self.ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(self.Acceleration_PhidgetsUnits_FromDevice, 0, 3) + \
                                                "\nDeadBand_PosControl_PhidgetsUnits_FromDevice: " + self.ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(self.DeadBand_PosControl_PhidgetsUnits_FromDevice, 0, 3) + \
                                                "\nEngagedState_PhidgetsUnits_FromDevice: " + self.ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(self.EngagedState_PhidgetsUnits_FromDevice, 0, 3)
                                                #"\n***Position_PhidgetsUnits_TO_BE_SET: " + str(self.Position_PhidgetsUnits_TO_BE_SET)
                    #######################################################

                    #######################################################
                    self.PrintToGui_Label.config(text=self.PrintToGui_Label_TextInput_Str)
                    #######################################################

                except:
                    exceptions = sys.exc_info()[0]
                    print("PhidgetBrushlessDCmotorDCC1100controller_ReubenPython2and3Class GUI_update_clock ERROR: Exceptions: %s" % exceptions)
                    traceback.print_exc()
                #######################################################
                #######################################################

                #######################################################
                #######################################################
                if self.RootIsOwnedExternallyFlag == 0:  # This class object owns root and must handle it properly
                    self.root.after(self.GUI_RootAfterCallbackInterval_Milliseconds, self.GUI_update_clock)
                #######################################################
                #######################################################

            #######################################################
            #######################################################
            #######################################################

        #######################################################
        #######################################################
        #######################################################
        #######################################################

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def IsInputList(self, input, print_result_flag = 0):

        result = isinstance(input, list)

        if print_result_flag == 1:
            self.MyPrint_WithoutLogFile("IsInputList: " + str(result))

        return result
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(self, input, number_of_leading_numbers=4, number_of_decimal_places=3):
        IsListFlag = self.IsInputList(input)

        if IsListFlag == 0:
            float_number_list = [input]
        else:
            float_number_list = list(input)

        float_number_list_as_strings = []
        for element in float_number_list:
            try:
                element = float(element)
                prefix_string = "{:." + str(number_of_decimal_places) + "f}"
                element_as_string = prefix_string.format(element)
                float_number_list_as_strings.append(element_as_string)
            except:
                self.MyPrint_WithoutLogFile(self.TellWhichFileWereIn() + ": ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput ERROR: " + str(element) + " cannot be turned into a float")
                return -1

        StringToReturn = ""
        if IsListFlag == 0:
            StringToReturn = float_number_list_as_strings[0].zfill(number_of_leading_numbers + number_of_decimal_places + 1 + 1)  # +1 for sign, +1 for decimal place
        else:
            StringToReturn = "["
            for index, StringElement in enumerate(float_number_list_as_strings):
                if float_number_list[index] >= 0:
                    StringElement = "+" + StringElement  # So that our strings always have either + or - signs to maintain the same string length

                StringElement = StringElement.zfill(number_of_leading_numbers + number_of_decimal_places + 1 + 1)  # +1 for sign, +1 for decimal place

                if index != len(float_number_list_as_strings) - 1:
                    StringToReturn = StringToReturn + StringElement + ", "
                else:
                    StringToReturn = StringToReturn + StringElement + "]"

        return StringToReturn
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def limitNumber(self, min_val, max_val, test_val):

        #test_val = float(test_val) #MUST HAVE THIS LINE TO CATCH STRINGS PASSED INTO THE FUNCTION

        if test_val > max_val:
            test_val = max_val
            #self.MyPrint_WithoutLogFile("limitNumber: input of " + str(test_val) + " was capped at maximum of " + str(max_val) + ".")
        elif test_val < min_val:
            test_val = min_val
            #self.MyPrint_WithoutLogFile("limitNumber: input of " + str(test_val) + " was capped at minimum of " + str(min_val) + ".")
        else:
            dummy_var = 0
            #self.MyPrint_WithoutLogFile("limitNumber ERROR: input of " + str(test_val) + " triggered the 'else' condition.")

        return test_val
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def LimitNumber_StringVarObject(self, min_val, max_val, test_val, StringVarObject, number_of_decimal_places = 1):

        try:
            test_val = float(test_val)

            if test_val > max_val:
                test_val = max_val
                #self.MyPrint_WithoutLogFile("Original input of " + str(test_val) + " capped at a maximum of " + str(max_val))
            elif test_val < min_val:
                test_val = min_val
                #self.MyPrint_WithoutLogFile("Original input of " + str(test_val) + " capped at a minimum of " + str(min_val))
            else:
                test_val = test_val
                #self.MyPrint_WithoutLogFile("Original input of " + str(test_val) + " not capped at a minimum of " + str(min_val) + " or maximum of " + str(max_val))

            prefix_string = "{:." + str(number_of_decimal_places) + "f}"
            string_to_set = prefix_string.format(test_val)
            StringVarObject.set(str(string_to_set))  # Reset the text, overwriting the bad value that was entered.

            return test_val
        except:
            exceptions = sys.exc_info()[0]
            self.MyPrint_WithoutLogFile("LimitNumber_StringVarObject ERROR: Exceptions: %s" % exceptions)
            return -1111111111
    ##########################################################################################################
    ##########################################################################################################
        
    ##########################################################################################################
    ##########################################################################################################
    def MyPrint_WithoutLogFile(self, input_string):

        input_string = str(input_string)

        if input_string != "":

            #input_string = input_string.replace("\n", "").replace("\r", "")

            ################################ Write to console
            # Some people said that print crashed for pyinstaller-built-applications and that sys.stdout.write fixed this.
            # http://stackoverflow.com/questions/13429924/pyinstaller-packaged-application-works-fine-in-console-mode-crashes-in-window-m
            if self.PrintToConsoleFlag == 1:
                sys.stdout.write(input_string + "\n")
            ################################

            ################################ Write to GUI
            self.PrintToGui_Label_TextInputHistory_List.append(self.PrintToGui_Label_TextInputHistory_List.pop(0)) #Shift the list
            self.PrintToGui_Label_TextInputHistory_List[-1] = str(input_string) #Add the latest value

            self.PrintToGui_Label_TextInput_Str = ""
            for Counter, Line in enumerate(self.PrintToGui_Label_TextInputHistory_List):
                self.PrintToGui_Label_TextInput_Str = self.PrintToGui_Label_TextInput_Str + Line

                if Counter < len(self.PrintToGui_Label_TextInputHistory_List) - 1:
                    self.PrintToGui_Label_TextInput_Str = self.PrintToGui_Label_TextInput_Str + "\n"
            ################################

    ##########################################################################################################
    ##########################################################################################################



