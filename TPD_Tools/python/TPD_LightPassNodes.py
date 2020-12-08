# --------------------------------------------------------
#  TPD_Tools
#  by Noah Catan
#
#  TPD_ColorPalette.py
#  Version: 1.0.2
#  Last Updated: 12.08.2020
# --------------------------------------------------------

import nuke

# List of light passes
lightPasses = [
'Shadow',
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

lightPassesMultiply = ['AO']

rgbaLayers = ['DIP']


def create_lp_layer(lpass):
    '''
    Creates an alpha layer based on a Light Pass List item
    '''

    lpass = nuke.Layer('PASS_{}'.format(lpass.upper()), ['{}.alpha'.format(lpass.upper())])
    print lpass


def create_rgba_layer(lpass):
    '''
    Creates an rgba layer
    '''

    lpass = nuke.Layer('{}'.format(lpass.upper()), ['{}.red'.format(lpass.upper()), '{}.green'.format(lpass.upper()), '{}.blue'.format(lpass.upper()), '{}.alpha'.format(lpass.upper())])
    print lpass

def create_layers():
    '''
    Creates layers from the the Light Passes List and other custom layers
    '''

    # Create passes for all the items in the Characters In Scene List
    for l in rgbaLayers:
        create_rgba_layer(l)

    # Create a layer for all the items in the Light Passes List
    for lp in lightPasses:
        create_lp_layer(lp)


def create_lp_nodes(lpass, node):
    '''
    Creates a nodes for a single light pass
    '''

    #clear selection
    nukescripts.clear_selection_recursive()

    # Get parent_dot's position
    parent_dot = node
    x = parent_dot.xpos()
    y = parent_dot.ypos()

    #store nodes in a list
    nodes_created = []

    #node_Dot_2
    node_Dot_2 = nuke.nodes.Dot(xpos=0+x,ypos=81+y,inputs=[parent_dot])
    node_Dot_2['name'].setValue('DOT2_{}'.format(lpass.upper()))
    nodes_created.append(node_Dot_2)
    
    #node_Shuffle_1 - LIGHT PASS
    node_Shuffle_1 = nuke.nodes.Shuffle(xpos=-34+x,ypos=157+y,inputs=[node_Dot_2])
    node_Shuffle_1['name'].setValue('SHUFFLE_{}'.format(lpass.upper()))
    node_Shuffle_1['in'].fromScript('PASS_{}'.format(lpass.upper()))
    node_Shuffle_1['label'].setValue('[value in]')
    node_Shuffle_1['red'].fromScript('black')
    node_Shuffle_1['green'].fromScript('black')
    node_Shuffle_1['blue'].fromScript('black')
    nodes_created.append(node_Shuffle_1)
    
    #node_Shuffle_2 - DIP ALPHA
    node_Shuffle_2 = nuke.nodes.Shuffle(xpos=90+x,ypos=72+y,inputs=[node_Dot_2])
    node_Shuffle_2['in'].fromScript('DIP')
    node_Shuffle_2['label'].setValue('[value in]')
    node_Shuffle_2['red'].fromScript('white')
    node_Shuffle_2['green'].fromScript('white')
    node_Shuffle_2['blue'].fromScript('white')
    nodes_created.append(node_Shuffle_2)
    
    #node_Grade_1
    node_Grade_1 = nuke.nodes.Grade(xpos=182+x,ypos=113+y,inputs=[node_Shuffle_2])
    node_Grade_1['name'].setValue('{}_LIGHT'.format(lpass.upper()))
    node_Grade_1['white'].setValue([0.0, 0.0, 0.0, 0.0])
    node_Grade_1['label'].setValue('LIGHT')
    nodes_created.append(node_Grade_1)
    
    #node_Grade_2
    node_Grade_2 = nuke.nodes.Grade(xpos=90+x,ypos=113+y,inputs=[node_Shuffle_2])
    node_Grade_2['name'].setValue('{}_SHADOW'.format(lpass.upper()))
    node_Grade_2['white'].setValue([0.0, 0.0, 0.0, 0.0])
    node_Grade_2['label'].setValue('SHADOW')
    nodes_created.append(node_Grade_2)
    
    #node_Keymix_1
    node_Keymix_1 = nuke.nodes.Keymix(xpos=90+x,ypos=157+y,inputs=[node_Grade_2,node_Grade_1,node_Shuffle_1])
    node_Keymix_1['name'].setValue('{}_KEYMIX'.format(lpass.upper()))
    node_Keymix_1['channels'].fromScript('DIP')
    nodes_created.append(node_Keymix_1)

    #node_Merge_1
    if lightPasses.index(lpass) > 1:
        node_Merge_1 = nuke.nodes.Merge2(xpos=90+x,ypos=250+y,inputs=[None, node_Keymix_1])
        node_Merge_1['name'].setValue('{}_MERGE'.format(lpass.upper()))
        node_Merge_1['Achannels'].setValue('rgb')
        node_Merge_1['Bchannels'].setValue('rgb')
        node_Merge_1['output'].setValue('rgb')
        if lpass in lightPassesMultiply:
            node_Merge_1['operation'].setValue('multiply')
        else:
            node_Merge_1['operation'].setValue('plus')



def create_lp_tree(lightPassesList, inputNode):
    '''
    Creates an node tree of light pass nodes, links them together with dots and merges
    '''

    # Set initial dot and previous dot
    node = inputNode
    prev_node = node
    merge_list = []
    merge = None

    # For every item in the Light Passes List...
    for lp in lightPassesList:
        # If the list index is 1, create a light pass tree connected to the first dot.
        if lightPassesList.index(lp) == 1:
            # Create Light Pass Nodes
            create_lp_nodes(lp, node)
        
        # If the list index is equal or greater than 2, create a light pass tree and connect it to a new dot.
        elif lightPassesList.index(lp) >= 2:
            if lp not in lightPassesMultiply:
                # Set position of and create a new dot
                x, y = prev_node.xpos(), prev_node.ypos()
                node = nuke.nodes.Dot(xpos=350+x,ypos=0+y,inputs=[prev_node])
                prev_node = node
                
                # Create Light Pass Nodes
                create_lp_nodes(lp, node)
                
                # Link merge node to previous merge node
                merge = nuke.toNode('{}_MERGE'.format(lp.upper()))
                merge.setInput(0, nuke.toNode('{}_MERGE'.format(lightPassesList[lightPassesList.index(lp)-1].upper())))
                merge_list.append(merge)


    for lp in lightPassesMultiply:
        if lp in lightPassesList:
            # Set position of and create a new dot
            x, y = prev_node.xpos(), prev_node.ypos()
            node = nuke.nodes.Dot(xpos=350+x,ypos=0+y,inputs=[prev_node])
            prev_node = node

            # Create Light Pass Nodes
            create_lp_nodes(lp, node)

            # Link merge node to previous merge node
            total_lp_items = len(lightPassesList)
            merge = nuke.toNode('{}_MERGE'.format(lp.upper()))
            if lightPassesMultiply.index(lp) == 0:
                merge.setInput(0, nuke.toNode('{}_MERGE'.format(lightPassesList[len(lightPassesList)-1].upper())))
                merge_list.append(merge)
            else:
                merge.setInput(0, nuke.toNode('{}_MERGE'.format(lightPassesMultiply[lightPassesMultiply.index(lp)-1].upper())))
                merge_list.append(merge)

    x, y = prev_node.xpos(), prev_node.ypos()
    dot1        = nuke.nodes.Dot        (xpos=384+x,ypos=0+y, inputs=[prev_node])
    shuffle1    = nuke.nodes.Shuffle    (xpos=350+x, ypos=72+y, inputs=[dot1])
    unpremult1  = nuke.nodes.Unpremult  (xpos=350+x, ypos=108+y, inputs=[shuffle1])
    merge1      = nuke.nodes.Merge2     (xpos=350+x, ypos=250+y, inputs=[unpremult1, merge])
    output      = nuke.nodes.Output     (xpos=350+x, ypos=350+y, inputs=[merge1])
    
    shuffle1['in'].setValue('DIP')
    shuffle1['label'].setValue('[value in]')
    merge1['operation'].setValue('multiply')


    connect_first_merge_node()


def connect_first_merge_node():
    '''
    Attach the first merge node's B input to the first Keymix node.
    '''
    first_in_pipe = nuke.toNode('{}_KEYMIX'.format(lightPasses[1].upper()))
    for i in range(2, len(lightPasses)):
        if lightPasses[i] not in lightPassesMultiply:
            first_merge = nuke.toNode('{}_MERGE'.format(lightPasses[i].upper()))
            first_merge.setInput(0, first_in_pipe)
            return


def create_lp_group():
    '''
    Wraps the whole thing inside a group node
    '''
    lp_group = nuke.createNode('Group', inpanel=False)
    lp_group['name'].setValue('TPD_LightPasses')
    lp_group.begin()

    inpt = nuke.nodes.Input()
    x, y = inpt.xpos(), inpt.ypos()

    dot1 = nuke.nodes.Dot(xpos=34+x, ypos=100+y, inputs=[inpt])

    create_lp_tree(lightPasses, dot1)

    lp_group.end()



create_layers()
create_lp_group()
