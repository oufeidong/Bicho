# Copyright (C) 2007  GSyC/LibreSoft
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
# Authors: Daniel Izquierdo Cortazar <dizquierdo@gsyc.escet.urjc.es>
#

from Bicho.backends import Backend, register_backend
from Bicho.utils import *
from HTMLUtils import *
from HTMLParser import HTMLParser
from ParserSFBugs import *
import re
import time
#import SqlBug
import Bicho.Bug


class SFBackend (Backend):

    def __init__ (self):
        Backend.__init__ (self)

    #def run (self):
    #    pass

   
    def get_links (self, url):
        p = Parser ()
        p.add_filter (['a'])

        try:
            p.feed (urllib.urlopen (url).read ())
            p.close ()
        except:
            pass # TODO

        return p.get_tags ()

   
   
    def getLinksBugs (self, url):
        #Next code must be located in the specific engine of SF
        links = []
        bugs = []
        next_bugs = ""
        
        #links = get_links('http://sourceforge.net/tracker/?group_id=93438&atid=604306&set=any')
        links = self.get_links(url)
       
        for link in links:
            url_str = str(link.get('href'))
            # Bugs URLs
            if re.search("tracker", url_str) and re.search("aid", url_str):
                bugs.append(url_join("http://sourceforge.net" + url_str))
                
            # Next page with bugs
            if re.search("offset", url_str):
                next_bugs = url_join("http://sourceforge.net/", url_str)
        
       
        return bugs, next_bugs

    
    def analyzeBug(self, bugUrl):
        
        parser = ParserSFBugs(bugUrl)
        print "Analizando: " + bugUrl
        parser.feed(urllib.urlopen(bugUrl).read())
        parser.close()
        
        return parser.getDataBug()
        
    
    
    def run (self, url):
        
        debug ("Running Bicho")
        

        #There are several pages of bugs for each project and 50 bugs per page
        #25th August 2007
        while url != "":
            print "Obteniendo links de bugs, de la url: " + url
            bugs, url = self.getLinksBugs(url)
            
            for bug in bugs:
                time.sleep(5)
                print self.analyzeBug(bug)




register_backend ("sf", SFBackend)
    