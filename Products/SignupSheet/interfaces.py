# -*- coding: utf-8 -*-

from zope.interface import Interface

class IRegistrant(Interface):
    """A registration taken from a SignupSheet"""

class ISignupSheet(Interface):
    """A sheet that users can use to subscribe to events"""

