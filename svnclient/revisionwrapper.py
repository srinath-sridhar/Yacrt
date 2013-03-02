import sys
import os
import pysvn
from datetime import datetime

svnstatus = {
'M' : 'Modified',  
'A' : 'Added',
'D' : 'Deleted',
'R' : 'Replaced' 
}

def getDateTimeAsString(logObject):
    return datetime.fromtimestamp(logObject['date']).strftime('%a %b %d %H:%M:%S')

    
def setAbsolutePath(root_url, path):
    if root_url[len(root_url) - 1] == '/':
        return root_url + path[1:]
    else:
        return root_url + path

class Changes:
    def __init__(self, change, repo_url):
        self.action = svnstatus.get(change['action'])
        self.relative_path = change['path']
        self.absolute_path = setAbsolutePath(repo_url, change['path'])
        
    def get_relative_path(self):
        return self.relative_path
    def get_action_on_file(self):
        return self.action
    def get_absolute_path(self):
        return self.absolute_path
            
# This class wraps the Log object returned by the svn log function
class Pysvrev:
    def __init__(self, logObject, repo_url):
        self.author = logObject['author']
        self.date = getDateTimeAsString(logObject)
        self.message = logObject['message']
        self.revision_number = logObject['revision'].number
        self.changes = logObject['changed_paths']
        self.repo_url = repo_url
        
    def get_date(self):
        return self.date
    def get_author(self):
        return self.author
    def get_message(self):
        return self.message
    def get_revision_number(self):
        return self.revision_number
    def get_changes(self):
        wrapped_changes = []
        if self.changes != None:
            for i in self.changes:
                wrapped_changes.append(Changes(i, self.repo_url))
            return wrapped_changes
    
    
    