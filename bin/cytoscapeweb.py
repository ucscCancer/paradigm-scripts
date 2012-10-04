#!/usr/bin/env python
"""
cytoscapeweb.py
"""
## Written By: Sam Ng
import getopt, os, re, sys
from optparse import OptionParser

basedir = os.path.dirname(os.path.abspath(__file__))

cytoscapewebExec = os.path.join(basedir, "cytoscapewebReport.py")

def usage(code = 0):
    print __doc__
    if code != None:
        sys.exit(code)

def log(msg, die = False):
    sys.stderr.write(msg)
    if die:
        sys.exit(1)

def main(args):
    ## parse arguments
    parser = OptionParser(usage = "%prog [options]")
    parser.add_option("-b", "--bundle", dest="bundle", default=None)
    parser.add_option("-i", "--html", dest="html", default=None)
    parser.add_option("-d", "--dir", dest="dir", default=None)
    options, args = parser.parse_args()
    
    if len(args) != 0:
        log("ERROR: incorrect number of arguments", die = True)
    
    bundleZip = options.bundle
    htmlPath = options.html
    dirPath = options.dir
    
    ## unzip and find features
    os.system("unzip %s" % (bundleZip))
    
    features = []
    for file in os.listdir("LAYOUT"):
        if os.path.isdir("LAYOUT/%s" % (file)):
            features.append(file)
    
    ## output
    os.system("mkdir %s" % (dirPath))
    for feature in features:
        tableFiles = []
        if os.path.exists("LAYOUT/%s_largest_netLinks.pdf" % (feature)):
            tableFiles.append("largest_netLinks:LAYOUT/%s_largest_netLinks.pdf" % (feature))
        if os.path.exists("LAYOUT/%s_largest_netNodes.pdf" % (feature)):
            tableFiles.append("largest_netNodes:LAYOUT/%s_largest_netNodes.pdf" % (feature))
        if os.path.exists("LAYOUT/%s_totLinks.pdf" % (feature)):
            tableFiles.append("total_netLinks:LAYOUT/%s_totLinks.pdf" % (feature))
        if os.path.exists("LAYOUT/%s_totNodes.pdf" % (feature)):
            tableFiles.append("total_netNodes:LAYOUT/%s_totNodes.pdf" % (feature))
        if len(tableFiles) > 0:
            os.system("%s %s -t %s -r /static/scripts LAYOUT/%s %s" % (sys.executable, cytoscapewebExec, ",".join(tableFiles), feature, dirPath))
        else:
            os.system("%s %s -r /static/scripts LAYOUT/%s %s" % (sys.executable, cytoscapewebExec, feature, dirPath))
    os.system("mv %s/stats.html %s" % (dirPath, htmlPath))
 
if __name__ == "__main__":
    main(sys.argv[1:])
