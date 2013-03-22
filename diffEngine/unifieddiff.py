# Unified Diff
import sys
import os
import difflib
import re

old_file_line_num = 1
new_file_line_num = 1

def __htmlFormatString(str):
    return str.replace('<', '&lt;').replace('>', '&gt;')

def __createHTMLViewFromContextDiff(output, diff):
    boundaryRecord = None
    startsWithPlus = re.compile(r"^\+.*")
    startsWithMinus = re.compile(r"^\-.*")

    for i in diff:
        if re.search(startsWithPlus, i) != None:
            __writeAddedLine(output, i[1:])
        elif re.search(startsWithMinus, i) != None:
            __writeDeletedLine(output, i[1:])
        else:
            __writeLine(output, i[1:])

def __createHTMLViewFromUnifiedDiff(output,diff):
    boundaryRecord = None
    startsWithPlus = re.compile(r"^\+.*")
    startsWithMinus = re.compile(r"^\-.*")
    line_range_pattern = re.compile(r"^\@.*")
    from_file_pattern = re.compile(r"^\-\-.*")
    to_file_pattern = re.compile(r"^\+\+.*")

    for i in diff:

        if re.search(from_file_pattern, i) != None:
            __writeFormattedLine(output, i[1:])
        elif re.search(to_file_pattern, i) !=None:
            __writeFormattedLine(output, i[1:])
        elif re.search(line_range_pattern, i) != None:
            __reset_line_numbers(i)
            __writeFormattedLine(output, i[1:])
        elif re.search(startsWithPlus, i) != None:
            __writeAddedLine(output, i[1:])
        elif re.search(startsWithMinus, i) != None:
            __writeDeletedLine(output, i[1:])
        else:
            __writeLine(output, i[1:])

def __reset_line_numbers(i):
    global old_file_line_num
    global new_file_line_num

    m = re.findall('\d+', i)
    #defensive copying
    o = old_file_line_num
    n = new_file_line_num

    try:
        temp = int(m[0])
        old_file_line_num = temp
        temp = int(m[2])
        new_file_line_num = temp
    except:
        print "exception in __reset_line_num    bers"
        old_file_line_num = o
        new_file_line_num = n


def __addCSS(output):
    output.append("<head><link rel='stylesheet' type='text/css' href='../diffEngine/unifieddiff_style.css'></head>")

def __writeFormattedLine(output, line):
    output.append("<tr><td class='line-number'></td><td class='line-number'></td><td><pre class='diff-table-pre unchanged-line'>" + __htmlFormatString(line) + "</pre></td></tr>")

def __writeDeletedLine(output, line):
    global old_file_line_num
    output.append("<tr><td class='line-number'>"+str(old_file_line_num)+"</td><td class='line-number'></td><td><pre class='diff-table-pre removed-line'>" + __htmlFormatString(line) + "</pre></td></tr>")
    old_file_line_num += 1

def __writeAddedLine(output, line):
    global new_file_line_num
    output.append("<tr onclick='diff_line_clicked_action(this,"+str(new_file_line_num)+")'><td class='line-number'></td><td class='line-number'>"+str(new_file_line_num)+"</td><td><pre class=' diff-table-pre added-line'>" + __htmlFormatString(line) + "</pre></td></tr>")
    new_file_line_num +=1

def __writeLine(output, line):
    global old_file_line_num
    global new_file_line_num
    output.append("<tr onclick='diff_line_clicked_action(this,"+str(old_file_line_num)+ ")'><td class='line-number'>"+str(old_file_line_num)+"</td><td class='line-number'>"+str(new_file_line_num)+"</td><td><pre class='diff-table-pre unchanged-line'>" + __htmlFormatString(line) + "</pre></td></tr>")
    old_file_line_num +=1
    new_file_line_num +=1

def __openTable(output):
    output.append("<table class='diff-table'><colgroup width='2%'/><colgroup width='2%'/><colgroup width='96%'/>")

def __closeTable(output):
    output.append("</table>")

def getUnifiedDiff(fileContentBefore, fileContentAfter):
    global old_file_line_num
    global new_file_line_num
    old_file_line_num = 1
    new_file_line_num = 1
    if fileContentBefore == None:
        fileContentBefore = ""
    output = []
#    __openTable(output)
    __createHTMLViewFromUnifiedDiff(output, difflib.unified_diff(fileContentBefore, fileContentAfter))
#    __closeTable(output)
    return output

def getContextDiff(fileContentBefore, fileContentAfter):
    global old_file_line_num
    global new_file_line_num
    old_file_line_num = 1
    new_file_line_num = 1
    if fileContentBefore == None:
        fileContentBefore = ""
    output = []
    __createHTMLViewFromContextDiff(output, difflib.Differ().compare(fileContentBefore, fileContentAfter))
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


