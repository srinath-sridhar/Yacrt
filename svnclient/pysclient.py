import os
import sys
import pysvn
from revisionwrapper import Pysvrev
from pylistwrapper import PylistWrapper
import svncommands

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
        for i in svncommands.list(self.client, self.url):
                l = PylistWrapper(i, self.url)
                file_list.append(l)
                # Log purposes only
#                logRepoFileListHeadVersion(self , l)
        return file_list
                
    def get_file_content_current_change(self, url):
        return self.client.cat(url).split('\n')
    
    def get_file_content_previous_change(self, url):
        headrev = self.client.info2(url)[0][1]['last_changed_rev'].number-1
        if headrev >= 1:
            return self.client.cat(url, revision=pysvn.Revision(pysvn.opt_revision_kind.number, headrev)).split('\n')
        else:
            return ''

    def get_revisions(self):
        revision_list = []
        for i in svncommands.log(self.client, self.url):
            revision_list.append(Pysvrev(i, self.url))
            # Log purposes only
            logRevisionListForARepo(Pysvrev(i, self.url))
        return revision_list

# End class

# logging classes

def logRepoFileListHeadVersion(client, l):
    print l.get_revision()
    print l.get_time_last_change()
    print l.get_kind()
    print l.get_absolute_path()
    print l.get_relative_path()
    if l.get_kind() == pysvn.node_kind.file:
        print client.get_file_content(l.get_absolute_path())
    print '-------------------'

def logRevisionListForARepo(l):
    print "Revision: " + str(l.get_revision_number())
    print l.get_author()
    print l.get_date()
    print l.get_message()
    for i in l.get_changes():
        print i.get_action_on_file() + " " + i.get_relative_path() + " @ " + i.get_absolute_path()
    print '-------------------'

# main calling methods

c = Pysclient('svn://192.168.2.21/home/ameya/TestRepo/')
print c.get_file_list()
print c.get_file_content_current_change('svn://192.168.2.21/home/ameya/TestRepo/src/sorting/InsertionSort.java')
print c.get_file_content_previous_change('svn://192.168.2.21/home/ameya/TestRepo/src/sorting/InsertionSort.java')
print c.get_client().info2(c.get_url(), recurse=False)[0][1].get('last_changed_rev')
print c.get_revisions()
    
    
    
    
    
    
    