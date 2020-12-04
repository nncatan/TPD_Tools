# -------------------------------------------------------------
#  TPD_Roto
#  by Noah Catan
#
#  TDP_Roto.py
#  Version: 1.0.2
#  Last Updated: 12.04.2020
# -------------------------------------------------------------

import nuke

def Create_TPD_Roto():

	# Create TPD_Roto
	n = nuke.createNode('TPD_Roto')

	# Check if previous connection is another TPD_Roto. If yes, set lightPass to the same value
	if n.inputs() > 0:
		if n.input(0).knob('lightPass'):
			n.knob('lightPass').setValue(int(n.input(0).knob('lightPass').getValue()))

	n.begin() # Open the group

	# Open TPD_ROTO_IN_GRP and then close it
	r = nuke.toNode('TPD_ROTO_IN_GRP')
	if nuke.toNode('preferences').knob('maxPanels').value() <= 1:
		nuke.toNode('preferences').knob('maxPanels').setValue(2)
		nuke.show(r)
		r.hideControlPanel()
		nuke.toNode('preferences').knob('maxPanels').setValue(1)
	else:
		nuke.show(r)
		r.hideControlPanel()

	n.end() # Close the group
	
	n.knob('selected').setValue(True)
	nuke.show(n)

def Reload_TPD_Roto():

	n = nuke.thisNode()
	
	n.begin() # Open the group

	# Open TPD_ROTO_IN_GRP and then close it
	r = nuke.toNode('TPD_ROTO_IN_GRP')
	if nuke.toNode('preferences').knob('maxPanels').value() <= 1:
		nuke.toNode('preferences').knob('maxPanels').setValue(2)
		nuke.show(r)
		r.hideControlPanel()
		nuke.toNode('preferences').knob('maxPanels').setValue(1)
	else:
		nuke.show(r)
		r.hideControlPanel()

	n.end() # Close the group
	
	n.knob('selected').setValue(True)
	nuke.show(n)


nuke.menu('Nodes').addCommand('TPD_Tools/TPD_Roto', 'TPD_Roto.Create_TPD_Roto()', 'alt+o', icon=None)