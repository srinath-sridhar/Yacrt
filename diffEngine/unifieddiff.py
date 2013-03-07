# Unified Diff 
import sys
import os
import difflib
import re

old_file_line_num = 1
new_file_line_num = 1

def __htmlFormatString(str):
    return str.replace('<', '&lt;').replace('>', '&gt;')

def __createHTMLViewFromUnifiedDiff(output,diff):
    boundaryRecord = None
    startsWithPlus = re.compile(r"^\+.*")
    startsWithMinus = re.compile(r"^\-.*")
    startsWithQuestion = re.compile(r"^\@`.*")
    for i in diff:
        if re.search(startsWithPlus, i) != None:
            __writeAddedLine(output, i[1:])
        elif re.search(startsWithMinus, i) != None:
            __writeDeletedLine(output, i[1:])
        elif re.search(startsWithQuestion, i) != None:
            # Do nothing for now.
            continue
        else:
            __writeLine(output, i[1:])

def __addCSS(output):
    output.append("<head><link rel='stylesheet' type='text/css' href='../diffEngine/unifieddiff_style.css'></head>")

def __writeDeletedLine(output, line):
    global old_file_line_num
    output.append("<tr><td>"+str(old_file_line_num)+"</td><td></td><td><pre class='diff-table-pre removed-line'>" + __htmlFormatString(line) + "</pre></td></tr>")
    old_file_line_num += 1

def __writeAddedLine(output, line):
    global new_file_line_num
    output.append("<tr><td></td><td>"+str(new_file_line_num)+"</td><td><pre class=' diff-table-pre added-line'>" + __htmlFormatString(line) + "</pre></td></tr>")
    new_file_line_num +=1
    
def __writeLine(output, line):
    global old_file_line_num
    global new_file_line_num
    output.append("<tr><td>"+str(old_file_line_num)+"</td><td>"+str(new_file_line_num)+"</td><td><pre class='diff-table-pre unchanged-line'>" + __htmlFormatString(line) + "</pre></td></tr>")
    old_file_line_num +=1
    new_file_line_num +=1

def __openTable(output):
    output.append("<table class='diff-table'><colgroup width='4%'/><colgroup width='4%'/><colgroup width='92%'/>")

def __closeTable(output):
    output.append("</table>")

def getUnifiedDiff(fileContentBefore, fileContentAfter):
    global old_file_line_num
    global new_file_line_num
    old_file_line_num = 1
    new_file_line_num = 1   
    output = [] 
    __openTable(output)
    __createHTMLViewFromUnifiedDiff(output, difflib.unified_diff(fileContentBefore, fileContentAfter))
    __closeTable(output) 
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


