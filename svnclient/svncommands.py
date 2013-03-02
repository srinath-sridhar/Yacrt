# Common API for retrieving data from a version control system
# Describes the functions required by the view
# NOTE : This file has to be renamed since this should not be specfic to 
#        any particular version control system
import sys
sys.path.append('..')
from pysclient import Pysclient
from diffEngine.unifieddiff import getUnifiedDiff
import pysvn

"""
 Create version control system specific client
"""
def __create_client(url, vc_type=None):
    return Pysclient(url)

"""
 Get all revisions for a given url and optionally all changed paths
 required for current working of my code. Should be replaced by 
 get_revision_details function
 IGNORE THIS.

 Output - Specify name of wrapper class
"""
def get_all_revision_details(url, discover_changes = False):
    client = create_client(url)
    return client.get_revisions(discover_changes)

"""
 Gets details of all revisions for a given repository in a range
    Options
        start_rev , end_rev - starting and ending revisions
            if both start and end are specified retireves [start, end]
            only start is specified retrieves [start, 0] 
            only end is specified retirieves [HEAD, end]
            neither start or end specified retrieves [HEAD, 0]
        discover_changes - optionally retrieve changed file paths

    Reference
        [start, end] - between start and end, both included
        [start, 0] - from and including start to the oldest revison
        [HEAD, end] - from the latest revision upto and including end
        [HEAD, 0] - all revisons for the given repository

    Returns List of Revisons wrapped as Pysrev
"""                           
def get_revision_details(url, start_rev=pysvn.Revision(pysvn.opt_revision_kind.head), end_rev=pysvn.Revision(pysvn.opt_revision_kind.number, 0), discover_changes=False):
    client = __create_client(url)
    return client.get_revisions(start_rev, end_rev, discover_changes)

"""
 I dont think this is really required unless we want to implement 
 browsing the repository (like a directory structure) over the web
"""
def list(client, url):
    client = create_client(url)
    return client.list(url, recurse=True)

"""
 Get all changed paths for a particular revision of a
 repository location.
 url - base path of the remote repository
 rev_number - revision number of repository
              if no revision number is specified 
              retireve changed paths of HEAD revision
 
 Output - Specify name of wrapper class
"""
def get_all_changed_paths(url, rev_number=None):
    client = create_client(url)
    return client.get_changed_paths(rev_number)

"""
 Gets the unified diff of a file with its immediately previous version.
 Example file "a" of revision 1000 is compared 
 against file "a" in revison 999
 url - base path of the remote repository
 rev_number - revision number of repository
              if no revision number is specified 
              use file from HEAD revision
 file_path  - relative ? path of file within the repository

 NOTE:  file_path and url may have an overlap. Make sure the overlap
        is resolved to get the url specific to the file

 Output - Array of html formatted lines that can be used as such
"""
def get_unified_html_diff(repo_url, file_path, rev_number = None):
    client = __create_client(repo_url)
    return getUnifiedDiff(client.get_file_content_previous_change(file_path, rev_number), client.get_file_content_current_change(file_path))

"""
 Gets the side by side diff of a file with its immediately previous version.
 Example file "a" of revision 1000 is compared 
 against file "a" in revison 999
 url - base path of the remote repository
 rev_number - revision number of repository
              if no revision number is specified 
              use file from HEAD revision
 file_path  - path of file within the repository
 

 NOTE:  file_path and url may have an overlap. Make sure the overlap
        is resolved to get the url specific to the file

 Output - Html formatted lines that can be used as such
"""
def get_side_by_side_html_diff(url, rev_number, file_path):
    return []




print get_revision_details('svn://192.168.2.21/home/ameya/TestRepo/')
f = open('UnifiedDiffTest.html', 'w')
f.write("<html>")
f.writelines(get_unified_html_diff('svn://192.168.2.21/home/ameya/TestRepo/', 'svn://192.168.2.21/home/ameya/TestRepo/src/sorting/InsertionSort.java'))
f.write("</html>")
# main calling methods


# print c.get_file_list()
# print c.get_file_content_current_change('svn://192.168.2.21/home/ameya/TestRepo/src/sorting/InsertionSort.java')
# print c.get_file_content_previous_change('svn://192.168.2.21/home/ameya/TestRepo/src/sorting/InsertionSort.java')
# print c.get_client().info2(c.get_url(), recurse=False)[0][1].get('last_changed_rev')
# print c.get_revisions()
