import os
import sys
import pysvn
from revisionwrapper import Pysvrev
from pylistwrapper import PylistWrapper

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
        # for i in svncommands.list(self.client, self.url):
        #         l = PylistWrapper(i, self.url)
        #         file_list.append(l)
                # Log purposes only
#                logRepoFileListHeadVersion(self , l)
        return file_list
                
    def get_head_revision_number(self):
        return self.client.info2(self.url)[0][1]['rev'].number

    def get_file_content_current_change(self, absoluteUrl, rev_number = None):
        if rev_number == None:
            rev_number = self.get_head_revision_number()
        return self.client.cat(absoluteUrl, revision=pysvn.Revision(pysvn.opt_revision_kind.number, rev_number)).split('\n')
    
    def get_file_content_previous_change(self, absoluteUrl, revision = None):
        if revision == None:
            headrev = self.get_head_revision_number() - 1
        else:
            headrev = revision - 1

        if headrev >= 1:
            return self.client.cat(absoluteUrl, revision=pysvn.Revision(pysvn.opt_revision_kind.number, headrev)).split('\n')
        else:
            return ''

    def get_revisions(self, startRevision, endRevision, discover_changed_paths):
        revision_list = []

        if (startRevision == None and endRevision == None):
            startRev = pysvn.Revision(pysvn.opt_revision_kind.head)
            endRev = pysvn.Revision(pysvn.opt_revision_kind.number, 0)
        elif (startRevision != None and endRevision == None):
            startRev = pysvn.Revision(pysvn.opt_revision_kind.number, startRevision)
            endRev = pysvn.Revision(pysvn.opt_revision_kind.number, 0)
        else:
            startRev = pysvn.Revision(pysvn.opt_revision_kind.number, startRevision)
            endRev = pysvn.Revision(pysvn.opt_revision_kind.number, endRevision)


        for i in self.client.log(self.url, startRev, endRev, discover_changed_paths):
            revision_list.append(Pysvrev(i, self.url))
            # Log purposes only
            # logRevisionListForARepo(Pysvrev(i, self.url))
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


    
    
    
    
    
    
    