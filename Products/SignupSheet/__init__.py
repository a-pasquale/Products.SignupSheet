# GNU General Public License (GPL)
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301, USA.
#

from Globals import package_home

#CMF
from Products.CMFCore import utils, permissions, DirectoryView
from Products.CMFPlone.utils import ToolInit

#Archetypes
from Products.Archetypes.public import *
from Products.Archetypes import listTypes
from Products.Archetypes.utils import capitalize

from zope.i18nmessageid import MessageFactory

ssMessageFactory = MessageFactory('signupsheet')

import os, os.path, sys, content

# Get configuration data, permissions
from Products.SignupSheet.config import *

# Register skin directories so they can be added to portal_skins
DirectoryView.registerDirectory('skins', product_globals)
DirectoryView.registerDirectory('skins/SignupSheet', product_globals)
DirectoryView.registerDirectory('skins/Registrant', product_globals)

def initialize(context):

    # Import the type, which results in registerType() being called
    from content import signupsheet, registrant

    # initialize the content, including types and add permissions
    content_types, constructors, ftis = process_types(
        listTypes(PROJECTNAME),
        PROJECTNAME)

    utils.ContentInit(
        PROJECTNAME + ' Content',
        content_types      = content_types,
        permission         = DEFAULT_ADD_CONTENT_PERMISSION,
        extra_constructors = constructors,
        fti                = ftis,
        ).initialize(context)
   
    # Give it some extra permissions to control them on a per class limit
    for i in range(0,len(content_types)):
        klassname=content_types[i].__name__
        if not klassname in ADD_CONTENT_PERMISSIONS:
            continue

        context.registerClass(meta_type   = ftis[i]['meta_type'],
                              constructors= (constructors[i],),
                              permission  = ADD_CONTENT_PERMISSIONS[klassname])
        

    