# -------------------------------------------------------------
#  TPD_AutoCrop
#  by Noah Catan
#
#  TDP_AutoCrop.py
#  Version: 1.0.1
#  Last Updated: 7.5.2021
# -------------------------------------------------------------

import nuke, nukescripts

def AutoCrop():

	node = nuke.selectedNode()

	first_frame = int(nuke.Root()['first_frame'].getValue())
	last_frame = int(nuke.Root()['last_frame'].getValue())


	if node.knob("desc"):
	    label = node.knob("desc").value()
	else:
	    label = node.knob("label").value()

	p = nuke.Panel("Execute on FrameRange")
	p.addSingleLineInput('Label', label)
	p.addSingleLineInput('Layer', "alpha")
	p.addSingleLineInput('First Frame', first_frame)
	p.addSingleLineInput('Last Frame', last_frame)
	p.addSingleLineInput('Increment', 1)


	if p.show():
	    
	    l  = p.value("Layer")
	    ff = int(p.value("First Frame"))
	    lf = int(p.value("Last Frame"))
	    i = int(p.value("Increment"))

	    nukescripts.autocrop(first=ff, last=lf, inc=i, layer=l)

	autocrop = node.dependent()[0]
	'''autocrop.setInput(0,None)
	autocrop.knob('xpos').setValue(node.xpos()+50)
	autocrop.knob('ypos').setValue(node.ypos()+35)'''
	autocrop.knob('label').setValue(l)

nuke.menu('Nodes').addCommand('TPD_Tools/TPD_AutoCrop', 'TPD_AutoCrop.AutoCrop()', shortcut=None)

