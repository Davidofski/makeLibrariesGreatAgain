# settigns for window

guiSize_x = 1300

xWindowSize = [0,0,0,0]
yWindowSize = [0,0,0,0]
xWindowSize[0] = guiSize_x - 16
yWindowSize[0] = 140    
xWindowSize[1] = guiSize_x - 16
yWindowSize[1] = 70
xWindowSize[2] = guiSize_x - 16
yWindowSize[2] = 200
xWindowSize[3] = guiSize_x - 16
yWindowSize[3] = 70

guiSize_y = int((yWindowSize[0] + yWindowSize[1] + yWindowSize[2] + yWindowSize[3]) * 1.14)

# offset for items
xoffset = 10
yoffset = 30

# define container for item positions
num_items = 14
xpos = []
ypos = []
for i in range(num_items):
    xpos.append(0)
    ypos.append(0)

# Button Exit
xpos[0] = xoffset
ypos[0] = yoffset * 2
# Button Execute
xpos[1] = xoffset + 50
ypos[1] = yoffset * 2
# Input Project Directory
xpos[2] = xoffset
ypos[2] = yoffset
# Input Library Directory
xpos[3] = xoffset
ypos[3] = yoffset * 2
# Input Search Text
xpos[4] = xoffset
ypos[4] = yoffset
# Input Replace Text
xpos[5] = xoffset + 300
ypos[5] = yoffset
# Output Log 1
xpos[6] = xoffset
ypos[6] = yoffset
# Reserve
xpos[7] = xoffset
ypos[7] = yoffset * 2
# Reserve
xpos[8] = xoffset
ypos[8] = yoffset * 3
# Input text font header file location
xpos[9] = xoffset
ypos[9] = yoffset * 3
# Checkbox for font size
xpos[10] = xoffset + 150
ypos[10] = yoffset * 2
# header for font size
xpos[11] = xoffset - 300
ypos[11] = yoffset
# Reserve
xpos[12] = xoffset 
ypos[12] = yoffset * 4
# Reserve
xpos[13] = xoffset
ypos[13] = yoffset * 5