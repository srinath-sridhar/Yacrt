# Unified Diff 
import sys
import os
import difflib
import re

output = []
def __htmlFormatString(str):
    return str.replace('<', '&lt;').replace('>', '&gt;')

def __createHTMLViewFromUnifiedDiff(diff):
    boundaryRecord = None
    startsWithPlus = re.compile(r"^\+.*")
    startsWithMinus = re.compile(r"^\-.*")
    startsWithQuestion = re.compile(r"^\?.*")
    for i in diff:
        if re.search(startsWithPlus, i) != None:
            __writeAddedLine(i[1:])
        elif re.search(startsWithMinus, i) != None:
            __writeDeletedLine(i[1:])
        elif re.search(startsWithQuestion, i) != None:
            # Do nothing for now.
            continue
        else:
            __writeLine(i[1:])

def __addCSS():
    output.append("<head><link rel='stylesheet' type='text/css' href='../diffEngine/unifieddiff_style.css'></head>")

def __writeDeletedLine(str):
    output.append("<tr><td class='red'><pre>" + __htmlFormatString(str) + "</pre></td></tr>")

def __writeAddedLine(str):
    output.append("<tr><td class='green'><pre>" + __htmlFormatString(str) + "</pre></td></tr>")
    
def __writeLine(str):
    output.append("<tr><td><pre>" + __htmlFormatString(str) + "</pre></td></tr>")

def __openTable():
    output.append("<table>")

def __closeTable():
    output.append("</table>")

def getUnifiedDiff(fileContentBefore, fileContentAfter):
    __addCSS();
    __openTable();
    __createHTMLViewFromUnifiedDiff(difflib.Differ().compare(fileContentBefore, fileContentAfter));
    __closeTable();
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


