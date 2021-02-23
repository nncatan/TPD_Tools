# --------------------------------------------------------
#  TPD_Tools 
#  by Noah Catan
#
#  menu.py
#  Version: 1.0.1
#  Last Updated: 12.09.2020
# --------------------------------------------------------

# Global Imports
import nuke


# Menus
menu = nuke.menu('Nodes')
TPD = menu.addMenu('TPD_Tools', icon="TPD_Icon.png", index=-1)


# Import Python Scripts
import TPD_Roto
import TPD_ColorPalette
import TPD_DIPSetup