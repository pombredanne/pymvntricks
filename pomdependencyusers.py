#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import division #1/2 = float, 1//2 = integer, python 3.0 behaviour in 2.6, to make future port to 3 easier.
from optparse import OptionParser
import os
import libxml2
def ffind(path,name):
	filelist = []
	for root, dirs, files in os.walk(path):
		for file in files:
			if file == name:
				filelist.append(os.path.join(root, file))
	return filelist
def parsepom(filename,deps,verbose):
	doc = libxml2.parseFile(filename)
	pom = doc.xpathNewContext()
	pom.xpathRegisterNs("pom","http://maven.apache.org/POM/4.0.0")
	projectgroupId=projectartifactId=projectversion=""
	for node in pom.xpathEval("/pom:project/pom:artifactId"):
		projectartifactId=node.content
	for node in pom.xpathEval("/pom:project/pom:groupId"):
		projectgroupId=node.content
	for node in pom.xpathEval("/pom:project/pom:version"):
		projectversion=node.content
	if projectgroupId == "":
		for node in pom.xpathEval("/pom:project/pom:parent/pom:groupId"):
			projectgroupId=node.content
	if projectversion == "":
		for node in pom.xpathEval("/pom:project/pom:parent/pom:version"):
			projectversion=node.content
	project=projectgroupId+":"+projectartifactId+":"+projectversion
	if verbose:
		print "Project: "+project 
	for dependency in pom.xpathEval("/pom:project/pom:dependencies/pom:dependency"):
		groupId=artifactId=version=""
		child = dependency.children
		while child is not None:
			if child.name == "artifactId":
				artifactId=child.content
			if child.name == "groupId":
				groupId=child.content
			if child.name == "version":
				version=child.content
			child=child.next
		fulldep=groupId+":"+artifactId+":"+version
		if verbose:
			print fulldep
		if fulldep in deps:
			depending=deps[fulldep]
		else:
			depending=[]
		depending.append(project)
		deps[fulldep]=depending
	doc.freeDoc()
	return
def main():
	optparser = OptionParser("usage: %prog [options]",version="%prog 0.1")
	optparser.add_option("--verbose", action="store_true", dest="verbose", help="be verbose", default=False)
	(options, args) = optparser.parse_args()
	if len(args) != 0:
		optparser.error("incorrect number of arguments")
	filelist = ffind(".","pom.xml")
	if options.verbose:
		print filelist
	deps = {}
	for file in filelist:
		if options.verbose:
			print "Parsing "+file
		parsepom(file,deps,options.verbose)
	for (dep,projects) in deps.items():
		print "\x1B[31m"+dep,"\x1B[0m",
		projects.sort()
		for project in projects:
			print project,
		print
	exit()
if __name__ == '__main__':
        main()
