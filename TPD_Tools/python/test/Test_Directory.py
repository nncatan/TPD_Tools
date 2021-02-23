import os
import nuke
import platform


def Test():

	myDir = os.path.dirname(__file__)
	lplist = os.path.join(myDir, "../lightPasses.txt")

	with open(lplist) as f:
	    lines = f.read().splitlines()

	for line in lines:
	    if line is not '':
	        if '*' in line:
	            line = line.replace('*', '')
	            print str(line + ' is a multiply layer')
	        else:
	            print str(line + ' is a plus layer')             
	        

nuke.menu('Nodes').addCommand('TPD_Tools/TestDir', 'Test_Directory.Test()', icon=None)