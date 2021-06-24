# --------------------------------------------------------
#  TPD_Tools
#  by Noah Catan
#
#  TPD_UpdateDIP.py
#  Version: 1.0.2
#  Last Updated: 06.24.2021
# --------------------------------------------------------

import nuke, nukescripts
import random

title   = 'TPD_UpdateDIP'
author  = 'Noah Catan'
version = 'v1.0.2'

m_layers = []

def listMLayers(node):
    '''
    Creates a list of every layer starting with an "m_"
    '''
    
    channels = node.channels()
    
    # Create sorted list of layers
    layers = sorted( list( set([c.split('.')[0] for c in channels]) ) )
    
    # Look for layers that have "m_" and append them to the m_layers list
    global m_layers
    m_layers = []
    for layer in layers:
        if "m_" in layer:
            m_layers.append(layer)
    
    # Error message if m_layers list contains nothing
    if len(m_layers) < 1:
        nuke.message('No layers with "m_" found...')
        return
        
def createGroup(node):
    
    # Create group
    group = nuke.createNode('Group', inpanel=False)
    group.setName('TPD_UpdateDIP')
    
    # Set group input and connect parent node's dependents
    group.setInput(0, node)
    if node.dependent()>0:
        for dependent in node.dependent():
            dependent.setInput(0, group)
    
    # Set group position
    group.knob('xpos').setValue(node.xpos())
    group.knob('ypos').setValue(node.ypos()+85)
    
    # Create text knob with title and version info; create divider knob
    text = nuke.Text_Knob('title',' ','<b><i>{} {}</i></b> by {}<br><br>'.format(title, version, author))
    div = nuke.Text_Knob('div', ' ')
    group.addKnob(text)
    group.addKnob(div)

    satCtrl = nuke.Double_Knob('satCtrl', 'saturation')
    satCtrl.setRange(0,4)
    satCtrl.setValue(2.5)
    group.addKnob(satCtrl)  
    
    # Inside the group
    with group:
        
        # Create input
        input = nuke.nodes.Input()
        input.knob('name').setValue('Input')
        
        # Create Colorspace node converting all channels from sRGB to Linear
        colorspace = nuke.nodes.Colorspace(xpos=input.xpos(), ypos=input.ypos()+25, colorspace_in='sRGB', inputs=[input], channels='all')
        
        # Create DIP layer if it doesn't exist
        if 'DIP' not in nuke.layers():
            nuke.Layer( 'DIP', [ 'DIP.red', 'DIP.green', 'DIP.blue', 'DIP.alpha' ] )
        
        # Create Shuffle; shuffle rgba into DIP
        shuffle = nuke.nodes.Shuffle(xpos=input.xpos(),ypos=input.ypos()+75, inputs=[colorspace], out='DIP')
        
        # Creates the main dot for the incremantal horizontal pipe
        dot = nuke.nodes.Dot(xpos=input.xpos()+34, ypos=input.ypos()+150, inputs=[shuffle])
        
        # Create empty global variables
        disjoint, disjoint1 = None, None
        stencil, stencil1 = None, None
        grade, grade1 = None, None
        over, over1 = None, None

                
        for layer in m_layers:
            dot1 = nuke.nodes.Dot(xpos=dot.xpos()+200,ypos=dot.ypos(), inputs=[dot])
            dot = dot1
            
            shuffle = nuke.nodes.Shuffle(xpos=dot.xpos()-34, ypos=dot.ypos()+50, inputs=[dot])
            shuffle.knob('in').setValue(layer)
            shuffle.knob('label').setValue('[value in]')
            
            
            
            if m_layers.index(layer)<1:
                dot2 = nuke.nodes.Dot(xpos=shuffle.xpos()+34, ypos=shuffle.ypos()+100, inputs=[shuffle])
                
                shuffleA = nuke.nodes.Shuffle(xpos=shuffle.xpos(), ypos=shuffle.ypos()+250, inputs=[dot2], red='alpha', green='alpha', blue='alpha', label='[value in]')
                grade1    = nuke.nodes.Grade(xpos=shuffle.xpos(), ypos=shuffle.ypos()+300, inputs=[shuffleA])
                
                r, g, b = (float(random.randint(30,100)))/100, (float(random.randint(30,100)))/100, (float(random.randint(30,100)))/100
                grade1.knob('white').setValue([r,g,b,1])
                grade1.knob('multiply').setValue((float(random.randint(30,100)))/100)
                grade1.knob('unpremult').setValue('rgba.alpha')

            
            elif m_layers.index(layer)==1:
                disjoint = nuke.nodes.Merge2(xpos=shuffle.xpos()+100, ypos=shuffle.ypos()+100, inputs=[dot2, shuffle], operation='disjoint-over')
                stencil  = nuke.nodes.Merge2(xpos=shuffle.xpos(), ypos=shuffle.ypos()+200, inputs=[shuffle, dot2], operation='stencil')
                shuffleA = nuke.nodes.Shuffle(xpos=shuffle.xpos(), ypos=shuffle.ypos()+250, inputs=[stencil], red='alpha', green='alpha', blue='alpha', label='[value in]') 
                grade    = nuke.nodes.Grade(xpos=shuffle.xpos(), ypos=shuffle.ypos()+300, inputs=[shuffleA])
                over     = nuke.nodes.Merge2(xpos=shuffle.xpos(), ypos=shuffle.ypos()+400, inputs=[grade1, grade], operation='disjoint-over')
                
                r, g, b = (float(random.randint(30,100)))/100, (float(random.randint(30,100)))/100, (float(random.randint(30,100)))/100
                grade.knob('white').setValue([r,g,b,1])
                grade1.knob('multiply').setValue((float(random.randint(30,100)))/100)
                grade.knob('unpremult').setValue('rgba.alpha')
                
            elif m_layers.index(layer)>1:
                disjoint = nuke.nodes.Merge2(xpos=shuffle.xpos()+100, ypos=shuffle.ypos()+100, inputs=[disjoint1, shuffle], operation='disjoint-over')
                stencil  = nuke.nodes.Merge2(xpos=shuffle.xpos(), ypos=shuffle.ypos()+200, inputs=[shuffle, disjoint1], operation='stencil')
                shuffleA = nuke.nodes.Shuffle(xpos=shuffle.xpos(), ypos=shuffle.ypos()+250, inputs=[stencil], red='alpha', green='alpha', blue='alpha', label='[value in]') 
                grade    = nuke.nodes.Grade(xpos=shuffle.xpos(), ypos=shuffle.ypos()+300, inputs=[shuffleA])
                over     = nuke.nodes.Merge2(xpos=shuffle.xpos(), ypos=shuffle.ypos()+400, inputs=[over1, grade], operation='disjoint-over')
                
                r, g, b = (float(random.randint(30,100)))/100, (float(random.randint(30,100)))/100, (float(random.randint(30,100)))/100
                grade.knob('white').setValue([r,g,b,1])
                grade1.knob('multiply').setValue((float(random.randint(30,100)))/100)
                grade.knob('unpremult').setValue('rgba.alpha')

            
            shuffle1  = shuffle
            disjoint1 = disjoint
            stencil1  = stencil
            over1     = over              
            
            if m_layers.index(layer)==len(m_layers)-1:
                if 'tpd_colormatte' not in nuke.layers():
                    nuke.Layer( 'tpd_colormatte', [ 'tpd_colormatte.red', 'tpd_colormatte.green', 'tpd_colormatte.blue', 'tpd_colormatte.alpha' ] )
                
                saturation = nuke.nodes.Saturation(xpos=shuffle.xpos(), ypos=shuffle.ypos()+450, inputs=[over])
                clamp      = nuke.nodes.Clamp(xpos=shuffle.xpos(), ypos=shuffle.ypos()+500, inputs=[saturation], channels='rgba')
                shuffle1   = nuke.nodes.Shuffle(xpos=shuffle.xpos(), ypos=shuffle.ypos()+550, inputs=[clamp], in2='DIP', out='tpd_colormatte', out2='rgba', black='red2', white='green2', red2='blue2', green2='alpha2')
                remove     = nuke.nodes.Remove(xpos=shuffle.xpos(), ypos=shuffle.ypos()+600, inputs=[shuffle1], operation='keep', channels='rgba', channels2='tpd_colormatte')
                output     = nuke.nodes.Output(xpos=shuffle.xpos(), ypos=shuffle.ypos()+700, inputs=[remove])

                saturation.knob('saturation').setExpression('satCtrl')
    
def start():            
    node = nuke.selectedNode()
    listMLayers(node)
    createGroup(node)
    m_layers = []

nuke.menu('Nodes').addCommand('TPD_Tools/TPD_UpdateDIP', 'TPD_UpdateDIP.start()', shortcut=None)