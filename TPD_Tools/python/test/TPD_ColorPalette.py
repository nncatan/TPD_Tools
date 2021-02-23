# --------------------------------------------------------
#  TPD_Tools
#  by Noah Catan
#
#  TPD_ColorPalette.py
#  Version: 1.0.3
#  Last Updated: 12.09.2020
# --------------------------------------------------------

import os
import sys
import nuke
import nukescripts
from PySide2 import *
from PySide2.QtCore import *


#import TPD_LightPassNodes

'''
# List of light passes
lightPasses = [
'Shadow',
'Key_Light',
'AO',
'Secondary',
'Ambient',
'Custom',
'Translucent',
'SSS_Skin',
'SSS_Rest',
'Specular',
'Rim_Light']

characters = ['Pope', 'Dog', 'Guard']

lightPassesMultiply = ['AO']
'''
#lightPasses = []
#lightPassesMultiply = []

characters = ['Pope', 'Dog', 'Guard']

rgbaLayers = ['DIP']

# -----------------------------------------------------------------------------------------------------------------------------------------------------------------
#  READ LIGHT PASS TXT FILE :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# -----------------------------------------------------------------------------------------------------------------------------------------------------------------


lightPasses = []
lightPassesMultiply = []
myDir = os.path.dirname(__file__)
lplist = os.path.join(myDir, "../lightPasses.txt")

with open(lplist) as f:
    lines = f.read().splitlines()

for line in lines:
    if line is not '':
        if '*' in line:
            line = line.replace('*', '')
            lightPasses.append(line)
            lightPassesMultiply.append(line)
        else:
            lightPasses.append(line)

#print lightPasses
#print lightPassesMultiply         




# -----------------------------------------------------------------------------------------------------------------------------------------------------------------
#  COLOR CONVERSIONS ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# -----------------------------------------------------------------------------------------------------------------------------------------------------------------


def hex2dec(hex_string):
    """
        return the integer value of a hexadecimal string     ----  Code by Robin Dutta1
    """
    if hex_string.startswith("#"):
        hex_string = hex_string[1:]
    if len(hex_string) == 3:
        hex_string = hex_string[0] + hex_string[0] + hex_string[1] + hex_string[1] + hex_string[2] + hex_string[2]
    if len(hex_string) == 6:
        hex_string += "FF"
    return int(hex_string, 16)


def hex2rgba(hexValue):
    '''
        returns the RGBA values of a hexadecimal string      ----  Code by Erwan Leroy
    '''
    hex =  '%08x' % hexValue
    rgba = [
    float(int(hex[0:2], 16))/255.0,
    float(int(hex[2:4],16))/255.0,
    float(int(hex[4:6], 16))/255.0,
    float(int(hex[6:8],16))/255.0]
    return rgba





# -----------------------------------------------------------------------------------------------------------------------------------------------------------------
#  COLOR PALETTE PANEL ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# -----------------------------------------------------------------------------------------------------------------------------------------------------------------


class ColorPalette(QtWidgets.QWidget):
    def __init__(self, parent=None):
        '''
            Creates the panel
        '''
        super(ColorPalette, self).__init__()
        #self.setWindowTitle('ColorPallete')
        
        
        self.master_layout = QtWidgets.QVBoxLayout()
        self.master_layout.setSpacing(0)
        self.master_layout.setMargin(0)

        # Create master tab layout
        self.allTabs = QtWidgets.QTabWidget()

        '''
        for c in characters:
            self.create_tab(c)
        '''
        self.create_tab('Color')

        self.master_layout.addWidget(self.allTabs)
        self.setLayout(self.master_layout)

    def makeUI(self):
        return self

    def create_tab(self, name):
        
        name_str = str(name)
        name = QtWidgets.QGroupBox()

        self.allTabs.addTab(name, name_str)
        self.create_tab_ui(name, name_str)

        
        
    def create_tab_ui(self, tab, name):

        layout = QtWidgets.QHBoxLayout()

        lpColors = QtWidgets.QWidget()
        lpColors_layout = QtWidgets.QVBoxLayout()
        lpColors_layout.setSpacing(0)
        lpColors_layout.setMargin(0)
        self.create_row('Shadow', lpColors_layout)
        for lp in lightPasses:
            self.create_row(lp, lpColors_layout)
        lpColors.setLayout(lpColors_layout)

        # Add columns to Color Tab
        layout.addWidget(lpColors)
        layout.setSpacing(0)
        layout.setMargin(20)
        #layout.setAlignment(Qt.AlignTop)
        #layout.addWidget(lpNames)
        #layout.addWidget(lpSliders)
        tab.setLayout(layout)
       
 
    def create_row(self, name, layout):
        row = QtWidgets.QWidget()
        row_layout = QtWidgets.QHBoxLayout()
        row_layout.setMargin(5)
        self.create_colorButton('self.{}'.format(name), 'black', row_layout)
        print 'created button ' + name
        self.create_label('self.{}'.format(name), row_layout)
        print 'created label ' + name
        self.create_slider('self.{}'.format(name), 100, row_layout)
        print 'created slider '+ name
        row.setLayout(row_layout)
        layout.addWidget(row)


    def create_colorButton(self, name, color, layout):
        '''
            Creates an button with a color
        '''
        name_str = str(name)[5:]
        #print name_str
        name = QtWidgets.QPushButton()
        name.setFixedSize(30,15)
        name.setStyleSheet("background-color: {}".format(color))
        name.clicked.connect(lambda: self.colorButton_clicked(name, name_str))
        layout.addWidget(name)


    def colorButton_clicked(self, name, name_str):
        '''
            When the color button is clicked, open the color dialog and change the button to the chosen color
        '''
        color = QtWidgets.QColorDialog.getColor()
        if color.isValid():
            name.setStyleSheet("background-color: {}".format(color.name()))
            #self.check_for_gradeNode(name_str, color)


    def create_label(self, name, layout):
        name = QtWidgets.QLabel(str(name)[5:])
        name.setFixedSize(75,20)
        layout.addWidget(name)

    def create_slider(self, name, input, layout):
        '''
            Creates a slider
        '''
        name = QtWidgets.QSlider(Qt.Horizontal, self)
        name.setRange(0, 100)
        name.setValue(input)
        name.setFixedSize(100, 20)

        # Check if value is correct
        #valueLabel = QtWidgets.QLabel(str(input*.01))
        #name.valueChanged.connect(lambda: valueLabel.setText(str(name.value()*.01)))

        layout.addWidget(name)
        #layout.addWidget(valueLabel)

'''
    def check_for_gradeNode(self, name, color):
        print color.rgba()
        if nuke.toNode('TPD_LightPasses') is not None:
            grp = nuke.toNode('TPD_LightPasses')
            grp.begin()
            print 'Group Found: ' + str(grp['name'].value())

            if nuke.toNode('{}_LIGHT'.format(name.upper())) is not None:
                rgba = hex2rgba(hex2dec(color.name()))
                grade = nuke.toNode('{}_LIGHT'.format(name).upper())
                grade.knob('white').setValue(rgba)
                print 'Grade Found: ' + str(grade['name'].value())

'''

class ColorPalettePane(ColorPalette):
    def __init__(self, node = "", knob="knobChanged"):
        super(ColorPalettePane, self).__init__()
        self.isPane = True



def addColorPalettePanel():
    global colorPalettePanel
    try: 
        colorPalettePanel = nukescripts.registerWidgetAsPanel('nuke.ColorPalettePane', 'Color Palette', 'ColorPalettePane')
        colorPalettePanel.addToPane(nuke.getPaneFor('Properties.1'))
    except:
        colorPalettePanel = nukescripts.registerWidgetAsPanel('nuke.ColorPalettePane', 'Color Palette', 'ColorPalettePane')




# -----------------------------------------------------------------------------------------------------------------------------------------------------------------
#  CREATE LAYERS ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# -----------------------------------------------------------------------------------------------------------------------------------------------------------------



def create_lp_layer(lpass):
    '''
        Creates an alpha layer based on a Light Pass List item
    '''

    lpass = nuke.Layer('LGHT_{}'.format(lpass.upper()), ['LGHT_{}.alpha'.format(lpass.upper())])
    #print lpass



def create_rgba_layer(lpass):
    '''
        Creates an rgba layer
    '''

    lpass = nuke.Layer('{}'.format(lpass.upper()), ['{}.red'.format(lpass.upper()), '{}.green'.format(lpass.upper()), '{}.blue'.format(lpass.upper()), '{}.alpha'.format(lpass.upper())])
    #print lpass



def create_layers():
    '''
        Creates layers from the the Light Passes List and other custom layers
    '''

    # Create passes for all the items in the RGBA Layers List
    for l in rgbaLayers:
        create_rgba_layer(l)

    # Create a layer for all the items in the Light Passes List
    for lp in lightPasses:
        create_lp_layer(lp)





# -----------------------------------------------------------------------------------------------------------------------------------------------------------------
#  CREATE LIGHT PASS NODES ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# -----------------------------------------------------------------------------------------------------------------------------------------------------------------




def create_lp_nodes(lpass, node):
    '''
        Creates a nodes for a single light pass
    '''

    #clear selection
    nukescripts.clear_selection_recursive()

    # Get parent_dot's position
    parent_dot = node
    x = parent_dot.xpos()
    y = parent_dot.ypos()

    #store nodes in a list
    nodes_created = []

    #node_Dot_2
    node_Dot_2 = nuke.nodes.Dot(xpos=0+x,ypos=81+y,inputs=[parent_dot])
    node_Dot_2['name'].setValue('DOT2_{}'.format(lpass.upper()))
    nodes_created.append(node_Dot_2)
    
    #node_Shuffle_1 - LIGHT PASS
    node_Shuffle_1 = nuke.nodes.Shuffle(xpos=-34+x,ypos=157+y,inputs=[node_Dot_2])
    node_Shuffle_1['name'].setValue('SHUFFLE_{}'.format(lpass.upper()))
    node_Shuffle_1['in'].fromScript('LGHT_{}'.format(lpass.upper()))
    node_Shuffle_1['label'].setValue('[value in]')
    node_Shuffle_1['red'].fromScript('black')
    node_Shuffle_1['green'].fromScript('black')
    node_Shuffle_1['blue'].fromScript('black')
    nodes_created.append(node_Shuffle_1)
    
    #node_Shuffle_2 - DIP ALPHA
    node_Shuffle_2 = nuke.nodes.Shuffle(xpos=90+x,ypos=72+y,inputs=[node_Dot_2])
    node_Shuffle_2['in'].fromScript('DIP')
    node_Shuffle_2['label'].setValue('[value in]')
    node_Shuffle_2['red'].fromScript('white')
    node_Shuffle_2['green'].fromScript('white')
    node_Shuffle_2['blue'].fromScript('white')
    nodes_created.append(node_Shuffle_2)
    
    #node_Grade_1      LIGHT
    node_Grade_1 = nuke.nodes.Grade(xpos=182+x,ypos=113+y,inputs=[node_Shuffle_2])
    node_Grade_1['name'].setValue('{}_LIGHT'.format(lpass.upper()))
    node_Grade_1['white'].setValue([0.0, 0.0, 0.0, 0.0])
    node_Grade_1['label'].setValue('LIGHT')
    nodes_created.append(node_Grade_1)
    
    #node_Grade_2      SHADOW
    node_Grade_2 = nuke.nodes.Grade(xpos=90+x,ypos=113+y,inputs=[node_Shuffle_2])
    node_Grade_2['name'].setValue('{}_SHADOW'.format(lpass.upper()))
    if lpass in lightPassesMultiply:
        node_Grade_2['white'].setValue([1.0,1.0,1.0,1.0])
    elif lightPasses.index(lpass)<=0:
        node_Grade_2['white'].setValue([0.2, 0.2, 0.2, 0.2])
    else:
        node_Grade_2['white'].setValue([0.0, 0.0, 0.0, 0.0])
    node_Grade_2['label'].setValue('SHADOW')
    nodes_created.append(node_Grade_2)
    
    #node_Keymix_1
    node_Keymix_1 = nuke.nodes.Keymix(xpos=90+x,ypos=157+y,inputs=[node_Grade_2,node_Grade_1,node_Shuffle_1])
    node_Keymix_1['name'].setValue('{}_KEYMIX'.format(lpass.upper()))
    node_Keymix_1['channels'].fromScript('rgb')
    nodes_created.append(node_Keymix_1)

    #node_Merge_1
    if lightPasses.index(lpass) > 0:
        node_Merge_1 = nuke.nodes.Merge2(xpos=90+x,ypos=250+y,inputs=[None, node_Keymix_1])
        node_Merge_1['name'].setValue('{}_MERGE'.format(lpass.upper()))
        node_Merge_1['Achannels'].setValue('rgb')
        node_Merge_1['Bchannels'].setValue('rgb')
        node_Merge_1['output'].setValue('rgb')
        if lpass in lightPassesMultiply:
            node_Merge_1['operation'].setValue('multiply')
        else:
            node_Merge_1['operation'].setValue('plus')




def create_lp_tree(lightPassesList, inputNode):
    '''
        Creates an node tree of light pass nodes, links them together with dots and merges
    '''

    # Set initial dot and previous dot
    node = inputNode
    prev_node = node
    merge_list = []
    merge = None

    # For every item in the Light Passes List...
    for lp in lightPassesList:
        # If the list index is 1, create a light pass tree connected to the first dot.
        if lightPassesList.index(lp) == 0:
            if lp not in lightPassesMultiply:
                # Create Light Pass Nodes
                create_lp_nodes(lp, node)
        
        # If the list index is equal or greater than 2, create a light pass tree and connect it to a new dot.
        elif lightPassesList.index(lp) >= 1:
            if lp not in lightPassesMultiply:
                # Set position of and create a new dot
                x, y = prev_node.xpos(), prev_node.ypos()
                node = nuke.nodes.Dot(xpos=350+x,ypos=0+y,inputs=[prev_node])
                prev_node = node
                
                # Create Light Pass Nodes
                create_lp_nodes(lp, node)
                
                # Link merge node to previous merge node
                merge = nuke.toNode('{}_MERGE'.format(lp.upper()))
                merge.setInput(0, nuke.toNode('{}_MERGE'.format(lightPassesList[lightPassesList.index(lp)-1].upper())))
                merge_list.append(merge)


    for lp in lightPassesMultiply:
        if lp in lightPassesList:
            # Set position of and create a new dot
            x, y = prev_node.xpos(), prev_node.ypos()
            node = nuke.nodes.Dot(xpos=350+x,ypos=0+y,inputs=[prev_node])
            prev_node = node

            # Create Light Pass Nodes
            create_lp_nodes(lp, node)

            # Link merge node to previous merge node
            total_lp_items = len(lightPassesList)
            merge = nuke.toNode('{}_MERGE'.format(lp.upper()))
            if lightPassesMultiply.index(lp) == 0:
                merge.setInput(0, nuke.toNode('{}_MERGE'.format(lightPassesList[len(lightPassesList)-1].upper())))
                merge_list.append(merge)
            else:
                merge.setInput(0, nuke.toNode('{}_MERGE'.format(lightPassesMultiply[lightPassesMultiply.index(lp)-1].upper())))
                merge_list.append(merge)

    
    # Creates the last set of nodes that multiplies all the lightpasses with the DIP pass
    x, y = prev_node.xpos(), prev_node.ypos()
    dot1        = nuke.nodes.Dot        (xpos=384+x,ypos=0+y, inputs=[prev_node])
    shuffle1    = nuke.nodes.Shuffle    (xpos=350+x, ypos=72+y, inputs=[dot1])
    unpremult1  = nuke.nodes.Unpremult  (xpos=350+x, ypos=108+y, inputs=[shuffle1])
    blur        = nuke.nodes.Blur       (xpos=225+x, ypos=250+y, inputs=[merge])
    merge1      = nuke.nodes.Merge2     (xpos=350+x, ypos=250+y, inputs=[unpremult1, blur])
    premult     = nuke.nodes.Premult    (xpos=350+x, ypos=300+y, inputs=[merge1])
    output      = nuke.nodes.Output     (xpos=350+x, ypos=350+y, inputs=[premult])
    
    shuffle1['in'].setValue('DIP')
    shuffle1['label'].setValue('[value in]')
    blur['channels'].setValue('rgb')
    blur['size'].setValue(2)
    merge1['operation'].setValue('multiply')
    merge1['Achannels'].setValue('rgb')
    merge1['Bchannels'].setValue('rgb')
    merge1['output'].setValue('rgb')

    connect_first_merge_node()


def connect_first_merge_node():
    '''
        Attach the first merge node's B input to the first Keymix node.
    '''
    first_in_pipe = nuke.toNode('{}_KEYMIX'.format(lightPasses[0].upper()))
    for i in range(1, len(lightPasses)):
        if lightPasses[i] not in lightPassesMultiply:
            first_merge = nuke.toNode('{}_MERGE'.format(lightPasses[i].upper()))
            first_merge.setInput(0, first_in_pipe)
            return



def create_lp_group():
    '''
        Wraps the whole thing inside a group node
    '''
    lp_group = nuke.createNode('Group', inpanel=False)
    lp_group['name'].setValue('TPD_LightPasses')

    with lp_group:

        inpt = nuke.nodes.Input()
        x, y = inpt.xpos(), inpt.ypos()

        dot1 = nuke.nodes.Dot(xpos=34+x, ypos=100+y, inputs=[inpt])

        create_lp_tree(lightPasses, dot1)

    knob = nuke.PyCustom_Knob("TPD_ColorPalette", 'ColorPalette', 'ColorPalette()')
    lp_group.addKnob(knob)
 

def start():
    #read_lightPass_txt()
    create_layers()
    create_lp_group()


    #start.panel = ColorPalette()
    #start.panel.show()

#nuke.ColorPalettePane = ColorPalettePane
#addColorPalettePanel()
nuke.menu('Nodes').addCommand('TPD_Tools/TPD_ColorPalette', 'TPD_ColorPalette.start()', shortcut='ctrl+shift+alt+o')