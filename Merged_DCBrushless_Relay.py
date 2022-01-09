# -*- coding: utf-8 -*-

'''
Reuben Brewer, Ph.D.
reuben.brewer@gmail.com
www.reubotics.com

Apache 2 License
Software Revision E, 09/03/2021

Verified working on: Python 2.7 and 3.7 for Windows 8.1 64-bit and Raspberry Pi Buster (no Mac testing yet).
'''

__author__ = 'reuben.brewer'

import os, sys, platform
import time, datetime
import traceback
import threading
import math
import collections
import inspect


if sys.version_info[0] < 3:
    from Tkinter import * #Python 2
    import tkFont
else:
    from tkinter import * #Python 3
    import tkinter.font as tkFont #Python 3
    from tkinter import ttk


if sys.version_info[0] < 3:
    import Queue  # Python 2
else:
    import queue as Queue  # Python 3


if sys.version_info[0] < 3:
    from builtins import raw_input as input
else:
    from future.builtins import input as input #"sudo pip3 install future" (Python 3) AND "sudo pip install future" (Python 2)


from Phidget22.PhidgetException import *
from Phidget22.Phidget import *
from Phidget22.Devices.Log import *
from Phidget22.LogLevel import *
from Phidget22.Devices.DigitalOutput import *


class MyPrint_ReubenPython2and3Class(Frame): #Subclass the Tkinter Frame

    def __init__(self, setup_dict):

        print("#################### MyPrint_ReubenPython2and3Class __init__ starting. ####################")

        self.OBJECT_CREATED_SUCCESSFULLY_FLAG = -1
        self.EXIT_PROGRAM_FLAG = 0

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
        if "NumberOfPrintLines" in setup_dict:
            self.NumberOfPrintLines = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("NumberOfPrintLines", setup_dict["NumberOfPrintLines"], 0.0, 1000.0))
        else:
            self.NumberOfPrintLines = 15

        print("NumberOfPrintLines = " + str(self.NumberOfPrintLines))
        ##########################################

        ##########################################
        if "WidthOfPrintingLabel" in setup_dict:
            self.WidthOfPrintingLabel = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("WidthOfPrintingLabel", setup_dict["WidthOfPrintingLabel"], 10.0, 1920.0))
        else:
            self.WidthOfPrintingLabel = 100

        print("WidthOfPrintingLabel = " + str(self.WidthOfPrintingLabel))
        ##########################################

        ##########################################
        if "PrintToConsoleFlag" in setup_dict:
            self.PrintToConsoleFlag = self.PassThrough0and1values_ExitProgramOtherwise("PrintToConsoleFlag", setup_dict["PrintToConsoleFlag"])
        else:
            self.PrintToConsoleFlag = 0

        print("PrintToConsoleFlag = " + str(self.PrintToConsoleFlag))
        ##########################################

        ##########################################
        if "LogFileNameFullPath" in setup_dict:
            self.LogFileNameFullPath = str(setup_dict["LogFileNameFullPath"])

            if self.LogFileNameFullPath.find("/") == -1 and self.LogFileNameFullPath.find("\\") == -1:
                print("MyPrint_ReubenPython2and3Class __init__ error: 'LogFileNameFullPath' must be FULL path (should include slashes).")
                return

        else:
            self.LogFileNameFullPath = os.getcwd()

        print("LogFileNameFullPath = " + str(self.LogFileNameFullPath))
        ##########################################

        self.PrintToGui_Label_TextInputHistory_List = [" "]*self.NumberOfPrintLines
        self.PrintToGui_Label_TextInput_Str = ""

        self.LinesToBeWrittenToFileQueue = Queue.Queue()

        self.GUI_ready_to_be_updated_flag = 0

        print("#################### MyPrint_ReubenPython2and3Class __init__ ended input-parameter parsing and variable initialization. ####################")

        ##########################################
        self.MainDataWritingThread_ThreadingObject = threading.Thread(target=self.MainDataWritingThread, args=())
        self.MainDataWritingThread_ThreadingObject.start()
        ##########################################

        ##########################################
        if self.USE_GUI_FLAG == 1:
            self.StartGUI(self.root)
        ##########################################

        self.OBJECT_CREATED_SUCCESSFULLY_FLAG = 1

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
    def getPreciseSecondsTimeStampString(self):
        ts = time.time()

        return ts
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def getTimeStampStringReubenPreferredFormat(self):
        ts = time.time()
        st = datetime.datetime.fromtimestamp(ts).strftime('date-%m-%d-%Y---time-%H-%M-%S')

        return st
    ##########################################################################################################
    ##########################################################################################################

    #######################################################################################################################
    #######################################################################################################################
    def CreateNewDirectoryIfItDoesntExist(self, DirectoryFullPathToCheck):
        try:
            #print("CreateNewDirectoryIfItDoesntExist, DirectoryFullPathToCheck = " + DirectoryFullPathToCheck)
            if os.path.isdir(DirectoryFullPathToCheck) == 0:
                os.makedirs(DirectoryFullPathToCheck)
                #print("CreateNewDirectoryIfItDoesntExist, created new directory!")
        except:
            exceptions = sys.exc_info()[0]
            print("CreateNewDirectoryIfItDoesntExist ERROR, Exceptions: %s" % exceptions)
            traceback.print_exc()

    #######################################################################################################################
    #######################################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def SetPrintToConsoleFlag(self, value):
        if value == 0 or value == 1:
            self.PrintToConsoleFlag = value
        else:
            self.my_print("SetPrintToConsoleFlag ERROR: This function accepts only 0 or 1.")
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def MainDataWritingThread(self):

        self.my_print("Started the MainDataWritingThread for MyPrint_ReubenPython2and3Class object.")

        ######################################################
        try:
            if self.LogFileNameFullPath != "":
                print(os.path.dirname(self.LogFileNameFullPath))
                self.CreateNewDirectoryIfItDoesntExist(os.path.dirname(self.LogFileNameFullPath)) #os.path.dirname grabs just the directory path

                with open(self.LogFileNameFullPath, "a+") as self.LogFileObject: #File is created if it doesn't exist, automatically closes cleanly due to "with" if program crashes
                    self.LogFileObject.write("######################################################" + "\n")
                    while True:
                        if self.LinesToBeWrittenToFileQueue.qsize() > 0:
                            NextLineToBeWrittenToFile = self.LinesToBeWrittenToFileQueue.get()
                            self.LogFileObject.write(self.getTimeStampStringReubenPreferredFormat() + ": " + NextLineToBeWrittenToFile + "\n")
                            self.LogFileObject.flush() #IF WE WON'T FLUSH, THEN WE'LL LOSE ALL CHANGES IF PYTHON CRASHES

                        if self.EXIT_PROGRAM_FLAG == 1:
                            self.LogFileObject.write("######################################################" + "\n")
                            break
                        else:
                            time.sleep(0.001)

        except:
            exceptions = sys.exc_info()[0]
            print("MyPrintClass ERROR: failed opening/writing LogFileNameFullPath = '" + str(self.LogFileNameFullPath) + "', Exceptions: %s" % exceptions)
        ######################################################


        print("Exited the main thread for MyPrint_ReubenPython2and3Class object.")
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def ExitProgram_Callback(self):

        print("Exiting all threads for MyPrint_ReubenPython2and3Class.")

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

        print("Starting the GUI_Thread for MyPrint_ReubenPython2and3Class object.")

        ########################
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
        ########################

        ########################
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
        ########################

        ########################
        self.PrintToGui_Label = Label(self.myFrame, text="PrintToGui_Label", width=self.WidthOfPrintingLabel)
        self.PrintToGui_Label.grid(row=0, column=0, padx=1, pady=1, columnspan=1, rowspan=1)
        ########################

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
    def GUI_update_clock(self):

        #######################################################
        #######################################################
        #######################################################
        if self.USE_GUI_FLAG == 1 and self.EXIT_PROGRAM_FLAG == 0:

            #######################################################
            #######################################################
            if self.GUI_ready_to_be_updated_flag == 1:

                #######################################################
                self.PrintToGui_Label.config(text = self.PrintToGui_Label_TextInput_Str)
                #######################################################

            #######################################################
            #######################################################

            #######################################################
            #######################################################
            if self.RootIsOwnedExternallyFlag == 0:  #This class object owns root and must handle it properly
                self.root.after(self.GUI_RootAfterCallbackInterval_Milliseconds, self.GUI_update_clock)
            #######################################################
            #######################################################

        #######################################################
        #######################################################
        #######################################################

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def my_print(self, input_string):

        input_string = str(input_string)

        if input_string != "":

            ################################ Write to file WITHOUT MODIFICATION
            if self.LogFileNameFullPath != "":
                self.LinesToBeWrittenToFileQueue.put(input_string)
            ################################

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

class Phidgets1xRelayREL2001_ReubenPython2and3Class(Frame): #Subclass the Tkinter Frame

    #######################################################################################################################
    #######################################################################################################################
    def __init__(self, setup_dict): #Subclass the Tkinter Frame

        print("#################### Phidgets1xRelayREL2001_ReubenPython2and3Class __init__ starting. ####################")

        self.EXIT_PROGRAM_FLAG = 0
        self.OBJECT_CREATED_SUCCESSFULLY_FLAG = -1
        self.EnableInternal_MyPrint_Flag = 0
        self.MainThread_still_running_flag = 0

        self.DigitalOutputsList_PhidgetsDigitalOutputObjects = list()

        self.NumberOfDigitalOutputs = 1

        self.DigitalOutputsList_AttachedAndOpenFlag = [-1.0]*self.NumberOfDigitalOutputs
        self.DigitalOutputsList_ErrorCallbackFiredFlag = [-1.0]*self.NumberOfDigitalOutputs

        self.DigitalOutputsList_State = [-1]*self.NumberOfDigitalOutputs
        self.DigitalOutputsList_State_NeedsToBeChangedFlag = [1]*self.NumberOfDigitalOutputs
        self.DigitalOutputsList_State_ToBeSet = [0]*self.NumberOfDigitalOutputs

        self.MostRecentDataDict = dict()

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
            print("Phidgets1xRelayREL2001_ReubenPython2and3Class __init__: No GUIparametersDict present, setting USE_GUI_FLAG = " + str(self.USE_GUI_FLAG))

        print("GUIparametersDict = " + str(self.GUIparametersDict))
        ##########################################
        ##########################################

       ##########################################
        if "VINT_DesiredSerialNumber" in setup_dict:
            try:
                self.VINT_DesiredSerialNumber = int(setup_dict["VINT_DesiredSerialNumber"])
            except:
                print("ERROR: VINT_DesiredSerialNumber invalid.")
        else:
            self.OBJECT_CREATED_SUCCESSFULLY_FLAG = 0
            print("PhidgetBrushlessDCmotorDCC1100controller_ReubenPython2and3Class ERROR: Must initialize object with 'VINT_DesiredSerialNumber' argument.")
            return

        print("VINT_DesiredSerialNumber: " + str(self.VINT_DesiredSerialNumber))
        ##########################################

        ##########################################
        if "VINT_DesiredPortNumber" in setup_dict:
            try:
                self.VINT_DesiredPortNumber = int(setup_dict["VINT_DesiredPortNumber"])
            except:
                print("ERROR: VINT_DesiredPortNumber invalid.")
        else:
            self.OBJECT_CREATED_SUCCESSFULLY_FLAG = 0
            print("PhidgetBrushlessDCmotorDCC1100controller_ReubenPython2and3Class ERROR: Must initialize object with 'VINT_DesiredPortNumber' argument.")
            return

        print("VINT_DesiredPortNumber: " + str(self.VINT_DesiredPortNumber))
        ##########################################

        ##########################################
        if "DesiredDeviceID" in setup_dict:
            try:
                self.DesiredDeviceID = int(setup_dict["DesiredDeviceID"])
            except:
                print("ERROR: DesiredDeviceID invalid.")
        else:
            self.OBJECT_CREATED_SUCCESSFULLY_FLAG = 0
            print("PhidgetBrushlessDCmotorDCC1100controller_ReubenPython2and3Class ERROR: Must initialize object with 'DesiredDeviceID' argument.")
            return

        print("DesiredDeviceID: " + str(self.DesiredDeviceID))
        ##########################################

        ##########################################
        if "NameToDisplay_UserSet" in setup_dict:
            self.NameToDisplay_UserSet = str(setup_dict["NameToDisplay_UserSet"])
        else:
            self.NameToDisplay_UserSet = ""
        ##########################################

        ##########################################
        if "WaitForAttached_TimeoutDuration_Milliseconds" in setup_dict:
            self.WaitForAttached_TimeoutDuration_Milliseconds = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("WaitForAttached_TimeoutDuration_Milliseconds", setup_dict["WaitForAttached_TimeoutDuration_Milliseconds"], 0.0, 60000.0))

        else:
            self.WaitForAttached_TimeoutDuration_Milliseconds = 5000

        print("WaitForAttached_TimeoutDuration_Milliseconds: " + str(self.WaitForAttached_TimeoutDuration_Milliseconds))
        ##########################################

        ##########################################
        if "UsePhidgetsLoggingInternalToThisClassObjectFlag" in setup_dict:
            self.UsePhidgetsLoggingInternalToThisClassObjectFlag = self.PassThrough0and1values_ExitProgramOtherwise("UsePhidgetsLoggingInternalToThisClassObjectFlag", setup_dict["UsePhidgetsLoggingInternalToThisClassObjectFlag"])
        else:
            self.UsePhidgetsLoggingInternalToThisClassObjectFlag = 1

        print("UsePhidgetsLoggingInternalToThisClassObjectFlag: " + str(self.UsePhidgetsLoggingInternalToThisClassObjectFlag))
        ##########################################

       ##########################################
        if "MainThread_TimeToSleepEachLoop" in setup_dict:
            self.MainThread_TimeToSleepEachLoop = self.PassThroughFloatValuesInRange_ExitProgramOtherwise("MainThread_TimeToSleepEachLoop", setup_dict["MainThread_TimeToSleepEachLoop"], 0.001, 100000)

        else:
            self.MainThread_TimeToSleepEachLoop = 0.005

        print("MainThread_TimeToSleepEachLoop: " + str(self.MainThread_TimeToSleepEachLoop))
        ##########################################

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

        self.DetectedDeviceName = "default"
        self.DetectedDeviceID = "default"
        self.DetectedDeviceVersion = "default"
        self.VINT_DetectedSerialNumber = "default"
        #########################################################

        #########################################################
        #########################################################

        #########################################################
        #########################################################
        try:

            #########################################################
            self.DigitalOutput0object = DigitalOutput()
            self.DigitalOutput0object.setIsHubPortDevice(True) # $$$$ KEY LINE THAT'S DIFFERENT FROM THE Phidgets4xRelayREL1000_ReubenPython2and3Class CODE!!!!
            self.DigitalOutputsList_PhidgetsDigitalOutputObjects.append(self.DigitalOutput0object)
            self.DigitalOutput0object.setHubPort(self.VINT_DesiredPortNumber)
            self.DigitalOutput0object.setDeviceSerialNumber(self.VINT_DesiredSerialNumber)
            self.DigitalOutput0object.setOnAttachHandler(self.DigitalOutput0onAttachCallback)
            self.DigitalOutput0object.setOnDetachHandler(self.DigitalOutput0onDetachCallback)
            self.DigitalOutput0object.setOnErrorHandler(self.DigitalOutput0onErrorCallback)
            self.DigitalOutput0object.openWaitForAttachment(self.WaitForAttached_TimeoutDuration_Milliseconds)
            #########################################################

            self.PhidgetsDeviceConnectedFlag = 1

        except PhidgetException as e:
            self.PhidgetsDeviceConnectedFlag = 0
            print("Phidgets1xRelayREL2001_ReubenPython2and3Class __init__Failed to attach, Phidget Exception %i: %s" % (e.code, e.details))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if self.PhidgetsDeviceConnectedFlag == 1:

            #########################################################
            if self.UsePhidgetsLoggingInternalToThisClassObjectFlag == 1:
                try:
                    Log.enable(LogLevel.PHIDGET_LOG_INFO, os.getcwd() + "\Phidgets1xRelayREL2001_ReubenPython2and3Class_PhidgetLog_INFO.txt")
                    print("Phidgets1xRelayREL2001_ReubenPython2and3Class __init__Enabled Phidget Logging.")
                except PhidgetException as e:
                    print("Phidgets1xRelayREL2001_ReubenPython2and3Class __init__Failed to enable Phidget Logging, Phidget Exception %i: %s" % (e.code, e.details))
            #########################################################

            #########################################################
            try:
                self.DetectedDeviceName = self.DigitalOutput0object.getDeviceName()
                print("DetectedDeviceName: " + self.DetectedDeviceName)

            except PhidgetException as e:
                print("Failed to call 'getDeviceName', Phidget Exception %i: %s" % (e.code, e.details))
            #########################################################

            #########################################################
            try:
                self.VINT_DetectedSerialNumber = self.DigitalOutput0object.getDeviceSerialNumber()
                print("VINT_DetectedSerialNumber: " + str(self.VINT_DetectedSerialNumber))

            except PhidgetException as e:
                print("Failed to call 'getDeviceSerialNumber', Phidget Exception %i: %s" % (e.code, e.details))
            #########################################################

            #########################################################
            try:
                self.DetectedDeviceID = self.DigitalOutput0object.getDeviceID()
                print("DetectedDeviceID: " + str(self.DetectedDeviceID))

            except PhidgetException as e:
                print("Failed to call 'getDesiredDeviceID', Phidget Exception %i: %s" % (e.code, e.details))
            #########################################################

            #########################################################
            try:
                self.DetectedDeviceVersion = self.DigitalOutput0object.getDeviceVersion()
                print("DetectedDeviceVersion: " + str(self.DetectedDeviceVersion))

            except PhidgetException as e:
                print("Failed to call 'getDeviceVersion', Phidget Exception %i: %s" % (e.code, e.details))
            #########################################################

            #########################################################
            try:
                self.DetectedDeviceLibraryVersion = self.DigitalOutput0object.getLibraryVersion()
                print("DetectedDeviceLibraryVersion: " + str(self.DetectedDeviceLibraryVersion))

            except PhidgetException as e:
                print("Failed to call 'getLibraryVersion', Phidget Exception %i: %s" % (e.code, e.details))
            #########################################################

            #########################################################
            if self.VINT_DetectedSerialNumber != self.VINT_DesiredSerialNumber:
                print("The desired Serial Number (" + str(self.VINT_DesiredSerialNumber) + ") does not match the detected serial number (" + str(self.VINT_DetectedSerialNumber) + ").")
                input("Press any key (and enter) to exit.")
                sys.exit()
            #########################################################

            #########################################################
            if self.DetectedDeviceID != self.DesiredDeviceID:
                print("The desired DesiredDeviceID (" + str(self.DesiredDeviceID) + ") does not match the detected Device ID (" + str(self.DetectedDeviceID) + ").")
                input("Press any key (and enter) to exit.")
                sys.exit()
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

        #########################################################
        #########################################################

    #######################################################################################################################
    #######################################################################################################################

    #######################################################################################################################
    #######################################################################################################################
    def __del__(self):
        dummy_var = 0
    #######################################################################################################################
    #######################################################################################################################

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
    def DigitalOutputGENERALonAttachCallback(self, DigitalOutputChannel):

        try:
            self.DigitalOutputsList_AttachedAndOpenFlag[DigitalOutputChannel] = 1
            self.MyPrint_WithoutLogFile("$$$$$$$$$$ DigitalOutputGENERALonAttachCallback event for DigitalOutputChannel " + str(DigitalOutputChannel) + ", Attached! $$$$$$$$$$")

        except PhidgetException as e:
            self.DigitalOutputsList_AttachedAndOpenFlag[DigitalOutputChannel] = 0
            self.MyPrint_WithoutLogFile("DigitalOutputGENERALonAttachCallback event for DigitalOutputChannel " + str(DigitalOutputChannel) + ", ERROR: Failed to attach DigitalOutput0, Phidget Exception %i: %s" % (e.code, e.details))
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def DigitalOutputGENERALonDetachCallback(self, DigitalOutputChannel):

        self.DigitalOutputsList_AttachedAndOpenFlag[DigitalOutputChannel] = 0
        self.MyPrint_WithoutLogFile("$$$$$$$$$$ DigitalOutputGENERALonDetachCallback event for DigitalOutputChannel " + str(DigitalOutputChannel) + ", Detatched! $$$$$$$$$$")

        try:
            self.DigitalOutputsList_PhidgetsDigitalOutputObjects[DigitalOutputChannel].openWaitForAttachment(self.WaitForAttached_TimeoutDuration_Milliseconds)
            time.sleep(0.250)

        except PhidgetException as e:
            self.MyPrint_WithoutLogFile("DigitalOutputGENERALonDetachCallback event for DigitalOutput Channel " + str(DigitalOutputChannel) + ", failed to openWaitForAttachment, Phidget Exception %i: %s" % (e.code, e.details))
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def DigitalOutputGENERALonErrorCallback(self, DigitalOutputChannel, code, description):

        self.DigitalOutputsList_ErrorCallbackFiredFlag[DigitalOutputChannel] = 1

        self.MyPrint_WithoutLogFile("DigitalOutputGENERALonErrorCallback event for DigitalOutput Channel " + str(DigitalOutputChannel) + ", Error Code " + ErrorEventCode.getName(code) + ", description: " + str(description))
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def DigitalOutput0onAttachCallback(self, HandlerSelf):

        DigitalOutputChannel = 0
        self.DigitalOutputGENERALonAttachCallback(DigitalOutputChannel)

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def DigitalOutput0onDetachCallback(self, HandlerSelf):

        DigitalOutputChannel = 0
        self.DigitalOutputGENERALonDetachCallback(DigitalOutputChannel)

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def DigitalOutput0onErrorCallback(self, HandlerSelf, code, description):

        DigitalOutputChannel = 0
        self.DigitalOutputGENERALonErrorCallback(DigitalOutputChannel, code, description)

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
    def SetRelayState(self, State_ToBeSet):

        if State_ToBeSet in [0, 1]:
            self.DigitalOutputsList_State_ToBeSet[0] = State_ToBeSet
            self.DigitalOutputsList_State_NeedsToBeChangedFlag[0] = 1
        else:
            print("SetRelayState ERROR, State_ToBeSet must be 0 or 1.")

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def GetMostRecentDataDict(self):

        self.MostRecentDataDict = dict([("DigitalOutputsList_State", self.DigitalOutputsList_State),
                                             ("DigitalOutputsList_ErrorCallbackFiredFlag", self.DigitalOutputsList_ErrorCallbackFiredFlag),
                                             ("Time", self.CurrentTime_CalculatedFromMainThread)])

        return self.MostRecentDataDict
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
    ########################################################################################################## unicorn
    def MainThread(self):

        self.MyPrint_WithoutLogFile("Started MainThread for Phidgets1xRelayREL2001_ReubenPython2and3Class object.")
        
        self.MainThread_still_running_flag = 1

        self.StartingTime_CalculatedFromMainThread = self.getPreciseSecondsTimeStampString()

        ###############################################
        while self.EXIT_PROGRAM_FLAG == 0:

            ###############################################
            self.CurrentTime_CalculatedFromMainThread = self.getPreciseSecondsTimeStampString() - self.StartingTime_CalculatedFromMainThread
            ###############################################

            ###############################################
            for DigitalOutputChannel in range(0, self.NumberOfDigitalOutputs):

                if self.DigitalOutputsList_State_NeedsToBeChangedFlag[DigitalOutputChannel] == 1:

                    self.DigitalOutputsList_PhidgetsDigitalOutputObjects[DigitalOutputChannel].setState(self.DigitalOutputsList_State_ToBeSet[DigitalOutputChannel])
                    time.sleep(0.002)

                    self.DigitalOutputsList_State[DigitalOutputChannel] = self.DigitalOutputsList_PhidgetsDigitalOutputObjects[DigitalOutputChannel].getState()
                    if self.DigitalOutputsList_State[DigitalOutputChannel] == self.DigitalOutputsList_State_ToBeSet[DigitalOutputChannel]:
                        self.DigitalOutputsList_State_NeedsToBeChangedFlag[DigitalOutputChannel] = 0

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

        ###############################################
        for DigitalOutputChannel in range(0, self.NumberOfDigitalOutputs):
            self.DigitalOutputsList_PhidgetsDigitalOutputObjects[DigitalOutputChannel].close()
        ###############################################

        self.MyPrint_WithoutLogFile("Finished MainThread for Phidgets1xRelayREL2001_ReubenPython2and3Class object.")
        
        self.MainThread_still_running_flag = 0
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def ExitProgram_Callback(self):

        print("Exiting all threads for Phidgets1xRelayREL2001_ReubenPython2and3Class object")

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

        print("Starting the GUI_Thread for Phidgets1xRelayREL2001_ReubenPython2and3Class object.")

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

        #################################################
        self.device_info_label = Label(self.myFrame, text="Device Info", width=50) #, font=("Helvetica", 16)

        self.device_info_label["text"] = self.NameToDisplay_UserSet + \
                                        "\nDevice Name: " + self.DetectedDeviceName + \
                                        "\nDevice Serial Number: " + str(self.VINT_DetectedSerialNumber) + \
                                        "\nDevice ID: " + str(self.DetectedDeviceID) + \
                                        "\nDevice Version: " + str(self.DetectedDeviceVersion)

        self.device_info_label.grid(row=0, column=0, padx=5, pady=1, columnspan=1, rowspan=1)
        #################################################

        #################################################
        self.DigitalOutputs_Label = Label(self.myFrame, text="DigitalOutputs_Label", width=70)
        self.DigitalOutputs_Label.grid(row=0, column=1, padx=5, pady=1, columnspan=1, rowspan=10)
        #################################################
        
        #################################################

        self.DigitalOutputButtonsFrame = Frame(self.myFrame)

        #if self.UseBorderAroundThisGuiObjectFlag == 1:
        #    self.myFrame["borderwidth"] = 2
        #    self.myFrame["relief"] = "ridge"

        self.DigitalOutputButtonsFrame.grid(row = 1, column = 0, padx = 1, pady = 1, rowspan = 1, columnspan = 1)

        self.DigitalOutputsList_ButtonObjects = []
        for DigitalOutputChannel in range(0, self.NumberOfDigitalOutputs):
            self.DigitalOutputsList_ButtonObjects.append(Button(self.DigitalOutputButtonsFrame, text="Relay " + str(DigitalOutputChannel), state="normal", width=8, command=lambda i=DigitalOutputChannel: self.DigitalOutputsList_ButtonObjectsResponse(i)))
            self.DigitalOutputsList_ButtonObjects[DigitalOutputChannel].grid(row=1, column=DigitalOutputChannel, padx=1, pady=1)
        #################################################

        ########################
        self.PrintToGui_Label = Label(self.myFrame, text="PrintToGui_Label", width=75)
        if self.EnableInternal_MyPrint_Flag == 1:
            self.PrintToGui_Label.grid(row=0, column=2, padx=1, pady=1, columnspan=1, rowspan=10)
        ########################

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
                    #######################################################
                    for DigitalOutputChannel in range(0, self.NumberOfDigitalOutputs):
                        if self.DigitalOutputsList_State[DigitalOutputChannel] == 1:
                            self.DigitalOutputsList_ButtonObjects[DigitalOutputChannel]["bg"] = self.TKinter_LightGreenColor
                        elif self.DigitalOutputsList_State[DigitalOutputChannel] == 0:
                            self.DigitalOutputsList_ButtonObjects[DigitalOutputChannel]["bg"] = self.TKinter_LightRedColor
                        else:
                            self.DigitalOutputsList_ButtonObjects[DigitalOutputChannel]["bg"] = self.TKinter_DefaultGrayColor
                    #######################################################

                    #######################################################
                    self.DigitalOutputs_Label["text"] = "\nDigital States: " + str(self.DigitalOutputsList_State) + \
                                                "\nTime: " + self.ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(self.CurrentTime_CalculatedFromMainThread, 0, 3) + \
                                                "\nData Frequency: " + self.ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(self.DataStreamingFrequency_CalculatedFromMainThread, 0, 3)
                    #######################################################

                    #######################################################
                    self.PrintToGui_Label.config(text=self.PrintToGui_Label_TextInput_Str)
                    #######################################################

                except:
                    exceptions = sys.exc_info()[0]
                    print("Phidgets1xRelayREL2001_ReubenPython2and3Class GUI_update_clock ERROR: Exceptions: %s" % exceptions)
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
    def DigitalOutputsList_ButtonObjectsResponse(self, DigitalOutputChannel):

        if self.DigitalOutputsList_State[DigitalOutputChannel] == 1:
            self.DigitalOutputsList_State_ToBeSet[DigitalOutputChannel] = 0
        else:
            self.DigitalOutputsList_State_ToBeSet[DigitalOutputChannel] = 1

        self.DigitalOutputsList_State_NeedsToBeChangedFlag[DigitalOutputChannel] = 1

        self.MyPrint_WithoutLogFile("DigitalOutputsList_ButtonObjectsResponse: Event fired for DigitalOutputChannel " + str(DigitalOutputChannel))

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
