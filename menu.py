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
#  KNOB DEFAULTS ::::::::::::::::::::::::::::::::::::::::::::::
# -------------------------------------------------------------

# ----- TRACKER -------------------
nuke.knobDefault('Tracker4.shutteroffset', "centered")
nuke.knobDefault('Tracker4.label', "Motion: [value transform]\nRef Frame: [value reference_frame]")
nuke.addOnUserCreate(lambda:nuke.thisNode()['reference_frame'].setValue(nuke.frame()), nodeClass='Tracker4')

# ----- SHUFFLES -------------------
nuke.knobDefault('Shuffle.label', "[value in]")
nuke.knobDefault('ShuffleCopy.label', "[value in]")

# ----- COLORSPACE -------------------
nuke.knobDefault('Colorspace.label', "[value colorspace_in] > [value colorspace_out]")

# ----- FRAMEHOLD -------------------
nuke.addOnUserCreate(lambda:nuke.thisNode()['first_frame'].setValue(nuke.frame()), nodeClass='FrameHold')

# ----- ZDEFOCUS ---------------
nuke.knobDefault('ZDefocus2.math', "depth")

# ----- MOTION BLUR SHUTTER CENTERED ---------------
nuke.knobDefault('Tracker4.shutteroffset', "centered")
nuke.knobDefault('TimeBlur.shutteroffset', "centered")
nuke.knobDefault('Transform.shutteroffset', "centered")
nuke.knobDefault('TransformMasked.shutteroffset', "centered")
nuke.knobDefault('CornerPin2D.shutteroffset', "centered")
nuke.knobDefault('MotionBlur2D.shutteroffset', "centered")
nuke.knobDefault('MotionBlur3D.shutteroffset', "centered")
nuke.knobDefault('ScanlineRender.shutteroffset', "centered")
nuke.knobDefault('Card3D.shutteroffset', "centered")





# -------------------------------------------------------------
#  TOOLS ::::::::::::::::::::::::::::::::::::::::::::::::::::::
# -------------------------------------------------------------


# ----- MENU ----------------------------

nuke.menu('Nodes').addMenu('TPD_Tools', icon="Rectangle.png")




# ----- GIZMOS ----------------------------

import TPD_Roto
