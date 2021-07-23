# --------------------------------------------------------
#  TPD_Tools 
#  by Noah Catan
#
#  menu.py
#  Version: 1.0.4
#  Last Updated: 7.5.2021
# --------------------------------------------------------

# Global Imports
import nuke


# Menus
menu = nuke.menu('Nodes')
TPD = menu.addMenu('TPD_Tools', icon="TPD_Icon.png", index=-1)

# Tools
menu.addCommand('TPD_Tools/TPD_ColorMatte', 'nuke.createNode("TPD_ColorMatte")', 'alt+m')
menu.addCommand('TPD_Tools/TPD_Grade', 'nuke.createNode("TPD_Grade")', 'alt+shift+g')
menu.addCommand('TPD_Tools/TPD_Output', 'nuke.createNode("TPD_Output")')
menu.addCommand('TPD_Tools/TPD_Prep', 'nuke.createNode("TPD_Prep")')

# Import Python Scripts
import TPD_Roto
import TPD_ColorPalette
import TPD_AutoCrop


# Import Experimental Python Scripts
import TPD_UpdateDIP
import TPD_DIPSetup
import TPD_TextureTrack
