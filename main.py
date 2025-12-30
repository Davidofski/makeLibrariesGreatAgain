'''     Project: Square Line Corrector UI

            What it does:
            - Corrects incorrect image names in Square Line generated project files
            - Activates and customizes lv_conf.h file for selected font sizes
                - Includes lv_conf.h in lvgl.h if not already included
                - Updates lv_conf.h file to include only selected font sizes
            - Copies Square Line project 'library -> ui' folder to Arduino library folder
            - Provides output log in GUI
            - Allows user to specify paths via GUI
            - Provides default paths loaded from defaultPaths.txt file
            - Stores last used paths in defaultPaths.txt file
                - If defaultPaths.txt does not exist, it is created with current working directory as default paths
            - Provides Execute and Exit buttons in GUI

        # GUI built with DearPyGui
        # Author: David Fischill (david.fischill@gmail.com) (GitHub: Davidofski)
        # Date: 30.12.2025
        # Version: 1.0.0
        '''
# importing necessary modules
import dearpygui.dearpygui as dpg
import settings as st
import os

# variables and memory for output log
outputMessages = []
messageText = ""
UIisBuilt = False
# configuration file names
lv_conf_filename = 'lv_conf.h'
lv_conf_template_filename = 'lv_conf_template.h'
lvgl_header_filename = r"\lvgl.h"

# Function to update output log in GUI
def outputLog(message):
    try:
        outputMessages.insert(0, message) # insert new message at the beginning
        if len(outputMessages) > 15: # keep only last 15 messages
            outputMessages.pop(15)
        # only update GUI if dpg is fully built, else context/items may not yet exist and program will crash
        if UIisBuilt: # check if GUI is built, then update output log, if GUI is not built yet, windows returns error
            messageText = "\n".join(outputMessages) # join messages
            dpg.set_value('output_log_0', messageText)  # update output log in GUI
    except Exception as e: # catch any error and print to console
        print(f"[Error] Error updating output log: {e}")

# Function to read any file
def readFile (path):
    try:
        with open (path, 'r') as file:
            message = f"[Read File] File successfully opened with path: {path}"
            text = file.read()
            file.close()
    except Exception as e:
        message = f"[Read File] [Error] File could NOT be opened with path {path}\nException: {e}"
        text = ""
    print(message)
    outputLog(message) # Log message to output log
    return text

# Function to write text to a file
def writeFile (path, text):
    try:
        with open (path, 'w') as file:
            file.write(text)
            message = f"[Writing File] Writing file was successful with path {path}"
            file.close()
    except Exception as e:
        message = f"[Writing File] [Error] Writing of file was NOT successful with path {path}\nException: {e}"
    print(message)
    outputLog(message) # Log message to output log

# Function to replace specific text
def replaceText(text, searchText, replacementText):
    if searchText not in text:
        message = f"[Replace Text]{searchText} not found in text."
    else:
        text = text.replace(searchText, replacementText)
        message = f"[Replace Text] {searchText} has been replaced with {replacementText}"
    print(message)
    outputLog(message) # Log message to output log
    return text

# Function to copy a folder from source to destination
def copyFolder(src, dst):
    import shutil
    try:
        try: # in case target folder already existant, try to remove it first
            shutil.rmtree(dst)
        except:
            pass
        shutil.copytree(src, dst) # copy folder from source to target destiantion
        message = f"[Copying Folter] Copied folder from {src} to {dst}"
    except Exception as e:
        message = f"[Copying Folter] [Error] Error copying folder: {e}"
    print(message)
    outputLog(message) # Log message to output log

# destroy GUI
def exitClicked(): # basically end the program
    dpg.stop_dearpygui()

# Function to activate and write font configuration to lv_conf.h file
def writeFontConfig (filePath, fontConfig, chosenFontSizes):
    try: 
        with open(filePath + lv_conf_filename, 'w') as file:
            fontConfigLines = fontConfig.splitlines()
            for i, line in enumerate(fontConfigLines):
                for size in [8,10,12,14,16,18,20,22,24,26,28,30,32,34,36,38,40,42,44,46,48]:
                    if f'#define LV_FONT_MONTSERRAT_{size}' in line:
                        if str(size) in chosenFontSizes:
                            fontConfigLines[i] = f'#define LV_FONT_MONTSERRAT_{size} 1'
                        else:
                            fontConfigLines[i] = f'#define LV_FONT_MONTSERRAT_{size} 0'
                    elif "#if 0" in line:
                        fontConfigLines[i] = "#if 1"
            file.write('\n'.join(fontConfigLines))
        file.close()
        message = f"[Writing File] Font configuration written to {filePath + lv_conf_filename}"
    except IOError:
        message = f"[Writing File] [Error] Error writing to configuration file {filePath}."
    print(message)
    outputLog(message)

def activateConfigFile (filePath):
    text = readFile(filePath + lvgl_header_filename)
    lines = text.splitlines()

    if f"lv_conf.h" in text:
        message = f"[Activate Config File ] Configuration file {lv_conf_filename} is already activated in lvgl.h."
    else:
        index = 17
        for i, line in enumerate(lines):
            if f"""#include "lv_conf_internal.h""" in line:
                index = i + 1
        lines.insert(index, f"""#include "{lv_conf_filename}""")
        message = f"[Activate Config File ] Configuration file {lv_conf_filename} activated in lvgl.h."
        newText = '\n'.join(lines)
        writeFile(filePath + r"\lvgl.h", newText)
    print(message)
    outputLog(message)

# execute sequence with provided paths
def executeClicked():
    # get paths
    pro_directory = dpg.get_value('pro_directory')
    lib_directory = dpg.get_value('lib_directory')
    fon_directory = dpg.get_value('fon_directory')

    # get variables for text replacement in file
    search_text = dpg.get_value('search_text')
    replace_text = dpg.get_value('replace_text')

    chosenFontSizes = []
    for i, size in enumerate([8,10,12,14,16,18,20,22,24,26,28,30,32,34,36,38,40,42,44,46,48]):
        if dpg.get_value(f'M{size}_checkbox'):
            chosenFontSizes.append(str(size))

    corruptFilePath = os.path.join(lib_directory, r"src\ui_theme_manager.c")

    # update lv_conf.h file
    fontConfig = readFile(fon_directory + lv_conf_filename)
    if fontConfig == "":
        fontConfig = readFile(fon_directory[:-4] + lv_conf_template_filename)
    writeFontConfig(fon_directory, fontConfig, chosenFontSizes)
    activateConfigFile(fon_directory)

    # execute functions
    # first copy folder to destination, then replace text in file
    copyFolder(pro_directory, lib_directory)
    file = readFile(corruptFilePath)
    newFile = replaceText(file, search_text, replace_text)
    writeFile(corruptFilePath, newFile)

    # rewrite default paths to file so they are always up to date
    file = pro_directory + "\n" + lib_directory + "\n" + fon_directory + "\n"
    writeFile(os.path.join(os.getcwd(), "defaultPaths.txt"), file)

    print("[Execution] Execution sequence completed.")

def loadStandards():
    # read default paths from file store them in variables
    filePath = os.path.join(os.getcwd(), "defaultPaths.txt")
    text = readFile(filePath)
    print(f"Read standard paths:\n{text}")

    if text != "": # if standard file existant read file lines
        lines = text.splitlines()
        numLines = len(lines)
        if numLines < 3: # if less than 3 lines, fill up with current working directory
            for _ in range(3 - numLines):
                lines.append(os.getcwd())
        defaultPath = [line.strip() for line in lines]
    else: # if not existing, create file with current working directory as default paths
        defaultPath = [os.getcwd(), os.getcwd(), os.getcwd()]
        try: # in case file does not exist, create defaultPaths.txt
            with open(file=filePath, mode="w") as file:
                for path in defaultPath:
                    file.write(path + "\n")
        except Exception as e:
            message = f"Error creating defaultPaths.txt: {e}"
            print(message)
            outputLog(message)
    return defaultPath


# read default paths from file
defaultPath = loadStandards()

# create DearPyGui context
dpg.create_context()

# UI window 1 for required file paths into input text fields
with dpg.window(label="File Paths",
                width=st.xWindowSize[0],
                height=st.yWindowSize[0],
                pos=(0,0),
                tag="filePathsWindow"):
    dpg.add_input_text(label='''Path of Square Line project 'library -> ui' folder''',
                       tag='pro_directory',
                       pos=(st.xpos[2], st.ypos[2]),
                       default_value=defaultPath[0])
    dpg.add_input_text(label='Arduino library path',
                       tag='lib_directory',
                       pos=(st.xpos[3], st.ypos[3]),
                       default_value=defaultPath[1])
    dpg.add_input_text(label='Font header file location',
                       tag='fon_directory',
                       pos=(st.xpos[9], st.ypos[9]),
                       default_value=defaultPath[2])

# UI window 2 to ender search and replace text into input text fields
with dpg.window(label="Replace incorrect text in Square Line project file",
                width=st.xWindowSize[1],
                height=st.yWindowSize[1],
                pos=(0,st.yWindowSize[0]),
                tag="replaceTextWindow"):
    dpg.add_input_text(label='Search text',
                       tag='search_text',
                       pos=(st.xpos[4], st.ypos[4]),
                       default_value="IMG",
                       width=100)
    dpg.add_input_text(label='Replace text',
                       tag='replace_text',
                       pos=(st.xpos[5], st.ypos[5]),
                       default_value="IMAGE",
                       width=100)

# UI window 3 to log output into multi line text box
with dpg.window(label="Output",
                width=st.xWindowSize[2],
                height=st.yWindowSize[2],
                pos=(0,st.yWindowSize[0] + st.yWindowSize[1]),
                tag="outputWindow"):
    dpg.add_input_text(tag='output_log_0',
                 pos=(st.xpos[6], st.ypos[6]),
                 readonly=True,
                 multiline=True,
                 no_horizontal_scroll=False,
                 width=st.xWindowSize[2]-30,
                 height=st.yWindowSize[2]-40)    

# UI window 4 to mark checkbozes and either execute or exit program
with dpg.window(label="Options",
                width=st.xWindowSize[3],
                height=st.yWindowSize[3],
                pos=(0,st.yWindowSize[0] + st.yWindowSize[1] + st.yWindowSize[2]),
                tag="buttonWindow"):
    dpg.add_button(label='EXIT',
                   tag='exit button',
                   callback=exitClicked,
                   pos=(st.xpos[0], st.ypos[0]))
    dpg.add_button(label='Execute',
                   tag='Execute library correction',
                   callback=executeClicked,
                   pos=(st.xpos[1], st.ypos[1]))
    # create checkboxes for desired font sizes
    for i, size in enumerate([8,10,12,14,16,18,20,22,24,26,28,30,32,34,36,38,40,42,44,46,48]):
        dpg.add_checkbox(label=f'M{size}',
                        tag=f'M{size}_checkbox',
                        pos=(st.xpos[10] + i * 50, st.ypos[10]))
    dpg.add_text(label='Select font sizes to include in build:',
                 pos=(st.xpos[11], st.ypos[11]),
                 show_label=True)

# Finally creating DearPyGUI viewpoint
dpg.create_viewport(title='Square Line Corrector UI',
                    width=st.guiSize_x,
                    height=st.guiSize_y,
                    x_pos=100,
                    y_pos=100)
dpg.setup_dearpygui()
dpg.show_viewport()

# Mem to activate output log (to avoid wintow exception)
UIisBuilt = True

# below replaces, start_dearpygui()
while dpg.is_dearpygui_running():
    dpg.render_dearpygui_frame()
dpg.destroy_context()