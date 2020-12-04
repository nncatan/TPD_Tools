# --------------------------------------------------------
#  TPD_Tools 
#  by Noah Catan
#
#  menu.py
#  Version: 1.0.0
#  Last Updated: 12.04.2020
# --------------------------------------------------------

# -------------------------------------------------------------
#  GLOBAL IMPORTS :::::::::::::::::::::::::::::::::::::::::::::
# -------------------------------------------------------------

import os
import nuke
import platform
import nukescripts




# -------------------------------------------------------------
#  DIRECTORY ::::::::::::::::::::::::::::::::::::::::::::::::::
# -------------------------------------------------------------

# Define username
User = os.environ['USERNAME']

# Define where .nuke directory is on each OS's network
Win_Dir = 'C:\\Users\\' + User + '\\.nuke'
MacOSX_Dir = '/Users/' + User + '/.nuke'
Linux_Dir = '/home/' + User + '/.nuke'

# Set global directory
if platform.system() == "Windows":
	dir = Win_Dir
	templates_dir = Win_Dir + '\\NC_nuke\\templates\\'
elif platform.system() == "Darwin":
	dir = MacOSX_Dir
	templates_dir = MacOSX_Dir + '/NC_nuke/templates/'
elif platform.system() == "Linux":
	dir = Linux_Dir
	templates_dir = Linux_Dir + '/NC_nuke/templates/'
else:
	dir = None



# -------------------------------------------------------------
#  TOOLS ::::::::::::::::::::::::::::::::::::::::::::::::::::::
# -------------------------------------------------------------


# ----- MENU ----------------------------

nuke.menu('Nodes').addMenu('TPD_Tools', icon="Rectangle.png")




# ----- GIZMOS ----------------------------

import TPD_Roto
