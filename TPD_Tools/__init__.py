# --------------------------------------------------------
#  TPD_Tools 
#  by Noah Catan
#
#  init.py
#  Version: 1.0.0
#  Last Updated: 12.04.2020
# --------------------------------------------------------

import nuke


# ----- DEFINE CUSTOM FOLDER STRUCTURE -------------------

nuke.pluginAddPath('./TPD_Tools/gizmos')
nuke.pluginAddPath('./TPD_Tools/icons')
nuke.pluginAddPath('./TPD_Tools/python')
nuke.pluginAddPath('./TPD_Tools/templates')

import TPD_Menu
import TPD_Roto
