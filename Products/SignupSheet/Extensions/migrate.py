# Migration methods
# DEPRECATED

from Products.CMFCore.utils import getToolByName
from Products.Archetypes.atapi import BaseUnit
from Products.Archetypes.atapi import ObjectField

def fixZPTFields(self):
    portal = getToolByName(self, 'portal_url').getPortalObject()
    ctool = getToolByName(portal, 'portal_catalog')
    sheets = ctool(portal_type='SignupSheet')
    fields_to_migrate = ('thank_you_text', 'email_response',)
    for sheet in sheets:
        obj = sheet.getObject()
        kwargs = {'schema':obj.Schema()}
        for f in fields_to_migrate:
            field = obj.getField(f)
            value = ObjectField.get(field, obj, **kwargs)
            if isinstance(value, BaseUnit):
                # old field value
                # get value (string)
                value = value()
                field.set(obj, value)
            else:
                # already migrated or new object
                pass
    return 'Migrated fields %s' % str(fields_to_migrate)