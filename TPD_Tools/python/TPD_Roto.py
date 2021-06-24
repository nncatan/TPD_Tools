# -------------------------------------------------------------
#  TPD_Roto
#  by Noah Catan
#
#  TDP_Roto.py
#  Version: 1.0.4
#  Last Updated: 06.24.2021
# -------------------------------------------------------------

import nuke



def Create_TPD_Roto():
	'''
		Creates the TPD_Roto node
	'''

	# Create TPD_Roto
	n = nuke.createNode('TPD_Roto')

	# Check if previous connection is another TPD_Roto. If yes, set lightPass to the same value
	if n.inputs() > 0:
		if n.input(0).knob('lightPass'):
			n.knob('lightPass').setValue(int(n.input(0).knob('lightPass').getValue()))

	Open_Close_Roto(n)
	
	n.knob('selected').setValue(True)
	nuke.show(n)




def Reload_TPD_Roto():
	'''
		Reloads TPD_Roto. This function is connected to the "Refresh" button on TPD_Roto
		A user can click that button if roto transform box is still hidden
	'''

	n = nuke.thisNode()
	Open_Close_Roto(n)




def Open_Close_Roto(TPDRotoNode):
	'''
		Opens and closes TPD_Roto node, to fix the weird bug that hides the roto transform box
	'''
	
	# Open the group
	TPDRotoNode.begin() 
	
	roto = nuke.toNode('TPD_ROTO_IN_GRP')

	# Find the 'maxPanels' value from the Preferences tab and add 1
	prefs = nuke.toNode('preferences').knob('maxPanels')
	prefs.setValue(prefs.value()+1)

	# Open and close the roto node
	nuke.show(roto)
	roto.hideControlPanel()

	# Set the 'maxPanels' value back to normal
	prefs.setValue(prefs.value()-1)
	
	# Close the group
	TPDRotoNode.end() 



nuke.menu('Nodes').addCommand('TPD_Tools/TPD_Roto', 'TPD_Roto.Create_TPD_Roto()', 'alt+o', icon=None)