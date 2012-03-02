# -*- coding: utf-8 -*-

import transaction
from Acquisition import aq_parent
from AccessControl import Unauthorized
from Products.CMFCore.utils import getToolByName

from Products.SignupSheet import ssMessageFactory as _

def registrantAdded(obj, event):
    """A new registrant added"""
    
    ftool = getToolByName(obj, 'portal_factory')
    if not ftool.isTemporary(obj):
        ssheet = aq_parent(obj)
        if ssheet.getEventsize() and ssheet.getSeatsLeft() < 0:
            ptool = getToolByName(obj, 'plone_utils')
            transaction.abort()
            ptool.addPortalMessage(_(u"Can't subscribe. No more free slots"), type='error')
