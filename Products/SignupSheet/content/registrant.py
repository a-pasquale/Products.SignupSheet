"""A Registrant type that has an editable schema"""

__author__  = 'Aaron VanDerlip avanderlip@gmail.com'
__docformat__ = 'plaintext'

import smtplib

from AccessControl import ClassSecurityInfo
from zope.interface import implements

from Products.SignupSheet import ssMessageFactory as _
from Products.SignupSheet.interfaces import IRegistrant
from Products.SignupSheet import config

try:
  from Products.LinguaPlone.public import *
except ImportError:
  # No multilingual support
  from Products.Archetypes.public import *

from Products.MailHost.MailHost import MailHostError

#CMF
from Products.CMFCore.permissions import View, ModifyPortalContent
from Products.CMFCore.utils import getToolByName

#ATSchemaEditorNG
from Products.ATSchemaEditorNG.ParentManagedSchema import ParentManagedSchema, ParentOrToolManagedSchema
from Products.ATSchemaEditorNG.config import ATSE_MANAGED_NONE, ATSE_MANAGED_FULL

#ATContentTypes
from Products.ATContentTypes.content.document import finalizeATCTSchema

RegistrantSchema = BaseContent.schema.copy() + Schema(( 

    StringField('first_name',
        default_method="getMemberName",
        widget=StringWidget(
            label=_(u"First name")
        )
    ),
     
    StringField('last_name',
        default_method="getMemberLastName",
        widget=StringWidget(
            label=_(u"Last name")
        )
    ),
    
    StringField('status',
        write_permission = """SignupSheet: View Registration Info""",
        atse_managed=ATSE_MANAGED_NONE,
        read_permission="SignupSheet: View Registration Info",
        vocabulary = [('registered','registered','label_registered'),('waitinglist','waitinglist','label_waitinglist')], 
        widget=SelectionWidget()
    ),
    
    StringField("email", 
        read_permission = """View""",
        default_content_type = """text/plain""",
        type = """string""",
        required = 1,
        validators=('isEmail',),
        schemata = """default""",
        default_method="getMemberEmail",
        widget=StringWidget(
          populate = True,
          macro = """widgets/string""",
          postback = True,
          cols = 30,
          label = """E-mail""",
          visible = {'edit': 'visible', 'view': 'visible'},
          maxlength = """255""",
          size = 30,
          modes = ('view', 'edit'),
        ),
    ),
))

#fix up views for Metadata so it is not displayed in the creation mode
for field in RegistrantSchema.filterFields(isMetadata=1):
    field.widget.visible = {'view':'invisible',
                            'edit':'invisible'}

RegistrantSchema['title'].required = 0
RegistrantSchema['title'].widget.visible = {'view':'invisible',
                                       'edit':'invisible'}
#Remove title and id from schema editor
RegistrantSchema['title'].atse_managed = ATSE_MANAGED_NONE
RegistrantSchema['id'].atse_managed = ATSE_MANAGED_NONE
RegistrantSchema['status'].atse_managed = ATSE_MANAGED_NONE


class Registrant(ParentOrToolManagedSchema, BaseContent):
    implements(IRegistrant)
    meta_type = portal_type = "Registrant"
    schema = RegistrantSchema
    global_allow = False
    
    
    def manage_afterAdd(self, item, container):
        self.updateSchemaFromEditor()
        BaseContent.manage_afterAdd(self, item, container)

    def setTitle(self, value, **kwargs):
        self.title = self.computeFullname()

    def Title(self):
        return self.computeFullname()


    def setStatus(self, value, **kwargs):
        #needs to be fixed
        if self.getStatus() == 'registered':
           pass
        else:
           self.status = self.computeStatus()
            
    def computeStatus(self):
        """to be continued """
        signupsheet = self.getParentNode()
        #this should be filtered for only the proper type
        # assume if registerd then stay that way
        event_size = signupsheet.getEventsize()
        current_size=len(signupsheet.contentIds(filter={'portal_type':'Registrant'}))
       
        if current_size <= event_size or event_size == 0:
            status = 'registered'     
        else:
            status = 'waitinglist'
            
        return status

    def computeFullname(self):
        """ compute the fullname from the firstname and lastname values """
        try:
            first_name = self.getField('first_name').getAccessor(self)()
            last_name = self.getField('last_name').getAccessor(self)()
            if first_name and last_name:
                space = ' '
            else:
                space = ''
            return "%s%s%s" % (first_name, space, last_name)
        except TypeError:
            # Sometimes ATSE update scheda during Registrant creation... this fix the problem
            return self.id
        except AttributeError:
            return self.id

    def getMemberEmail(self):
        member = getToolByName(self, 'portal_membership').getAuthenticatedMember()
        return member.getProperty('email') or ''

    def _getFirstLastMemberName(self, member):
        """
        Obtain the first/last member name
        """
        try:
            first_last_name_order = getToolByName(self, 'portal_properties').signupsheet_properties.first_last_name_order
        except:
            first_last_name_order = 'fl'

        fullname = member.getProperty('fullname') or member.getId() or ''
        elements = fullname.split()
        
        if len(elements)==1:
            return (elements[0], '')
        if len(elements)==2:
            if first_last_name_order=='fl':
                return (elements[0], elements[1])
            else:
                return (elements[1], elements[0])                
        return ('','')

    def getMemberName(self):
        mtool = getToolByName(self, 'portal_membership')
        if mtool.isAnonymousUser():
            return ''
        member = mtool.getAuthenticatedMember()
        return self._getFirstLastMemberName(member)[0]

    def getMemberLastName(self):
        mtool = getToolByName(self, 'portal_membership')
        if mtool.isAnonymousUser():
            return ''
        member = mtool.getAuthenticatedMember()
        return self._getFirstLastMemberName(member)[1]

    def sendNotificationMail(self):
        """
        Send a confirmation message to the registrant's email.
        """

        portal_url  = getToolByName(self, 'portal_url')
        portal      = portal_url.getPortalObject()
        plone_utils = getToolByName(self, 'plone_utils')
        portal      = portal_url.getPortalObject()
        mailHost    = plone_utils.getMailHost()
        encoding    = plone_utils.getSiteEncoding()
        signupsheet = self.aq_parent
        send_from_address = envelope_from = portal.getProperty('email_from_address', 'somebody@somebody.org')

        send_to_address = self.getEmail()
        notify_to_address = signupsheet.getNotifyEmail()
        subtype = signupsheet.getHtmlEmail() and 'html' or 'plain'
        
        #generate email message
        options = {}
        options['registrant'] = self
        message = signupsheet.getEmailResponse(**options)
        #email subject
        subject = signupsheet.getEmailResponseSubject(**options)
        subject = subject.strip()
        try:
            mailHost.secureSend(message, send_to_address, envelope_from, subject=subject, subtype=subtype, charset=encoding, debug=False, From=send_from_address)
        except (MailHostError, smtplib.SMTPException), e:
            self.plone_log("Error notifying the user: %s" % str(e))
        
        #generate notification email
        if notify_to_address:
            message = signupsheet.getNotifyEmailResponse(**options)
            subject = signupsheet.getNotifyEmailResponseSubject(**options)
            subject = subject.strip()
            try:
                mailHost.secureSend(message, notify_to_address, envelope_from, subject=subject, subtype=subtype, charset=encoding, debug=False, From=send_from_address)
            except (MailHostError, smtplib.SMTPException):
                pass

registerType(Registrant, config.PROJECTNAME)
