import os
import sys

# This class wraps the List object returned by svn list function
class PylistWrapper:

    def setAbsolutePath(self, listObject, root_url):
        if root_url[len(root_url) - 1] == '/':
            self.absolute_path = root_url + listObject[0]['repos_path'][2:]
        else:
            self.absolute_path = root_url + listObject[0]['repos_path'][1:]

    def __init__(self, listObject, root_url):
        self.revision = listObject[0]['created_rev']
        self.setAbsolutePath(listObject, root_url)
        self.relative_path = listObject[0]['repos_path'][1:]
        self.kind = listObject[0]['kind']
        self.size = listObject[0]['size']
        self.last_author = listObject[0]['last_author']
        self.has_props = listObject[0]['has_props']
        self.timeOfLastChange = listObject[0]['time']  
        
    def get_revision(self):
        return self.revision
    def get_absolute_path(self):
        return self.absolute_path
    def get_relative_path(self):
        return self.relative_path
    def get_kind(self):
        return self.kind
    def get_size(self):
        return self.size
    def get_last_author(self):
        return self.last_author
    def get_time_last_change(self):
        return self.timeOfLastChange
    
# End class