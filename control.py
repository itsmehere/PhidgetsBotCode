# -*- coding: utf-8 -*-

'''
Reuben Brewer, Ph.D.
reuben.brewer@gmail.com,
www.reubotics.com

Apache 2 License
Software Revision D, 11/12/2021

Verified working on: Python 2.7, 3.8 for Windows 8.1, 10 64-bit and Raspberry Pi Buster (no Mac testing yet).
'''

__author__ = 'reuben.brewer'

from PhidgetBrushlessDCmotorDCC1100controller_ReubenPython2and3Class import *
from MyPrint_ReubenPython2and3Class import *
import keyboard

import os, sys, platform
import time, datetime
import threading
import collections

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
    from builtins import raw_input as input
else:
    from future.builtins import input as input #"sudo pip3 install future" (Python 3) AND "sudo pip install future" (Python 2)
###############

##########################################################################################################
##########################################################################################################
def getPreciseSecondsTimeStampString():
    ts = time.time()

    return ts
##########################################################################################################
##########################################################################################################

##########################################################################################################
##########################################################################################################
def TestButtonResponse():
    global MyPrint_ReubenPython2and3ClassObject
    global USE_MYPRINT_FLAG

    if USE_MYPRINT_FLAG == 1:
        MyPrint_ReubenPython2and3ClassObject.my_print("Test Button was Pressed!")
    else:
        print("Test Button was Pressed!")
##########################################################################################################
##########################################################################################################

##########################################################################################################
##########################################################################################################
def GUI_update_clock():
    global root
    global EXIT_PROGRAM_FLAG
    global GUI_RootAfterCallbackInterval_Milliseconds
    global USE_GUI_FLAG

    global PhidgetBrushlessDCmotorDCC1100controller_ReubenPython2and3ClassObject_Left1
    global BLDC_OPEN_FLAG_Left1
    global SHOW_IN_GUI_BLDC_FLAG_Left1

    global PhidgetBrushlessDCmotorDCC1100controller_ReubenPython2and3ClassObject_Right0
    global BLDC_OPEN_FLAG_Right0
    global SHOW_IN_GUI_BLDC_FLAG_Right0

    global MyPrint_ReubenPython2and3ClassObject
    global MYPRINT_OPEN_FLAG
    global SHOW_IN_GUI_MYPRINT_FLAG

    if USE_GUI_FLAG == 1:
        if EXIT_PROGRAM_FLAG == 0:
        #########################################################
        #########################################################

            #########################################################
            if BLDC_OPEN_FLAG_Left1 == 1 and SHOW_IN_GUI_BLDC_FLAG_Left1 == 1:
                PhidgetBrushlessDCmotorDCC1100controller_ReubenPython2and3ClassObject_Left1.GUI_update_clock()
            #########################################################

            #########################################################
            if BLDC_OPEN_FLAG_Right0 == 1 and SHOW_IN_GUI_BLDC_FLAG_Right0 == 1:
                PhidgetBrushlessDCmotorDCC1100controller_ReubenPython2and3ClassObject_Right0.GUI_update_clock()
            #########################################################

            #########################################################
            if MYPRINT_OPEN_FLAG == 1 and SHOW_IN_GUI_MYPRINT_FLAG == 1:
                MyPrint_ReubenPython2and3ClassObject.GUI_update_clock()
            #########################################################

            root.after(GUI_RootAfterCallbackInterval_Milliseconds, GUI_update_clock)
        #########################################################
        #########################################################

##########################################################################################################
##########################################################################################################

##########################################################################################################
##########################################################################################################
def ExitProgram_Callback():
    global root
    global EXIT_PROGRAM_FLAG
    global GUI_RootAfterCallbackInterval_Milliseconds

    global PhidgetBrushlessDCmotorDCC1100controller_ReubenPython2and3ClassObject_Left1
    global BLDC_OPEN_FLAG_Left1

    global PhidgetBrushlessDCmotorDCC1100controller_ReubenPython2and3ClassObject_Right0
    global BLDC_OPEN_FLAG_Right0

    global MyPrint_ReubenPython2and3ClassObject
    global MYPRINT_OPEN_FLAG

    print("Exiting all threads in test_program_for_MyPrint_ReubenPython2and3Class.")

    EXIT_PROGRAM_FLAG = 1

    #########################################################
    if BLDC_OPEN_FLAG_Left1 == 1:
        PhidgetBrushlessDCmotorDCC1100controller_ReubenPython2and3ClassObject_Left1.ExitProgram_Callback()
    #########################################################

    #########################################################
    if BLDC_OPEN_FLAG_Right0 == 1:
        PhidgetBrushlessDCmotorDCC1100controller_ReubenPython2and3ClassObject_Right0.ExitProgram_Callback()
    #########################################################

    #########################################################
    if MYPRINT_OPEN_FLAG == 1:
        MyPrint_ReubenPython2and3ClassObject.ExitProgram_Callback()
    #########################################################

##########################################################################################################
##########################################################################################################

##########################################################################################################
##########################################################################################################
def GUI_Thread():
    global root
    global GUI_RootAfterCallbackInterval_Milliseconds

    ################################################# KEY GUI LINE
    #################################################
    root = Tk()
    #################################################
    #################################################

    #################################################
    TestButton = Button(root, text='Test Button', state="normal", width=20, command=lambda i=1: TestButtonResponse())
    TestButton.grid(row=0, column=0, padx=5, pady=1)
    #################################################

    #################################################
    root.protocol("WM_DELETE_WINDOW", ExitProgram_Callback)  # Set the callback function for when the window's closed.
    root.after(GUI_RootAfterCallbackInterval_Milliseconds, GUI_update_clock)
    root.mainloop()
    #################################################

    #################################################
    root.quit() #Stop the GUI thread, MUST BE CALLED FROM GUI_Thread
    root.destroy() #Close down the GUI thread, MUST BE CALLED FROM GUI_Thread
    #################################################

##########################################################################################################
##########################################################################################################

##########################################################################################################
##########################################################################################################
if __name__ == '__main__':

    #################################################
    #################################################
    global my_platform

    if platform.system() == "Linux":

        if "raspberrypi" in platform.uname():  # os.uname() doesn't work in windows
            my_platform = "pi"
        else:
            my_platform = "linux"

    elif platform.system() == "Windows":
        my_platform = "windows"

    elif platform.system() == "Darwin":
        my_platform = "mac"

    else:
        my_platform = "other"

    print("The OS platform is: " + my_platform)
    #################################################
    #################################################

    #################################################
    #################################################
    global USE_GUI_FLAG
    USE_GUI_FLAG = 1

    # --- LEFT MOTOR ---

    global USE_BLDC_FLAG_Left1
    USE_BLDC_FLAG_Left1 = 1

    global USE_BLDC_POSITION_CONTROL_FLAG_Left1
    USE_BLDC_POSITION_CONTROL_FLAG_Left1 = 0 #SET TO 0 FOR VELOCITY CONTROL

    global USE_BLDC_SINUSOIDAL_INPUT_FLAG_Left1
    USE_BLDC_SINUSOIDAL_INPUT_FLAG_Left1 = 1

    # --- RIGHT MOTOR ---

    global USE_BLDC_FLAG_Right0
    USE_BLDC_FLAG_Right0 = 1

    global USE_BLDC_POSITION_CONTROL_FLAG_Right0
    USE_BLDC_POSITION_CONTROL_FLAG_Right0 = 0 #SET TO 0 FOR VELOCITY CONTROL

    global USE_BLDC_SINUSOIDAL_INPUT_FLAG_Right0
    USE_BLDC_SINUSOIDAL_INPUT_FLAG_Right0 = 1

    #################################################
    #################################################

    global USE_MYPRINT_FLAG
    USE_MYPRINT_FLAG = 1
    #################################################
    #################################################

    #################################################
    #################################################
    global SHOW_IN_GUI_BLDC_FLAG_Left1
    SHOW_IN_GUI_BLDC_FLAG_Left1 = 1

    global SHOW_IN_GUI_BLDC_FLAG_Right0
    SHOW_IN_GUI_BLDC_FLAG_Right0 = 1

    global SHOW_IN_GUI_MYPRINT_FLAG
    SHOW_IN_GUI_MYPRINT_FLAG = 1
    #################################################
    #################################################

    #################################################
    #################################################
    global GUI_ROW_BLDC_Left1
    global GUI_COLUMN_BLDC_Left1
    global GUI_PADX_BLDC_Left1
    global GUI_PADY_BLDC_Left1
    global GUI_ROWSPAN_BLDC_Left1
    global GUI_COLUMNSPAN_BLDC_Left1
    GUI_ROW_BLDC_Left1 = 1

    GUI_COLUMN_BLDC_Left1 = 0
    GUI_PADX_BLDC_Left1 = 1
    GUI_PADY_BLDC_Left1 = 10
    GUI_ROWSPAN_BLDC_Left1 = 1
    GUI_COLUMNSPAN_BLDC_Left1 = 1

    global GUI_ROW_BLDC_Right0
    global GUI_COLUMN_BLDC_Right0
    global GUI_PADX_BLDC_Right0
    global GUI_PADY_BLDC_Right0
    global GUI_ROWSPAN_BLDC_Right0
    global GUI_COLUMNSPAN_BLDC_Right0
    GUI_ROW_BLDC_Right0 = 1

    GUI_COLUMN_BLDC_Right0 = 0
    GUI_PADX_BLDC_Right0 = 1
    GUI_PADY_BLDC_Right0 = 10
    GUI_ROWSPAN_BLDC_Right0 = 1
    GUI_COLUMNSPAN_BLDC_Right0 = 1

    global GUI_ROW_MYPRINT
    global GUI_COLUMN_MYPRINT
    global GUI_PADX_MYPRINT
    global GUI_PADY_MYPRINT
    global GUI_ROWSPAN_MYPRINT
    global GUI_COLUMNSPAN_MYPRINT
    GUI_ROW_MYPRINT = 2

    GUI_COLUMN_MYPRINT = 0
    GUI_PADX_MYPRINT = 1
    GUI_PADY_MYPRINT = 10
    GUI_ROWSPAN_MYPRINT = 1
    GUI_COLUMNSPAN_MYPRINT = 1
    #################################################
    #################################################

    #################################################
    #################################################
    global EXIT_PROGRAM_FLAG
    EXIT_PROGRAM_FLAG = 0

    global root

    global GUI_RootAfterCallbackInterval_Milliseconds
    GUI_RootAfterCallbackInterval_Milliseconds = 30

    global PhidgetBrushlessDCmotorDCC1100controller_ReubenPython2and3ClassObject_Left1
    global BLDC_OPEN_FLAG_Left1
    BLDC_OPEN_FLAG_Left1 = -1

    global PhidgetBrushlessDCmotorDCC1100controller_ReubenPython2and3ClassObject_Right0
    global BLDC_OPEN_FLAG_Right0
    BLDC_OPEN_FLAG_Right0 = -1

    global MyPrint_ReubenPython2and3ClassObject

    global MYPRINT_OPEN_FLAG
    MYPRINT_OPEN_FLAG = -1

    global CurrentTime_MainLoopThread
    CurrentTime_MainLoopThread = -11111.0

    global StartingTime_MainLoopThread
    StartingTime_MainLoopThread = -11111.0

    # -------------------------- LEFT MOTOR --------------------------

    global SINUSOIDAL_MOTION_INPUT_ROMtestTimeToPeakAngle_Left1
    SINUSOIDAL_MOTION_INPUT_ROMtestTimeToPeakAngle_Left1 = 2.0

    global SINUSOIDAL_MOTION_INPUT_MinValue_PositionControl_Left1
    SINUSOIDAL_MOTION_INPUT_MinValue_PositionControl_Left1 = -50.0

    global SINUSOIDAL_MOTION_INPUT_MaxValue_PositionControl_Left1
    SINUSOIDAL_MOTION_INPUT_MaxValue_PositionControl_Left1 = 50.0
    
    global SINUSOIDAL_MOTION_INPUT_MinValue_VelocityControl_Left1
    SINUSOIDAL_MOTION_INPUT_MinValue_VelocityControl_Left1 = -0.1 # Was originally -1.0, changed to -0.1

    global SINUSOIDAL_MOTION_INPUT_MaxValue_VelocityControl_Left1
    SINUSOIDAL_MOTION_INPUT_MaxValue_VelocityControl_Left1 = 0.1 # Was originally 1.0, changed to 0.1

    # -------------------------- RIGHT MOTOR --------------------------

    global SINUSOIDAL_MOTION_INPUT_ROMtestTimeToPeakAngle_Right0
    SINUSOIDAL_MOTION_INPUT_ROMtestTimeToPeakAngle_Right0 = 2.0

    global SINUSOIDAL_MOTION_INPUT_MinValue_PositionControl_Right0
    SINUSOIDAL_MOTION_INPUT_MinValue_PositionControl_Right0 = -50.0

    global SINUSOIDAL_MOTION_INPUT_MaxValue_PositionControl_Right0
    SINUSOIDAL_MOTION_INPUT_MaxValue_PositionControl_Right0 = 50.0
    
    global SINUSOIDAL_MOTION_INPUT_MinValue_VelocityControl_Right0
    SINUSOIDAL_MOTION_INPUT_MinValue_VelocityControl_Right0 = -0.1 # Was originally -1.0, changed to -0.1

    global SINUSOIDAL_MOTION_INPUT_MaxValue_VelocityControl_Right0
    SINUSOIDAL_MOTION_INPUT_MaxValue_VelocityControl_Right0 = 0.1 # Was originally 1.0, changed to 0.1

    #################################################
    #################################################

    #################################################  KEY GUI LINE
    #################################################
    if USE_GUI_FLAG == 1:
        print("Starting GUI thread...")
        GUI_Thread_ThreadingObject = threading.Thread(target=GUI_Thread)
        GUI_Thread_ThreadingObject.setDaemon(True) #Should mean that the GUI thread is destroyed automatically when the main thread is destroyed.
        GUI_Thread_ThreadingObject.start()
        time.sleep(0.5)  #Allow enough time for 'root' to be created that we can then pass it into other classes.
    else:
        root = None
    #################################################
    #################################################

    #################################################
    #################################################
    #PositionInRev = PositionInPhidgetsUnits*(1.0/(NumberOfBLDCmotorPoles * 3.0)) * (1.0/GearRatio)

    # -------------------------- LEFT MOTOR --------------------------

    global BLDC_MostRecentDict_Left1

    global BLDC_MostRecentDict_Position_PhidgetsUnits_FromDevice_Left1
    BLDC_MostRecentDict_Position_PhidgetsUnits_FromDevice_Left1 = -11111

    global BLDC_MostRecentDict_Velocity_PhidgetsUnits_FromDevice_Left1
    BLDC_MostRecentDict_Velocity_PhidgetsUnits_FromDevice_Left1 = -11111

    global BLDC_MostRecentDict_Velocity_PhidgetsUnits_DifferentiatedRaw_Left1
    BLDC_MostRecentDict_Velocity_PhidgetsUnits_DifferentiatedRaw_Left1 = -11111

    global BLDC_MostRecentDict_Velocity_PhidgetsUnits_DifferentiatedSmoothed_Left1
    BLDC_MostRecentDict_Velocity_PhidgetsUnits_DifferentiatedSmoothed_Left1 = -11111

    global BLDC_MostRecentDict_DutyCycle_PhidgetsUnits_FromDevice_Left1
    BLDC_MostRecentDict_DutyCycle_PhidgetsUnits_FromDevice_Left1 = -11111

    global BLDC_MostRecentDict_Temperature_DegC_FromDevice_Left1
    BLDC_MostRecentDict_Temperature_DegC_FromDevice_Left1 = -11111

    global BLDC_MostRecentDict_Time_Left1
    BLDC_MostRecentDict_Time_Left1 = -11111

    # -------------------------- RIGHT MOTOR --------------------------

    global BLDC_MostRecentDict_Right0

    global BLDC_MostRecentDict_Position_PhidgetsUnits_FromDevice_Right0
    BLDC_MostRecentDict_Position_PhidgetsUnits_FromDevice_Right0 = -11111

    global BLDC_MostRecentDict_Velocity_PhidgetsUnits_FromDevice_Right0
    BLDC_MostRecentDict_Velocity_PhidgetsUnits_FromDevice_Right0 = -11111

    global BLDC_MostRecentDict_Velocity_PhidgetsUnits_DifferentiatedRaw_Right0
    BLDC_MostRecentDict_Velocity_PhidgetsUnits_DifferentiatedRaw_Right0 = -11111

    global BLDC_MostRecentDict_Velocity_PhidgetsUnits_DifferentiatedSmoothed_Right0
    BLDC_MostRecentDict_Velocity_PhidgetsUnits_DifferentiatedSmoothed_Right0 = -11111

    global BLDC_MostRecentDict_DutyCycle_PhidgetsUnits_FromDevice_Right0
    BLDC_MostRecentDict_DutyCycle_PhidgetsUnits_FromDevice_Right0 = -11111

    global BLDC_MostRecentDict_Temperature_DegC_FromDevice_Right0
    BLDC_MostRecentDict_Temperature_DegC_FromDevice__Right0 = -11111

    global BLDC_MostRecentDict_Time_Right0
    BLDC_MostRecentDict_Time_Right0 = -11111

    #################################################
    BLDC_GUIparametersDict_Left1 = dict([("USE_GUI_FLAG", USE_GUI_FLAG and SHOW_IN_GUI_BLDC_FLAG_Left1),
                                    ("root", root),
                                    ("EnableInternal_MyPrint_Flag", 1),
                                    ("NumberOfPrintLines", 10),
                                    ("UseBorderAroundThisGuiObjectFlag", 0),
                                    ("GUI_ROW", GUI_ROW_BLDC_Left1),
                                    ("GUI_COLUMN", GUI_COLUMN_BLDC_Left1),
                                    ("GUI_PADX", GUI_PADX_BLDC_Left1),
                                    ("GUI_PADY", GUI_PADY_BLDC_Left1),
                                    ("GUI_ROWSPAN", GUI_ROWSPAN_BLDC_Left1),
                                    ("GUI_COLUMNSPAN", GUI_COLUMNSPAN_BLDC_Left1)])
    #################################################

    #################################################
    global BLDC_setup_dict_PositionControl_Left1
    BLDC_setup_dict_PositionControl_Left1 = dict([("GUIparametersDict", BLDC_GUIparametersDict_Left1),
                            ("UsePhidgetsLoggingInternalToThisClassObjectFlag", 1),
                            ("WaitForAttached_TimeoutDuration_Milliseconds", 5000),
                            ("user_set_name", "Reuben's Test BLDC Controller"),
                            ("VINT_DesiredSerialNumber", 634222), #CHANGE THIS TO MATCH YOUR UNIQUE VINT
                            ("VINT_DesiredPortNumber", 1), #CHANGE THIS TO MATCH YOUR UNIQUE VINT
                            ("DesiredDeviceID", 108),
                            ("NameToDisplay_UserSet", "Reuben's Test BLDC Controller"),
                            ("ENABLE_GETS_MAINTHREAD", 0),
                            ("FailsafeTime_Milliseconds", 10000),
                            ("MainThread_TimeToSleepEachLoop", 0.001),
                            ("ControlMode", "position"),  #position or velocity, AFTER SWITCHING ControlMode, YOU SOMETIMES NEED TO RUN PYTHON FILE ONCE AND THEN POWER-CYCLE BOARD FOR EFFECT TO TAKE
                            ("VelocityMinLimit_PhidgetsUnits_UserSet", 0.0),
                            ("VelocityMaxLimit_PhidgetsUnits_UserSet", 10000.0),
                            ("VelocityStallLimit_PhidgetsUnits_UserSet", 15.0),  #Setting StallVelocity to 0 will turn off stall protection functionality
                            ("BrakingStrengthLimit_VelControl_Percent_UserSet", 100.0),
                            ("AccelerationMaxLimit_PhidgetsUnits_UserSet", 100000.0),
                            ("PositionMinLimit_PhidgetsUnits_UserSet", -1000.0),
                            ("PositionMaxLimit_PhidgetsUnits_UserSet", 1000.0),
                            ("Kp_PosControl_Gain_UserSet", 20000.0),  #IF MOTOR-CONTROL FAILS, THEN TRY ALL-NEGATIVE-GAIN-VALUES (Kp, Ki, and KD)!
                            ("Ki_PosControl_Gain_UserSet", 2.0),  #IF MOTOR-CONTROL FAILS, THEN TRY ALL-NEGATIVE-GAIN-VALUES (Kp, Ki, and KD)!
                            ("Kd_PosControl_Gain_UserSet", 40000.0),  #IF MOTOR-CONTROL FAILS, THEN TRY ALL-NEGATIVE-GAIN-VALUES (Kp, Ki, and KD)!
                            ("DeadBand_PosControl_PhidgetsUnits_UserSet", 10.0),  #Lower DeadBand value is a tighter Position loop (allows less error)
                            ("RescaleFactor_MultipliesPhidgetsUnits_UserSet", 1.0),
                            ("UpdateDeltaT_ms", 20)]) #100 min for velocity, 20 min for position
    #################################################

    #################################################
    global BLDC_setup_dict_VelocityControl_Left1
    BLDC_setup_dict_VelocityControl_Left1 = dict([("GUIparametersDict", BLDC_GUIparametersDict_Left1),
                            ("UsePhidgetsLoggingInternalToThisClassObjectFlag", 1),
                            ("WaitForAttached_TimeoutDuration_Milliseconds", 5000),
                            ("user_set_name", "Reuben's Test BLDC Controller"),
                            ("VINT_DesiredSerialNumber", 634222), #CHANGE THIS TO MATCH YOUR UNIQUE VINT
                            ("VINT_DesiredPortNumber", 1), #CHANGE THIS TO MATCH YOUR UNIQUE VINT
                            ("DesiredDeviceID", 108),
                            ("NameToDisplay_UserSet", "Reuben's Test BLDC Controller"),
                            ("ENABLE_GETS_MAINTHREAD", 1),
                            ("FailsafeTime_Milliseconds", 10000),
                            ("MainThread_TimeToSleepEachLoop", 0.001),
                            ("ControlMode", "velocity"),  #position or velocity, AFTER SWITCHING ControlMode, MUST RUN PYTHON FILE ONCE AND THEN POWER-CYCLE BOARD FOR EFFECT TO TAKE
                            ("VelocityMinLimit_PhidgetsUnits_UserSet", -1.0),
                            ("VelocityMaxLimit_PhidgetsUnits_UserSet", 1.0),
                            ("VelocityStallLimit_PhidgetsUnits_UserSet", 15.0),  #Setting StallVelocity to 0 will turn off stall protection functionality
                            ("BrakingStrengthLimit_VelControl_Percent_UserSet", 100.0),
                            ("AccelerationMaxLimit_PhidgetsUnits_UserSet", 100.0),
                            ("PositionMinLimit_PhidgetsUnits_UserSet", -1000.0),
                            ("PositionMaxLimit_PhidgetsUnits_UserSet", 1000.0),
                            ("Kp_PosControl_Gain_UserSet", 20000.0),  #IF MOTOR-CONTROL FAILS, THEN TRY ALL-NEGATIVE-GAIN-VALUES (Kp, Ki, and KD)!
                            ("Ki_PosControl_Gain_UserSet", 2.0),  #IF MOTOR-CONTROL FAILS, THEN TRY ALL-NEGATIVE-GAIN-VALUES (Kp, Ki, and KD)!
                            ("Kd_PosControl_Gain_UserSet", 40000.0),  #IF MOTOR-CONTROL FAILS, THEN TRY ALL-NEGATIVE-GAIN-VALUES (Kp, Ki, and KD)!
                            ("DeadBand_PosControl_PhidgetsUnits_UserSet", 10.0),  #Lower DeadBand value is a tighter Position loop (allows less error)
                            ("RescaleFactor_MultipliesPhidgetsUnits_UserSet", 1.0),
                            ("UpdateDeltaT_ms", 100)]) #100 min for velocity, 20 min for position
    #################################################

    #################################################
    BLDC_GUIparametersDict_Right0 = dict([("USE_GUI_FLAG", USE_GUI_FLAG and SHOW_IN_GUI_BLDC_FLAG_Right0),
                                    ("root", root),
                                    ("EnableInternal_MyPrint_Flag", 1),
                                    ("NumberOfPrintLines", 10),
                                    ("UseBorderAroundThisGuiObjectFlag", 0),
                                    ("GUI_ROW", GUI_ROW_BLDC_Right0),
                                    ("GUI_COLUMN", GUI_COLUMN_BLDC_Right0),
                                    ("GUI_PADX", GUI_PADX_BLDC_Right0),
                                    ("GUI_PADY", GUI_PADY_BLDC_Right0),
                                    ("GUI_ROWSPAN", GUI_ROWSPAN_BLDC_Right0),
                                    ("GUI_COLUMNSPAN", GUI_COLUMNSPAN_BLDC_Right0)])
    #################################################

    #################################################
    global BLDC_setup_dict_PositionControl_Right0
    BLDC_setup_dict_PositionControl_Right0 = dict([("GUIparametersDict", BLDC_GUIparametersDict_Right0),
                            ("UsePhidgetsLoggingInternalToThisClassObjectFlag", 1),
                            ("WaitForAttached_TimeoutDuration_Milliseconds", 5000),
                            ("user_set_name", "Reuben's Test BLDC Controller"),
                            ("VINT_DesiredSerialNumber", 634222), #CHANGE THIS TO MATCH YOUR UNIQUE VINT
                            ("VINT_DesiredPortNumber", 0), #CHANGE THIS TO MATCH YOUR UNIQUE VINT
                            ("DesiredDeviceID", 108),
                            ("NameToDisplay_UserSet", "Reuben's Test BLDC Controller"),
                            ("ENABLE_GETS_MAINTHREAD", 0),
                            ("FailsafeTime_Milliseconds", 10000),
                            ("MainThread_TimeToSleepEachLoop", 0.001),
                            ("ControlMode", "position"),  #position or velocity, AFTER SWITCHING ControlMode, YOU SOMETIMES NEED TO RUN PYTHON FILE ONCE AND THEN POWER-CYCLE BOARD FOR EFFECT TO TAKE
                            ("VelocityMinLimit_PhidgetsUnits_UserSet", 0.0),
                            ("VelocityMaxLimit_PhidgetsUnits_UserSet", 10000.0),
                            ("VelocityStallLimit_PhidgetsUnits_UserSet", 15.0),  #Setting StallVelocity to 0 will turn off stall protection functionality
                            ("BrakingStrengthLimit_VelControl_Percent_UserSet", 100.0),
                            ("AccelerationMaxLimit_PhidgetsUnits_UserSet", 100000.0),
                            ("PositionMinLimit_PhidgetsUnits_UserSet", -1000.0),
                            ("PositionMaxLimit_PhidgetsUnits_UserSet", 1000.0),
                            ("Kp_PosControl_Gain_UserSet", 20000.0),  #IF MOTOR-CONTROL FAILS, THEN TRY ALL-NEGATIVE-GAIN-VALUES (Kp, Ki, and KD)!
                            ("Ki_PosControl_Gain_UserSet", 2.0),  #IF MOTOR-CONTROL FAILS, THEN TRY ALL-NEGATIVE-GAIN-VALUES (Kp, Ki, and KD)!
                            ("Kd_PosControl_Gain_UserSet", 40000.0),  #IF MOTOR-CONTROL FAILS, THEN TRY ALL-NEGATIVE-GAIN-VALUES (Kp, Ki, and KD)!
                            ("DeadBand_PosControl_PhidgetsUnits_UserSet", 10.0),  #Lower DeadBand value is a tighter Position loop (allows less error)
                            ("RescaleFactor_MultipliesPhidgetsUnits_UserSet", 1.0),
                            ("UpdateDeltaT_ms", 20)]) #100 min for velocity, 20 min for position
    #################################################

    #################################################
    global BLDC_setup_dict_VelocityControl_Right0
    BLDC_setup_dict_VelocityControl_Right0 = dict([("GUIparametersDict", BLDC_GUIparametersDict_Right0),
                            ("UsePhidgetsLoggingInternalToThisClassObjectFlag", 1),
                            ("WaitForAttached_TimeoutDuration_Milliseconds", 5000),
                            ("user_set_name", "Reuben's Test BLDC Controller"),
                            ("VINT_DesiredSerialNumber", 634222), #CHANGE THIS TO MATCH YOUR UNIQUE VINT
                            ("VINT_DesiredPortNumber", 0), #CHANGE THIS TO MATCH YOUR UNIQUE VINT
                            ("DesiredDeviceID", 108),
                            ("NameToDisplay_UserSet", "Reuben's Test BLDC Controller"),
                            ("ENABLE_GETS_MAINTHREAD", 1),
                            ("FailsafeTime_Milliseconds", 10000),
                            ("MainThread_TimeToSleepEachLoop", 0.001),
                            ("ControlMode", "velocity"),  #position or velocity, AFTER SWITCHING ControlMode, MUST RUN PYTHON FILE ONCE AND THEN POWER-CYCLE BOARD FOR EFFECT TO TAKE
                            ("VelocityMinLimit_PhidgetsUnits_UserSet", -1.0),
                            ("VelocityMaxLimit_PhidgetsUnits_UserSet", 1.0),
                            ("VelocityStallLimit_PhidgetsUnits_UserSet", 15.0),  #Setting StallVelocity to 0 will turn off stall protection functionality
                            ("BrakingStrengthLimit_VelControl_Percent_UserSet", 100.0),
                            ("AccelerationMaxLimit_PhidgetsUnits_UserSet", 100.0),
                            ("PositionMinLimit_PhidgetsUnits_UserSet", -1000.0),
                            ("PositionMaxLimit_PhidgetsUnits_UserSet", 1000.0),
                            ("Kp_PosControl_Gain_UserSet", 20000.0),  #IF MOTOR-CONTROL FAILS, THEN TRY ALL-NEGATIVE-GAIN-VALUES (Kp, Ki, and KD)!
                            ("Ki_PosControl_Gain_UserSet", 2.0),  #IF MOTOR-CONTROL FAILS, THEN TRY ALL-NEGATIVE-GAIN-VALUES (Kp, Ki, and KD)!
                            ("Kd_PosControl_Gain_UserSet", 40000.0),  #IF MOTOR-CONTROL FAILS, THEN TRY ALL-NEGATIVE-GAIN-VALUES (Kp, Ki, and KD)!
                            ("DeadBand_PosControl_PhidgetsUnits_UserSet", 10.0),  #Lower DeadBand value is a tighter Position loop (allows less error)
                            ("RescaleFactor_MultipliesPhidgetsUnits_UserSet", 1.0),
                            ("UpdateDeltaT_ms", 100)]) #100 min for velocity, 20 min for position
    #################################################

    if USE_BLDC_FLAG_Left1 == 1:
        try:

            if USE_BLDC_POSITION_CONTROL_FLAG_Left1 == 1:
                PhidgetBrushlessDCmotorDCC1100controller_ReubenPython2and3ClassObject_Left1 = PhidgetBrushlessDCmotorDCC1100controller_ReubenPython2and3Class(BLDC_setup_dict_PositionControl_Left1)

            else:
                PhidgetBrushlessDCmotorDCC1100controller_ReubenPython2and3ClassObject_Left1 = PhidgetBrushlessDCmotorDCC1100controller_ReubenPython2and3Class(BLDC_setup_dict_VelocityControl_Left1)

            time.sleep(0.25)
            BLDC_OPEN_FLAG_Left1 = PhidgetBrushlessDCmotorDCC1100controller_ReubenPython2and3ClassObject_Left1.OBJECT_CREATED_SUCCESSFULLY_FLAG

        except:
            exceptions = sys.exc_info()[0]
            print("PhidgetBrushlessDCmotorDCC1100controller_ReubenPython2and3ClassObject __init__: Exceptions: %s" % exceptions, 0)
            traceback.print_exc()

    if USE_BLDC_FLAG_Right0 == 1:
        try:

            if USE_BLDC_POSITION_CONTROL_FLAG_Right0 == 1:
                PhidgetBrushlessDCmotorDCC1100controller_ReubenPython2and3ClassObject_Right0 = PhidgetBrushlessDCmotorDCC1100controller_ReubenPython2and3Class(BLDC_setup_dict_PositionControl_Right0)

            else:
                PhidgetBrushlessDCmotorDCC1100controller_ReubenPython2and3ClassObject_Right0 = PhidgetBrushlessDCmotorDCC1100controller_ReubenPython2and3Class(BLDC_setup_dict_VelocityControl_Right0)

            time.sleep(0.25)
            BLDC_OPEN_FLAG_Right0 = PhidgetBrushlessDCmotorDCC1100controller_ReubenPython2and3ClassObject_Right0.OBJECT_CREATED_SUCCESSFULLY_FLAG

        except:
            exceptions = sys.exc_info()[0]
            print("PhidgetBrushlessDCmotorDCC1100controller_ReubenPython2and3ClassObject __init__: Exceptions: %s" % exceptions, 0)
            traceback.print_exc()
    #################################################
    #################################################

    #################################################
    #################################################
    if USE_MYPRINT_FLAG == 1:

        MyPrint_ReubenPython2and3ClassObject_GUIparametersDict = dict([("USE_GUI_FLAG", USE_GUI_FLAG and SHOW_IN_GUI_MYPRINT_FLAG),
                                                                        ("root", root),
                                                                        ("UseBorderAroundThisGuiObjectFlag", 0),
                                                                        ("GUI_ROW", GUI_ROW_MYPRINT),
                                                                        ("GUI_COLUMN", GUI_COLUMN_MYPRINT),
                                                                        ("GUI_PADX", GUI_PADX_MYPRINT),
                                                                        ("GUI_PADY", GUI_PADY_MYPRINT),
                                                                        ("GUI_ROWSPAN", GUI_ROWSPAN_MYPRINT),
                                                                        ("GUI_COLUMNSPAN", GUI_COLUMNSPAN_MYPRINT)])

        MyPrint_ReubenPython2and3ClassObject_setup_dict = dict([("NumberOfPrintLines", 10),
                                                                ("WidthOfPrintingLabel", 200),
                                                                ("PrintToConsoleFlag", 1),
                                                                ("LogFileNameFullPath", os.getcwd() + "//TestLog.txt"),
                                                                ("GUIparametersDict", MyPrint_ReubenPython2and3ClassObject_GUIparametersDict)])

        try:
            MyPrint_ReubenPython2and3ClassObject = MyPrint_ReubenPython2and3Class(MyPrint_ReubenPython2and3ClassObject_setup_dict)
            time.sleep(0.25)
            MYPRINT_OPEN_FLAG = MyPrint_ReubenPython2and3ClassObject.OBJECT_CREATED_SUCCESSFULLY_FLAG

        except:
            exceptions = sys.exc_info()[0]
            print("MyPrint_ReubenPython2and3ClassObject __init__: Exceptions: %s" % exceptions)
            traceback.print_exc()
    #################################################
    #################################################

    #################################################
    #################################################
    if USE_BLDC_FLAG_Left1 == 1 and BLDC_OPEN_FLAG_Left1 != 1:
        print("Failed to open PhidgetBrushlessDCmotorDCC1100controller_ReubenPython2and3Class (Left Motor).")
        input("Press any key (and enter) to exit.")
        sys.exit()
    #################################################
    #################################################

    #################################################
    #################################################
    if USE_BLDC_FLAG_Right0 == 1 and BLDC_OPEN_FLAG_Right0 != 1:
        print("Failed to open PhidgetBrushlessDCmotorDCC1100controller_ReubenPython2and3Class (Right Motor).")
        input("Press any key (and enter) to exit.")
        sys.exit()
    #################################################
    #################################################

    #################################################
    #################################################
    if USE_MYPRINT_FLAG == 1 and MYPRINT_OPEN_FLAG != 1:
        print("Failed to open MyPrint_ReubenPython2and3ClassObject.")
        input("Press any key (and enter) to exit.")
        sys.exit()
    #################################################
    #################################################

    ################################################# SHOWS HOW TO OFFSET THE ANGLE
    #################################################
    #if BLDC_setup_dict["ControlMode"] == "position":
    #    time.sleep(0.5)
    #    PhidgetBrushlessDCmotorDCC1100controller_ReubenPython2and3ClassObject.SetPositionOffsetOnBoardWithoutMoving(90)
    #################################################
    #################################################

    #################################################
    #################################################
    print("Starting main loop 'test_program_for_PhidgetBrushlessDCmotorDCC1100controller_ReubenPython2and3Class.")
    StartingTime_MainLoopThread = getPreciseSecondsTimeStampString()

    # DRIVE AND TURN SPEEDS

    DRIVE_SPEED = 0.4
    TURN_SPEED = 0.2

    while(EXIT_PROGRAM_FLAG == 0):

        ###################################################
        CurrentTime_MainLoopThread = getPreciseSecondsTimeStampString() - StartingTime_MainLoopThread
        ###################################################

        ###################################################
        if USE_BLDC_FLAG_Left1 == 1:
            ######################### GETs
            BLDC_MostRecentDict_Left1 = PhidgetBrushlessDCmotorDCC1100controller_ReubenPython2and3ClassObject_Left1.GetMostRecentDataDict()

            BLDC_MostRecentDict_Position_PhidgetsUnits_FromDevice_Left1 = BLDC_MostRecentDict_Left1["Position_PhidgetsUnits_FromDevice"]
            BLDC_MostRecentDict_Velocity_PhidgetsUnits_FromDevice_Left1 = BLDC_MostRecentDict_Left1["Velocity_PhidgetsUnits_FromDevice"]
            BLDC_MostRecentDict_Velocity_PhidgetsUnits_DifferentiatedRaw_Left1 = BLDC_MostRecentDict_Left1["Velocity_PhidgetsUnits_DifferentiatedRaw"]
            BLDC_MostRecentDict_Velocity_PhidgetsUnits_DifferentiatedSmoothed_Left1 = BLDC_MostRecentDict_Left1["Velocity_PhidgetsUnits_DifferentiatedSmoothed"]
            BLDC_MostRecentDict_DutyCycle_PhidgetsUnits_FromDevice_Left1 = BLDC_MostRecentDict_Left1["DutyCycle_PhidgetsUnits_FromDevice"]
            BLDC_MostRecentDict_Temperature_DegC_FromDevice_Left1 = BLDC_MostRecentDict_Left1["Temperature_DegC_FromDevice"]
            BLDC_MostRecentDict_Time_Left1 = BLDC_MostRecentDict_Left1["Time"]

            if keyboard.is_pressed('w'):
                # Forward
                PhidgetBrushlessDCmotorDCC1100controller_ReubenPython2and3ClassObject_Left1.CommandMotorFromExternalProgram_VelocityControl(DRIVE_SPEED)
            elif keyboard.is_pressed('s'):
                # Backward
                PhidgetBrushlessDCmotorDCC1100controller_ReubenPython2and3ClassObject_Left1.CommandMotorFromExternalProgram_VelocityControl(-DRIVE_SPEED)
            elif keyboard.is_pressed('a'):
                # Left
                PhidgetBrushlessDCmotorDCC1100controller_ReubenPython2and3ClassObject_Left1.CommandMotorFromExternalProgram_VelocityControl(-TURN_SPEED)
            elif keyboard.is_pressed('d'):
                # Right
                PhidgetBrushlessDCmotorDCC1100controller_ReubenPython2and3ClassObject_Left1.CommandMotorFromExternalProgram_VelocityControl(TURN_SPEED)
            else:
                # Stop
                PhidgetBrushlessDCmotorDCC1100controller_ReubenPython2and3ClassObject_Left1.CommandMotorFromExternalProgram_VelocityControl(0)

        if USE_BLDC_FLAG_Right0 == 1:
            ######################### GETs
            BLDC_MostRecentDict_Right0 = PhidgetBrushlessDCmotorDCC1100controller_ReubenPython2and3ClassObject_Right0.GetMostRecentDataDict()

            BLDC_MostRecentDict_Position_PhidgetsUnits_FromDevice_Right0 = BLDC_MostRecentDict_Right0["Position_PhidgetsUnits_FromDevice"]
            BLDC_MostRecentDict_Velocity_PhidgetsUnits_FromDevice_Right0 = BLDC_MostRecentDict_Right0["Velocity_PhidgetsUnits_FromDevice"]
            BLDC_MostRecentDict_Velocity_PhidgetsUnits_DifferentiatedRaw_Right0 = BLDC_MostRecentDict_Right0["Velocity_PhidgetsUnits_DifferentiatedRaw"]
            BLDC_MostRecentDict_Velocity_PhidgetsUnits_DifferentiatedSmoothed_Right0 = BLDC_MostRecentDict_Right0["Velocity_PhidgetsUnits_DifferentiatedSmoothed"]
            BLDC_MostRecentDict_DutyCycle_PhidgetsUnits_FromDevice_Right0 = BLDC_MostRecentDict_Right0["DutyCycle_PhidgetsUnits_FromDevice"]
            BLDC_MostRecentDict_Temperature_DegC_FromDevice_Right0 = BLDC_MostRecentDict_Right0["Temperature_DegC_FromDevice"]
            BLDC_MostRecentDict_Time_Right0 = BLDC_MostRecentDict_Right0["Time"]

            if keyboard.is_pressed('w'):
                # Forward
                PhidgetBrushlessDCmotorDCC1100controller_ReubenPython2and3ClassObject_Right0.CommandMotorFromExternalProgram_VelocityControl(-DRIVE_SPEED)
            elif keyboard.is_pressed('s'):
                # Backward
                PhidgetBrushlessDCmotorDCC1100controller_ReubenPython2and3ClassObject_Right0.CommandMotorFromExternalProgram_VelocityControl(DRIVE_SPEED)
            elif keyboard.is_pressed('a'):
                # Left
                PhidgetBrushlessDCmotorDCC1100controller_ReubenPython2and3ClassObject_Right0.CommandMotorFromExternalProgram_VelocityControl(-TURN_SPEED)
            elif keyboard.is_pressed('d'):
                # Right
                PhidgetBrushlessDCmotorDCC1100controller_ReubenPython2and3ClassObject_Right0.CommandMotorFromExternalProgram_VelocityControl(TURN_SPEED)
            else:
                # Stop
                PhidgetBrushlessDCmotorDCC1100controller_ReubenPython2and3ClassObject_Right0.CommandMotorFromExternalProgram_VelocityControl(0)
        
        time.sleep(0.010)
        ###################################################

    #################################################
    #################################################

    print("Exiting main program 'test_program_for_PhidgetBrushlessDCmotorDCC1100controller_ReubenPython2and3Class.")
##########################################################################################################
##########################################################################################################