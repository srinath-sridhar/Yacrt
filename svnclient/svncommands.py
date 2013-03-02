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
    Return the HEAD version number
"""
def get_head_version_number(url):
    c = __create_client(url)
    return str(c.get_head_revision_number())

"""
 @ UNUSED

 Get all revisions for a given url and optionally all changed paths
 required for current working of my code. Should be replaced by 
 get_revision_details function

 Output - Specify name of wrapper class
"""
def get_all_revision_details(url, discover_changes = False):
    client = create_client(url)
    return client.get_revisions(discover_changes)

"""
 Gets details of all revisions for a given repository in a range
    Options
        start_rev , end_rev - starting and ending revisions
        discover_changes - optionally retrieve changed file paths

    Reference
        [] - All revisions
        [start, end] - between start and end, both included
        [start] - from and including start to the oldest revison

    Returns List of Pysrev instances
"""                           
def get_revision_details(url, start_rev=None, end_rev=None, discover_changes=False):
    client = __create_client(url)
    return client.get_revisions(start_rev, end_rev, discover_changes)

"""
    Could be needed for further work
"""
def list(client, url):
    client = __create_client(url)
    return client.list(url, recurse=True)

"""
 Get all changed paths for a particular revision of a
 repository location.
 url - base path of the remote repository
 rev_number - revision number of repository
 
 Returns - One Change instance 
"""

def __repoHasChanges(changed_paths):
    return len(changed_paths) > 0

def get_all_changed_paths(url, rev_number=None):
    client = __create_client(url)
    if rev_number == None:
        rev_number = get_head_version_number(url)
    changed_paths = client.get_revisions(rev_number, rev_number, True)
    if(__repoHasChanges(changed_paths)):
        return changed_paths[0].get_changes()
    else:
        return None

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

 Returns - Array of html formatted lines that can be used as such
"""
def get_unified_html_diff(repo_url, file_path, rev_number = None):
    client = __create_client(repo_url)
    return getUnifiedDiff(client.get_file_content_previous_change(file_path, rev_number), client.get_file_content_current_change(file_path, rev_number))

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









"""

Tests and Examples

"""
repoURL = 'svn://192.168.2.21/home/ameya/TestRepo/'
print "HEAD Revison Number for Repo: " + get_head_version_number(repoURL)


print "\nTest 1: Getting all revisions from Head to End\n-----------------------------------\n"
print get_revision_details(repoURL)

print "\nTest 2: Getting all revisions from A to B\n-----------------------------------\n"
print get_revision_details(repoURL,4,3)

print "\nTest 3: Getting all revisions from A to End\n-----------------------------------\n"
print get_revision_details(repoURL,2)

print "\nTest 4: Getting all Changed paths for No Revison\n-----------------------------------\n"
l = get_all_changed_paths(repoURL)
for i in l:
    print i.get_action_on_file() + " " + i.get_relative_path() + " @ " + i.get_absolute_path()

print "\nTest 5: Getting all Changed paths for A Revison\n-----------------------------------\n"
l = get_all_changed_paths(repoURL, 1)
for i in l:
    print i.get_action_on_file() + " " + i.get_relative_path() + " @ " + i.get_absolute_path()


f = open('UnifiedDiffTest.html', 'w')
f.write("<html>")
f.writelines(get_unified_html_diff(repoURL, 'svn://192.168.2.21/home/ameya/TestRepo/src/sorting/InsertionSort.java', 5))
f.write("</html>")

