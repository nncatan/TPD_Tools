# -------------------------------------------------------------
#  TPD_ColorPalette
#  by Noah Catan
#
#  TDP_ColorPalette.py
#  Version: 1.1.1
#  Last Updated: 06.24.2021
# -------------------------------------------------------------

import nuke

# List of light passes
lightPasses = [
'Key_Light',
'AO',
'Secondary',
'Ambient',
'Custom',
'Translucent',
'SSS_Skin',
'SSS_Rest',
'Specular',
'Rim_Light']

# -----------------------------------------------------------------------------------------------------------------------------------------------------------------
#  CHECK FOR LIGHT PASS LAYERS ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# -----------------------------------------------------------------------------------------------------------------------------------------------------------------

def create_lp_layer(lpass):
	'''
		Creates an alpha layer based on a Light Pass List item
	'''
	lpass = nuke.Layer('LGHT_{}'.format(lpass.upper()), ['LGHT_{}.alpha'.format(lpass.upper())])
	#print lpass



def create_rgba_layer(lpass):
	'''
		Creates an rgba layer
	'''
	lpass = nuke.Layer('{}'.format(lpass.upper()), ['{}.red'.format(lpass.upper()), '{}.green'.format(lpass.upper()), '{}.blue'.format(lpass.upper()), '{}.alpha'.format(lpass.upper())])
	#print lpass



def check_for_layers():
	'''
		Creates layers from the the Light Passes List and other custom layers
	'''
	layers = []
	for i in nuke.layers():
		layers.append(i)
	print(layers)

	layerExists = False

	for lp in lightPasses:
		lpass = "LGHT_{}".format(lp.upper())

		for layer in layers:
			if lpass == layer:
				layerExists = True
				print(str(str(layer) + ' layer already exists.'))
		
		if layerExists == False:
			create_lp_layer(lp)
			print(str("Creating " + str(lpass) + ' layer.'))

	for layer in layers:
		if layer == 'DIP':
			layerExists == True
			print('DIP layer already exists.')

	if layerExists == False:
		create_rgba_layer('DIP')
		print("Creating DIP layer.")



# -----------------------------------------------------------------------------------------------------------------------------------------------------------------
#  TPD_ColorPalette GIZMO & MENU ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# -----------------------------------------------------------------------------------------------------------------------------------------------------------------

def TPD_ColorPalette():
	print('Checking for LGHT layers.')
	check_for_layers()
	print('Check complete.')
	nuke.createNode('TPD_ColorPalette')
	print('TPD_ColorPalette node created.')


nuke.menu('Nodes').addCommand('TPD_Tools/TPD_ColorPalette', 'TPD_ColorPalette.TPD_ColorPalette()', shortcut='shift+alt+o')