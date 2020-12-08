# --------------------------------------------------------
#  TPD_Tools
#  by Noah Catan
#
#  TPD_ColorPalette.py
#  Version: 1.0.2
#  Last Updated: 12.08.2020
# --------------------------------------------------------

import sys
import nuke
from PySide2 import *#QtWidgets, QtGui, QtCore
from PySide2.QtCore import *#Qt
#from collections import OrderedDict

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

charactersInScene = ['Pope', 'Dog']


class Panel(QtWidgets.QWidget):
    def __init__(self):
        '''
        Creates the panel
        '''
        super(Panel, self).__init__()
        self.title = 'TPD_ColorPalette'
        self.setWindowTitle(self.title)
        
        

        
        # Create Color Tab
        colorTab = QtWidgets.QGroupBox('Color Palette')
        colorTab_layout = QtWidgets.QHBoxLayout()
        
        
        # Create column of light pass color buttons
        lpColors = QtWidgets.QWidget()
        lpColors_layout = QtWidgets.QVBoxLayout()
        for lp in lightPasses:
            self.create_colorButton('self.{}'.format(lp), 'black', lpColors_layout)
        lpColors.setLayout(lpColors_layout)
        
        
        # Create column of light pass names
        lpNames = QtWidgets.QWidget()
        lpNames_layout = QtWidgets.QVBoxLayout()
        for lp in lightPasses:
            lpName = QtWidgets.QLabel(lp)
            lpNames_layout.addWidget(lpName)
        lpNames.setLayout(lpNames_layout)
    
    
        # Create column of light pass sliders
        lpSliders = QtWidgets.QWidget()
        lpSliders_layout = QtWidgets.QVBoxLayout()
        for lp in lightPasses:
            self.create_slider("self.{}".format(lp), 100, lpSliders_layout)
        lpSliders.setLayout(lpSliders_layout)
        
        
        # Add columns to Color Tab
        colorTab_layout.addWidget(lpColors)
        colorTab_layout.addWidget(lpNames)
        colorTab_layout.addWidget(lpSliders)
        colorTab.setLayout(colorTab_layout)
        
        
        # Define master layout and add Color Tab to it    
        master_layout = QtWidgets.QVBoxLayout()
        master_layout.addWidget(colorTab)
        self.setLayout(master_layout)
        
       
    def create_colorButton(self, name, color, layout):
        '''
        Creates an button with a color
        '''
        name = QtWidgets.QPushButton()
        name.setStyleSheet("background-color: {}".format(color))
        name.clicked.connect(lambda: self.colorButton_clicked(name))
        layout.addWidget(name)


    def colorButton_clicked(self, name):
        '''
        When the color button is clicked, open the color dialog and change the button to the chosen color
        '''
        color = QtWidgets.QColorDialog.getColor()
        if color.isValid():
            name.setStyleSheet("background-color: {}".format(color.name()))


    def create_slider(self, name, input, layout):
        '''
        Creates a slider
        '''
        name = QtWidgets.QSlider(Qt.Horizontal, self)
        name.setRange(0, 100)
        name.setValue(100)

        # Check if value is correct
        valueLabel = QtWidgets.QLabel(str(input*.01))
        name.valueChanged.connect(lambda: valueLabel.setText(str(name.value()*.01)))

        layout.addWidget(name)
        layout.addWidget(valueLabel)

        
   

def start():
    start.panel = Panel()
    start.panel.show()
    
start()
