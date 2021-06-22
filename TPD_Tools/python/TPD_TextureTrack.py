# --------------------------------------------------------
#  TPD_Tools
#  by Noah Catan
#
#  TPD_DIPSetup.py
#  Version: 1.0.2
#  Last Updated: 04.12.2021
# --------------------------------------------------------

import nuke, nukescripts
version = 'v1.0.2'
layers = []
m_layers = []
knobList = []
linkedKnobs = []

def textureTrackSetup(DIP):

	# Create variables
	# DIP = nuke.selectedNode()
	channels = DIP.channels()
	global m_layers
	m_layers = []

	# Create sorted list of DIP layers
	global layers
	layers = sorted( list( set([c.split('.')[0] for c in channels]) ) )

	# Look for layers that have "m_" and append them to m_layers
	for layer in layers:
		if "m_" in layer:
			m_layers.append(layer)
			print "Added " +str(layer)

	if len(m_layers)<1:
		nuke.message('No layers starting with "m_" found...')
		return

	# Create DIP layer if it's not found
	if 'DIP' not in nuke.layers():
		nuke.Layer( 'DIP', [ 'DIP.red', 'DIP.green', 'DIP.blue', 'DIP.alpha' ] )
		"DIP layer not found. Creating DIP layer."
	else:
		print "DIP layer found."

	# Clear selection
	#nukescripts.clear_selection_recursive()

	# Create tex01 layer if not found
	if 'tex01' not in nuke.layers():
		nuke.Layer( 'tex01', [ 'tex01.red', 'tex01.green', 'tex01.blue', 'tex01.alpha' ] )

	nukescripts.clear_selection_recursive()
	DIP['selected'].setValue(True)
	grp = nuke.createNode('Group', inpanel=False)
	grp.setName('TPD_TextureTrack')
	grp['xpos'].setValue(DIP.xpos())
	grp['ypos'].setValue(85+DIP.ypos())
	grp.setInput(0,DIP)
	print 'Created Group node'

	
	text = nuke.Text_Knob('title',' ','<i>TPD_TextureTrack</i></b> {}<br>by Noah Catan<br><br><b>'.format(version))
	div1 = nuke.Text_Knob('div', ' ')
	grp.addKnob(text)
	grp.addKnob(div1)

	
	global_scale = nuke.Double_Knob('global_scale','global scale')
	global_rotate = nuke.Double_Knob('global_rotate','global rotate')
	div = nuke.Text_Knob('div', ' ')
	grp.addKnob(global_scale)
	grp.addKnob(global_rotate)
	grp.addKnob(div)
	grp['global_scale'].setRange(1,5)
	grp['global_scale'].setValue(1)
	grp['global_rotate'].setRange(0,360)
	grp['global_rotate'].setValue(0)


	with grp:
		input1 = nuke.nodes.Input()
		dot = nuke.nodes.Dot(xpos=34+input1.xpos(),ypos=200+input1.ypos(), inputs=[input1])
		create_nodeTree(dot)
	
	'''for transform in transformList:
		knobTarget = "{}.{}".format(transform.name(), 'scaleOffset')
		linkedKnobs.append(knobTarget)

	for knob in linkedKnobs:
		link_knob = nuke.Link_Knob("{}".format(layers[linkedKnobs.index(knob)]))
		link_knob.setLink(knob)
		grp.addKnob(link_knob)'''

	for knob in knobList:
		link_knob = nuke.Link_Knob('{}'.format(knob[9:]))
		link_knob.setLink(knob)
		grp.addKnob(link_knob)



def create_nodeTree(node):
	
	n = node
	n1, n2, n3 = None, None, None

	controls = nuke.nodes.NoOp(name='CONTROLS',xpos=n.xpos()+300,ypos=n.ypos())

	texInput = nuke.nodes.Input(name='tex01',xpos=n.xpos()-34,ypos=250+n.ypos())

	dot = nuke.nodes.Dot(xpos=0+n.xpos(),ypos=100+n.ypos(), inputs=[n])
	dot1 = nuke.nodes.Dot(xpos=250+n.xpos(),ypos=100+n.ypos(), inputs=[dot])

	n = dot1
	n1 = texInput

	for l in m_layers:
		print str("Adding layer "+l)
		x,y = n.xpos(), n.ypos()

		dot1 = nuke.nodes.Dot(xpos=x+350,ypos=y+0,inputs=[n])
		shuffle = nuke.nodes.Shuffle(xpos=x-34,ypos=y+50,inputs=[n])
		shuffle['in'].setValue(str(l))
		shuffle['label'].setValue('[value in]')
		nukescripts.clear_selection_recursive()
		shuffle['selected'].setValue(True)

		try:
			nukescripts.autocrop(layer='a')
		except:
			print "oops"
			return

		autocrop = shuffle.dependent()[0]
		acName = autocrop.name()

		dot2 = nuke.nodes.Dot(xpos=x-100,ypos=y+200,inputs=[n1])
		
		transform = nuke.nodes.Transform(xpos=x-134,ypos=y+250,inputs=[dot2])
		transform['center'].setExpression('width/2',0)
		transform['center'].setExpression('height/2',1)
		
		scaleOffset = nuke.Double_Knob('{}_scale'.format(str(l)), '{}_scale'.format(str(l)))
		rotateOffset = nuke.Double_Knob('{}_rotate'.format(str(l)), '{}_rotate'.format(str(l)))
		controls.addKnob(scaleOffset)
		controls.addKnob(rotateOffset)
		controls['{}_scale'.format(str(l))].setRange(1,5)
		controls['{}_scale'.format(str(l))].setValue(1)
		controls['{}_rotate'.format(str(l))].setRange(0,360)
		controls['{}_rotate'.format(str(l))].setValue(0)
		transform['scale'].setExpression('parent.global_scale * CONTROLS.{}_scale'.format(str(l)))
		transform['rotate'].setExpression('parent.global_rotate + CONTROLS.{}_rotate'.format(str(l)))

		knobList.append('{}.{}_scale'.format(controls.name(), str(l)))
		knobList.append('{}.{}_rotate'.format(controls.name(), str(l)))
		
		cornerpin = nuke.nodes.CornerPin2D(xpos=x-134,ypos=y+300,inputs=[transform])

		cornerpin['to1'].setExpression('{}.bbox.x'.format(acName), 0)
		cornerpin['to1'].setExpression('{}.bbox.y'.format(acName), 1)
		cornerpin['to2'].setExpression('{}.bbox.r'.format(acName), 0)
		cornerpin['to2'].setExpression('{}.bbox.y'.format(acName), 1)
		cornerpin['to3'].setExpression('{}.bbox.r'.format(acName), 0)
		cornerpin['to3'].setExpression('{}.bbox.t'.format(acName), 1)
		cornerpin['to4'].setExpression('{}.bbox.x'.format(acName), 0)
		cornerpin['to4'].setExpression('{}.bbox.t'.format(acName), 1)

		cornerpin['from2'].setExpression('width',0)
		cornerpin['from3'].setExpression('width',0)
		cornerpin['from3'].setExpression('height',1)
		cornerpin['from4'].setExpression('height',1)

		copy = nuke.nodes.Copy(xpos=x-34,ypos=y+290,inputs=[autocrop, cornerpin])
		copy['from0'].setValue('none')
		copy['to0'].setValue('none')
		copy['channels'].setValue('rgb')
		copy['bbox'].setValue('B')

		premult = nuke.nodes.Premult(xpos=x-34,ypos=y+350,inputs=[copy])

		if m_layers.index(l) < 1:
			dot3 = nuke.nodes.Dot(xpos=x,ypos=y+400,inputs=[premult])
			n2 = dot3
		elif m_layers.index(l) >= 1:
			merge = nuke.nodes.Merge2(xpos=x-34,ypos=y+400,inputs=[premult,n2])
			merge['operation'].setValue('disjoint_over')
			n2 = merge
		
		if m_layers.index(l)==len(m_layers)-1:
			shuffle = nuke.nodes.Shuffle(xpos=x-34,ypos=y+600,inputs=[n2])
			shuffle['alpha'].setValue('red')
			output = nuke.nodes.Output(xpos=x-34,ypos=y+650,inputs=[shuffle])


		n = dot1
		n1 = dot2



def start():
	node = nuke.selectedNode()
	textureTrackSetup(node)

nuke.menu('Nodes').addCommand('TPD_Tools/Experimental/TPD_TextureTrack', 'TPD_TextureTrack.start()', shortcut=None)