# --------------------------------------------------------
#  TPD_Tools
#  by Noah Catan
#
#  TPD_DIPSetup.py
#  Version: 1.0.2
#  Last Updated: 01.24.2021
# --------------------------------------------------------


import nuke, nukescripts

layers = []
   
def setup(DIP):
	print "Setup Start"
	channels = DIP.channels()
	global layers
	layers = sorted( list( set([c.split('.')[0] for c in channels]) ) )
	m_layers = []

	for layer in layers:
		if "m_" in layer:
			m_layers.append(layer)
			print str("Added "+layer)
		else:
			layers.remove(layer)
			print str("Removed "+layer)

	if len(m_layers)<1:
		nuke.message('No layers starting with "m_" found...')
		return

	if 'DIP' not in nuke.layers():
		nuke.Layer( 'DIP', [ 'DIP.red', 'DIP.green', 'DIP.blue', 'DIP.alpha' ] )
		"DIP layer not found. Creating DIP layer."
	else:
		print "DIP layer found."

		   
	nukescripts.clear_selection_recursive()
	DIP['selected'].setValue(True)
	grp = nuke.createNode('Group', inpanel=False)
	grp.setName('TPD_CutLowerLayers')
	grp['xpos'].setValue(DIP.xpos())
	grp['ypos'].setValue(85+DIP.ypos())
	print 'Created Group node'
	
	with grp:
		input1 = nuke.nodes.Input()
		dot = nuke.nodes.Dot(xpos=34+input1.xpos(),ypos=200+input1.ypos(), inputs=[input1])
		nodeTree(dot)
		
	grp.setInput(0, DIP)
	if DIP.dependent()>0:
		for d in DIP.dependent():
			d.setInput(0, grp)





def nodeTree(node):
	"""
		Creates the node tree inside the group.
		Each layer will cut out its alpha from the next layer, i.e. 'm_01_xxxx' will cut a hole through 'm_02_xxxx' and so on.
	"""
	print 'Starting nodeTree function'        
	n = node
	n1, n2, n3 = None, None, None
	dot = nuke.nodes.Dot(xpos=150+n.xpos(),ypos=0+n.ypos(), inputs=[n])
	dot1 = nuke.nodes.Dot(xpos=0+n.xpos(),ypos=200+n.ypos(),inputs=[n])
	n = dot
	
	for l in layers:
		print str("Adding layer "+l)
		x,y = n.xpos(), n.ypos()
	
		dot2 = nuke.nodes.Dot(xpos=150+x,ypos=0+y, inputs=[n])
		shuffle1 = nuke.nodes.Shuffle(xpos=-34+x,ypos=30+y,inputs=[n])
		shuffle1['label'].setValue("[value in]")
		shuffle1['in'].setValue(str(l))
		

		if layers.index(l)<1:
			dot3 = nuke.nodes.Dot(xpos=0+x,ypos=100+y,inputs=[shuffle1])
			dot4 = nuke.nodes.Dot(xpos=0+x,ypos=150+y,inputs=[dot3])
			

		elif layers.index(l)==1:
			merge1 = nuke.nodes.Merge2(xpos=-34+x,ypos=147+y,inputs=[shuffle1, dot4])
			merge1['operation'].setValue('stencil')
			merge2 = nuke.nodes.Merge2(xpos=41+x,ypos=97+y,inputs=[shuffle1, dot3])
			merge2['operation'].setValue('disjoint-over')
			dot5 = nuke.nodes.Dot(xpos=75+x,ypos=150+y,inputs=[merge2])
			shuffleCopy1 = nuke.nodes.ShuffleCopy(xpos=-34+x,ypos=197+y,inputs=[dot1, merge1])
			shuffleCopy1['out'].setValue(str(l))
			shuffleCopy1['red'].setValue('red')
			shuffleCopy1['green'].setValue('green')
			shuffleCopy1['blue'].setValue('blue')
			shuffleCopy1['alpha'].setValue('alpha')
			n1, n2, n3 = dot5, merge2, shuffleCopy1
			

		elif layers.index(l)==len(layers)-1:
			merge1 = nuke.nodes.Merge2(xpos=-34+x,ypos=147+y,inputs=[shuffle1, n1])
			merge1['operation'].setValue('stencil')
			shuffleCopy1 = nuke.nodes.ShuffleCopy(xpos=-34+x,ypos=197+y,inputs=[n3, merge1])
			shuffleCopy1['out'].setValue(str(l))
			shuffleCopy1['red'].setValue('red')
			shuffleCopy1['green'].setValue('green')
			shuffleCopy1['blue'].setValue('blue')
			shuffleCopy1['alpha'].setValue('alpha')
			shuffle2 = nuke.nodes.Shuffle(xpos=-34+x,ypos=400+y,inputs=[shuffleCopy1])
			shuffle2['out'].setValue('DIP')
			shuffle2['red'].setValue('red')
			shuffle2['green'].setValue('green')
			shuffle2['blue'].setValue('blue')
			shuffle2['alpha'].setValue('alpha')
			output1 = nuke.nodes.Output(xpos=-34+x,ypos=500+y,inputs=[shuffle2])
			
			
		else:
			merge1 = nuke.nodes.Merge2(xpos=-34+x,ypos=147+y,inputs=[shuffle1, n1])
			merge1['operation'].setValue('stencil')
			merge2 = nuke.nodes.Merge2(xpos=41+x,ypos=97+y,inputs=[shuffle1, n2])
			merge2['operation'].setValue('disjoint-over')
			dot5 = nuke.nodes.Dot(xpos=75+x,ypos=150+y,inputs=[merge2])
			shuffleCopy1 = nuke.nodes.ShuffleCopy(xpos=-34+x,ypos=197+y,inputs=[n3, merge1])
			shuffleCopy1['out'].setValue(str(l))
			shuffleCopy1['red'].setValue('red')
			shuffleCopy1['green'].setValue('green')
			shuffleCopy1['blue'].setValue('blue')
			shuffleCopy1['alpha'].setValue('alpha')
			n1, n2, n3 = dot5, merge2, shuffleCopy1
		
		n = dot2




def start():
	node = nuke.selectedNode()
	if node.Class()=='Read':
		setup(node)
	else:
		nuke.message('Must select one Read node')
		pass

nuke.menu('Nodes').addCommand('TPD_Tools/TPD_DIPSetup', 'TPD_DIPSetup.start()', shortcut=None)