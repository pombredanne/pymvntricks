#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import division #1/2 = float, 1//2 = integer, python 3.0 behaviour in 2.6, to make future port to 3 easier.
from optparse import OptionParser
import libxml2
def main():
	optparser = OptionParser("usage: %prog [options]",version="%prog 0.1")
	optparser.add_option("--verbose", action="store_true", dest="verbose", help="be verbose", default=False)
	optparser.add_option("--pom", dest="pompath",help="path to the pom file", metavar="pompath")
	optparser.add_option("--artifact", dest="artifact",help="artifact we're working with", metavar="artifact")
	optparser.add_option("--value", dest="version",help="version we're setting", metavar="version")
	(options, args) = optparser.parse_args()
	if len(args) != 0:
		optparser.error("incorrect number of arguments")
	doc=libxml2.parseFile(options.pompath)
	pom=doc.xpathNewContext()
	pom.xpathRegisterNs("pom","http://maven.apache.org/POM/4.0.0")
	for node in pom.xpathEval("/pom:project/pom:build/pom:plugins/pom:plugin[pom:artifactId='"+options.artifact+"']/pom:version"):
		node.setContent(options.version)
	pom.xpathFreeContext()
	#print doc.serialize()
	doc.saveFile(options.pompath)
	doc.freeDoc()
if __name__ == '__main__':
        main()
