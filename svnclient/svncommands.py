# Common API for retrieving data from a version control system
# Describes the functions required by the view
# NOTE : This file has to be renamed since this should not be specfic to 
#        any particular version control system

from svnclient.pysclient import Pysclient

"""
 Create version control system specific client
"""
def create_client(url, vc_type=None):
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
        start_rev , end_rev - control range
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

    Output - Specify name of wrapper class
"""                           
def get_revision_details(url, start_rev=None, end_rev=None, discover_changes=False):
    client = create_client(url)
    return client.log(url, discover_changed_paths=discover_changes, strict_node_history=True)

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
 file_path  - path of file within the repository

 NOTE:  file_path and url may have an overlap. Make sure the overlap
        is resolved to get the url specific to the file

 Output - Array of html formatted lines that can be used as such
"""
def get_unified_html_diff(url, rev_number, file_path):
    return []

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
