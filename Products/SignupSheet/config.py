# -*- coding: utf-8 -*-

from Products.CMFCore.permissions import setDefaultRoles

PROJECTNAME = "SignupSheet"
DEFAULT_ADD_CONTENT_PERMISSION = "SignupSheet: Add SignupSheet"
product_globals=globals()

#dictionary of addtional types so that permissions can be set separately in the install
ADD_CONTENT_PERMISSIONS = {
    'Registrant': 'SignupSheet: Add Registrant',
}

setDefaultRoles('SignupSheet: View Registration Info', ('Manager', 'Owner',))
setDefaultRoles('SignupSheet: View Registrants', ('Manager', ))
setDefaultRoles('SignupSheet: View Thank You', ('Manager', 'Anonymous'))
setDefaultRoles(DEFAULT_ADD_CONTENT_PERMISSION, ('Manager', 'Owner', ))
setDefaultRoles(ADD_CONTENT_PERMISSIONS['Registrant'], ('Manager', 'Owner', 'Anonymous', ))
