import os
import sys
import pysvn


class Pysclient:
    
    def __init__(self, url):
        self.url = url
        self.client = pysvn.Client()
        
    def get_url(self):
        return self.url
    
    def get_client(self):
        return self.client
    
    def get_file_list(self):
        file_list = []
        for i in self.client.list(self.url, recurse=True):
                l = PylistWrapper(i, self.url)
                file_list.append(l)
                ## Log purposes only
#                print l.get_revision()
#                print l.get_time_last_change()
#                print l.get_kind()
#                print l.get_absolute_path()
#                print l.get_relative_path()
#                if l.get_kind() == pysvn.node_kind.file:
#                    print self.get_file_content(l.get_absolute_path())
#                print '-------------------'
        return file_list
                
    def get_file_content(self, url):
        return self.client.cat(url)

# End class

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

c = Pysclient('svn://192.168.2.21/home/ameya/TestRepo/')
print c.get_file_list()
    
    
    
    
    
    
    