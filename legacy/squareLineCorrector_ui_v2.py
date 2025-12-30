import dearpygui.dearpygui as dpg
import settings as st
import os

outputMessages = []
UIisBuilt = False


def outputLog(message):
    try:
        outputMessages.insert(0, message)
        if len(outputMessages) > 3:
            outputMessages.pop(3)
        # only update GUI if dpg is fully built, else context/items may not yet exist and program will crash
        if UIisBuilt:
            dpg.set_value('output_log_0', outputMessages[0] if len(outputMessages) > 0 else "")
            dpg.set_value('output_log_1', outputMessages[1] if len(outputMessages) > 1 else "")
            dpg.set_value('output_log_2', outputMessages[2] if len(outputMessages) > 2 else "")
    except Exception as e:
        print(f"Error updating output log: {e}")

# Function to read a file
def readFile (path):
    try:
        with open (path, 'r') as file:
            message = f"File successfully opened with path: {path}"
            text = file.read()
            file.close()
    except Exception as e:
        message = f"File could NOT be opened with path {path}\nException: {e}"
        text = ""
    print(message)
    outputLog(message)
    return text

# Function to write text to a file
def writeFile (path, text):
    try:
        with open (path, 'w') as file:
            file.write(text)
            message = f"Writing file was successful with path {path}"
            file.close()
    except Exception as e:
        message = f"Writing of file was NOT successful with path {path}\nException: {e}"
    print(message)
    outputLog(message)

# Function to replace specific text
def replaceText(text, searchText, replacementText):
    if searchText not in text:
        message = f"'{searchText}' not found in text."
    else:
        text = text.replace(searchText, replacementText)
        message = f"{searchText} has been replaced with {replacementText}"
    print(message)
    outputLog(message)
    return text

# Function to copy a folder from source to destination
def copyFolder(src, dst):
    import shutil
    try:
        # in case target folder already existant, folder will be deleted
        try:
            shutil.rmtree(dst)
        except:
            pass
        # copy folder from source to target destiantion
        shutil.copytree(src, dst)
        message = f"Copied folder from {src} to {dst}"
    except Exception as e:
        message = f"Error copying folder: {e}"
    print(message)
    outputLog(message)

# destroy GUI
def exitClicked():
    dpg.stop_dearpygui()

# execute sequence with provided paths
def executeClicked():
    # get paths
    pro_directory = dpg.get_value('pro_directory')
    lib_directory = dpg.get_value('lib_directory')

    # get variables for text replacement in file
    search_text = dpg.get_value('search_text')
    replace_text = dpg.get_value('replace_text')

    corruptFilePath = os.path.join(lib_directory, r"src\ui_theme_manager.c")

    # execute functions
    # first copy folder to destination, then replace text in file
    copyFolder(pro_directory, lib_directory)
    file = readFile(corruptFilePath)
    newFile = replaceText(file, search_text, replace_text)
    writeFile(corruptFilePath, newFile)

    # rewrite default paths to file so they are always up to date
    file = pro_directory + "\n" + lib_directory + "\n"
    writeFile(os.path.join(os.getcwd(), "defaultPaths.txt"), file)

def loadStandards():
    # read default paths from file store them in variables
    filePath = os.path.join(os.getcwd(), "defaultPaths.txt")
    text = readFile(filePath)
    print(f"Read standard paths:\n{text}")

    if text != "": # if standard file existant read file lines
        lines = text.splitlines()
        defaultPath = [line.strip() for line in lines]
    else: # if not existing, create file with current working directory as default paths
        defaultPath = [os.getcwd(), os.getcwd()]
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

# UI window
with dpg.window(label="Make Libraries Great Again",
                width=st.windowSize_x,
                height=st.windowSize_y,
                pos=(0,0),
                tag="error log"):
    dpg.add_button(label='EXIT',
                   tag='exit button',
                   callback=exitClicked,
                   pos=(st.xpos_item_1, st.ypos_item_1))
    dpg.add_button(label='Execute',
                   tag='Execute library correction',
                   callback=executeClicked,
                   pos=(st.xpos_item_2, st.ypos_item_2))
    dpg.add_input_text(label='''Path of Square Line project 'library -> ui' folder''',
                       tag='pro_directory',
                       pos=(st.xpos_item_3, st.ypos_item_3),
                       default_value=defaultPath[0])
    dpg.add_input_text(label='Arduino library path',
                       tag='lib_directory',
                       pos=(st.xpos_item_4, st.ypos_item_4),
                       default_value=defaultPath[1])
    dpg.add_input_text(label='Search text',
                       tag='search_text',
                       pos=(st.xpos_item_5, st.ypos_item_5),
                       default_value="IMG")
    dpg.add_input_text(label='Replace text',
                       tag='replace_text',
                       pos=(st.xpos_item_6, st.ypos_item_6),
                       default_value="IMAGE")
    dpg.add_text(label=': Output log 1',
                 tag='output_log_0',
                 pos=(st.xpos_item_7, st.ypos_item_7))
    dpg.add_text(label=': Output log 2',
                 tag='output_log_1',
                 pos=(st.xpos_item_8, st.ypos_item_8))
    dpg.add_text(label=': Output log 3:',
                 tag='output_log_2',
                 pos=(st.xpos_item_9, st.ypos_item_9))

dpg.create_viewport(title='Square Line Corrector UI',
                    width=st.guiSize_x,
                    height=st.guiSize_y,
                    x_pos=1000,
                    y_pos=100)
dpg.setup_dearpygui()
dpg.show_viewport()

UIisBuilt = True

# below replaces, start_dearpygui()
while dpg.is_dearpygui_running():

    dpg.render_dearpygui_frame()
dpg.destroy_context()