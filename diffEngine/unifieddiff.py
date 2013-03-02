# Unified Diff 
import sys
import os
import difflib
import re
import pysclient
output = []
def htmlFormatString(str):
    return str.replace('<', '&lt;').replace('>', '&gt;')

def createHTMLViewFromUnifiedDiff(diff):
    boundaryRecord = None
    startsWithPlus = re.compile(r"^\+.*")
    startsWithMinus = re.compile(r"^\-.*")
    startsWithQuestion = re.compile(r"^\?.*")
    for i in diff:
        if re.search(startsWithPlus, i) != None:
            writeAddedLine(i[1:])
        elif re.search(startsWithMinus, i) != None:
            writeDeletedLine(i[1:])
        elif re.search(startsWithQuestion, i) != None:
            # Do nothing for now.
            continue
        else:
            writeLine(i[1:])

def addCSS():
    output.append("<head><link rel='stylesheet' type='text/css' href='unifieddiff_style.css'></head>")

def writeDeletedLine(str):
    print 'line'
    output.append("<tr><td class='red'><pre>" + htmlFormatString(str) + "</pre></td></tr>")

def writeAddedLine(str):
    print 'line'
    output.append("<tr><td class='green'><pre>" + htmlFormatString(str) + "</pre></td></tr>")
    
def writeLine(str):
    print 'line'
    output.append("<tr><td><pre>" + htmlFormatString(str) + "</pre></td></tr>")

def openTable():
    output.append("<table>")

def closeTable():
    output.append("</table>")

def getUnifiedDiff(fileContentBefore, fileContentAfter):
    addCSS();
    openTable();
    createHTMLViewFromUnifiedDiff(difflib.Differ().compare(fileContentBefore, fileContentAfter));
    closeTable();
    return output


# Testing commands - Do not uncomment.

# c = pysclient.Pysclient('svn://192.168.2.21/home/ameya/TestRepo/')
# print c.get_file_list()
# #diff1 = difflib.Differ().compare(open('blah', 'r').readlines(), open('blah2', 'r').readlines())
# diff1 = difflib.Differ().compare(c.get_file_previous_content('svn://192.168.2.21/home/ameya/TestRepo/src/sorting/InsertionSort.java'), c.get_file_content('svn://192.168.2.21/home/ameya/TestRepo/src/sorting/InsertionSort.java'))
# openHTML()
# addCSS()
# openTable()
# createHTMLViewFromUnifiedDiff(diff1)
# closeTable()
# closeHTML()
# f = open('CustomDiff.html', 'w')
# f.writelines(output)


