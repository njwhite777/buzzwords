#!/usr/bin/env python

import glob

files = glob.glob("*.py")

for pyFile in files:

    if( pyFile not in ['classbuild.py','__init__.py'] ):
        with open(pyFile,'w') as fileHandle:
            fileNameNoExt = pyFile.split('.')[0]
            fileNameNoExtCap = fileNameNoExt.capitalize()

            fileHandle.write('#!/usr/bin/env python\n')
            fileHandle.write('\n')
            fileHandle.write('from flask_restful import Resource\n')
            fileHandle.write('\n')
            fileHandle.write('\n')
            fileHandle.write('class {}(Resource):'.format(fileNameNoExtCap))
            fileHandle.write('\n')
            fileHandle.write('\n')
            fileHandle.write('    def __init__(self):\n')
            fileHandle.write('        pass')
