# -*- coding: utf-8 -*-

from zope.interface import implements

from Products.CMFCore.utils import getToolByName
from Products.CMFCore.permissions import View, ModifyPortalContent, ManagePortal
from Products.CMFPlone.interfaces import INonStructuralFolder
from Products.CMFPlone.i18nl10n import utranslate

from Products.SignupSheet import ssMessageFactory as _
from Products.SignupSheet import config

#ArcheTypes
from Products.Archetypes.public import *

from Products.SignupSheet.content.registrant import Registrant
from Products.SignupSheet.interfaces import ISignupSheet

#ATSchemaEditorNG
from Products.ATSchemaEditorNG.interfaces import ISchemaEditor
from Products.ATSchemaEditorNG.SchemaEditor import SchemaEditor
from Products.ATSchemaEditorNG import util
from Products.ATSchemaEditorNG.config import ManageSchemaPermission

#ATContentTypes
from Products.ATContentTypes.content.base import ATCTOrderedFolder
from Products.ATContentTypes.content.folder import *

#security
from AccessControl import ClassSecurityInfo

from Products.TALESField import TALESString
from Products.TemplateFields import ZPTField

#need this for the export tool
import csv
from cStringIO import StringIO

schema = ATFolder.schema.copy() + ConstrainTypesMixinSchema.copy() + Schema(( 


IntegerField('eventsize',
             required=1,
             default=0,
             read_permission="SignupSheet: View Registration Info",
             validators=('isInt',),    
             widget=StringWidget(
                 description = "Set to 0 for unlimited registration",
                 visible={'edit':'visible', 'view':'invisible'},
                 size=6,
                 label='Number of registrants',
                 i18n_domain='signupsheet',
                 label_msgid='field_eventsize',
                 description_msgid='fieldhelp_eventsize',
             )
),


IntegerField('waitlist_size',
             required=1,
             default=0,
             read_permission="SignupSheet: View Registration Info",
             validators=('isInt',),    
             widget=StringWidget(
                 description = "",
                 visible={'edit':'visible', 'view':'invisible'},
                 size=6,
                 label='Size of wait list',
                 i18n_domain='signupsheet',
                 label_msgid='field_waitlist_size',
                 description_msgid='fieldhelp_waitlist_size',
         )
),

BooleanField('display_size_left',
             default=False,
             widget=BooleanWidget(
                 visible={'edit':'visible', 'view':'invisible'},
                 i18n_domain='signupsheet',
                 label='Display seats left',
                 label_msgid='field_display_size_left',
                 description="Choose to show in the subscription page the number of seats left",
                 description_msgid='fieldhelp_display_size_left',
         )
),

DateTimeField('earlyBirdDate',
             required=0,
             default=None,
             read_permission="SignupSheet: View Thank You",
             widget=CalendarWidget(
                 description = "",
                 visible={'edit':'visible', 'view':'invisible'},
                 size=6,
                 label='Early bird phase until',
                 i18n_domain='signupsheet',
                 label_msgid='field_early_bird_phase',
                 description_msgid='fieldhelp_early_bird_phase',
         )
),

DateTimeField('registrationDeadline',
             required=0,
             default=None,
             read_permission="SignupSheet: View Thank You",
             widget=CalendarWidget(
                 description = "",
                 visible={'edit':'visible', 'view':'invisible'},
                 size=6,
                 label='Registration deadline',
                 i18n_domain='signupsheet',
                 label_msgid='field_registration_deadline',
                 description_msgid='fieldhelp_registration_deadline',
         )
),

 TextField('text',
           accessor='getBodyText',
              required=True,
              searchable=True,
              primary=True,
              validators = ('isTidyHtmlWithCleanup',),
              #validators = ('isTidyHtml',),
              default_content_type='text/html',
              default_output_type = 'text/x-html-safe',
              allowable_content_types=('text/html',
                                       'text/plain',
                                       ),
              widget = RichWidget(
                        description = "Text for front page of signup",
                        description_msgid = "help_body_text",
                        label = "Body Text",
                        label_msgid = "label_body_text",
                        rows = 25,
                        i18n_domain = "signupsheet",
               ),
),

TextField('registrantProlog',
              required=False,
              searchable=False,
              primary=False,
              validators = ('isTidyHtmlWithCleanup',),
              default_output_type = 'text/x-html-safe',
              default_content_type='text/html',
              allowable_content_types=('text/html',
                                       'text/plain',
                                       ),
              widget = RichWidget(
                        description = "This text will be displayed before registrant fields on the registrant edit page.",
                        description_msgid = "help_registrant_prolog_text",
                        label = "Registrant prolog",
                        label_msgid = "label_registrant_prolog_text",
                        rows = 15,
                        i18n_domain = "signupsheet",
               ),
),

ZPTField("thank_you_text", 
        schemata="thank you",
        accessor='getThankYouText',
        default_output_type = 'text/html',
        read_permission="SignupSheet: View Thank You",
        default_method = '_get_thank_you_text_message',
        required=0,
        widget=TextAreaWidget(
            label="Thank You",
            label_msgid="label_Thank_You",
            visible={'edit':'visible', 'view':'invisible'},
            description="""Thank you page for returned to registrant. Is rendered in context of SignupSheet. Current registrant object is available through 'options/registrant'.""",
            description_msgid="help_Thank_You",
            i18n_domain="signupsheet",
            rows=10,
        ), 
    ), 
BooleanField('htmlEmail',
            schemata="thank you",
            default=False,
            widget=BooleanWidget(
                 description = "Check this checkbox to send email in HTML format. Otherwise will be sent in plain text.",
                 label='HTML email',
                 visible={'edit':'visible', 'view':'invisible'},
                 i18n_domain='signupsheet',
                 label_msgid='label_html_email',
                 description_msgid='help_html_email',
            )
),
TALESString('email_response_subject',
        schemata="thank you",
        accessor="getEmailResponseSubject",
        validators=('talesvalidator',),
        read_permission="SignupSheet: View Thank You",
        default_method = "_get_email_response_subject_message",
        required = 0,
        widget = StringWidget(
            visible={'edit':'visible', 'view':'invisible'},
            label="Confirmation email subject",
            label_msgid="label_email_response_subject",
            description="Enter TALES expression of confirmation email subject. 'object' is SignupSheet object.",
            description_msgid="help_email_response_subject",
            size=60,
            i18n_domain="signupsheet",
        )
    ),
ZPTField("email_response", 
        schemata="thank you",
        read_permission="SignupSheet: View Thank You",
        default_method = "_get_email_response_message",
        required=0,
        accessor="getEmailResponse",
        allowable_content_types=('text/plain',),
        widget=TextAreaWidget(
            label="Email response message",
            label_msgid="label_email_response",
            visible={'edit':'visible', 'view':'invisible'},
            description="""Email message text that is returned to registrant. This template is rendered in context of SignupSheet. Current registrant object is available through 'options/registrant'.""",
            description_msgid="help_email_message",
            i18n_domain="signupsheet",
            rows=10,
        ), 
    ), 
StringField("notifyEmail", 
        schemata="thank you",
        default =  "",
        read_permission="SignupSheet: View Registration Info",
        required=0,
        validators=('isEmail',),
        widget=StringWidget(
            label="Notify mail address",
            label_msgid="label_notify_email",
            visible={'edit':'visible', 'view':'invisible'},
            description="""Email address which will be notified about new registrant""",
            description_msgid="help_notify_email",
            i18n_domain="signupsheet",
            size=30,
        ), 
    ), 
TALESString('notify_email_response_subject',
        schemata="thank you",
        accessor="getNotifyEmailResponseSubject",
        validators=('talesvalidator',),
        read_permission="SignupSheet: View Thank You",
        default_method = '_get_notify_email_response_subject_message',
        required = 0,
        widget = StringWidget(
            visible={'edit':'visible', 'view':'invisible'},
            label="Notification email subject",
            label_msgid="label_notify_email_response_subject",
            description="Enter TALES expression of notification email subject. 'object' is SignupSheet object. If no notfiyEmail address set, this field is not used.",
            description_msgid="help_notify_email_response_subject",
            size=60,
            i18n_domain="signupsheet",
        )
    ),
ZPTField("notify_email_response", 
        schemata="thank you",
        read_permission="SignupSheet: View Thank You",
        default_method = "_get_notify_email_response_message",
        required=0,
        accessor="getNotifyEmailResponse",
        widget=TextAreaWidget(
            label="Notification email response message",
            label_msgid="label_notify_email_response",
            visible={'edit':'visible', 'view':'invisible'},
            description="""Email message text that is sent to notifyEmail address. If no notfiyEmail address set, this field is not used.""",
            description_msgid="help_notify_email_message",
            i18n_domain="signupsheet",
            rows=10,
        ), 
    ), 
))

class SignupSheet(SchemaEditor, ATFolder, BaseFolder):
    """Container for Registrants"""
    #setup actions for edit and export tools
    actions = ({
        'id'          : 'editschema',
        'name'        : 'edit registrant form',
        'action'      : 'string:${object_url}/signupsheet_schema_editor',
        'permissions': (ManageSchemaPermission,),
        'category'    : 'object',
         },
         {
        'id'          : 'viewregistrants',
        'name'        : 'view registrants',
        'action'      : 'string:${object_url}/view_registrants',
        'permissions': ('Modify portal content',),
        'category'    : 'object',
         },
         {
        'id'          : 'exportdata',
        'name'        : 'export data',
        'action'      : 'string:${object_url}/export_registrant_fields',
        'permissions': ('Modify portal content',),
        'category'    : 'object',
         },
    )

    security = ClassSecurityInfo()
    
    schema = schema
    portal_type = meta_type =  "SignupSheet"
    archetype_name = 'Signup Sheet'
    content_icon   = 'page_edit.gif'
    
    # explicitly specify base_view because this is a folder
    default_view   = 'base_view'
    immediate_view = 'base_view'
    
    # Allow images and files to be uploaded into this containerish object
    allowed_content_types = ['Registrant']

    __implements__ = (ATFolder.__implements__,ISchemaEditor) 

# Make sure we get title-to-id generation when an object is created
    _at_rename_after_creation = True


    """
    Container to act as host for schema editing.
    """
   
    def manage_afterAdd(self, item, container):
        """ """
        # do not show metadata fieldset
        #self.atse_registerObject(getattr(Products.SignupSheet.content.registrant,'Registrant'), ('metadata', ))
        self.atse_registerObject(Registrant, ('metadata', ))
        BaseFolder.manage_afterAdd(self, item, container)


    def _site_encoding(self):
        "Returns the site encoding"
        putils = getToolByName(self, 'plone_utils', None)
        if putils is not None:
            return putils.getSiteEncoding()
        else:
            portal_properties = self.portal_properties
            site_props = portal_properties.site_properties
            return site_props.default_charset or 'utf-8'
   
   
   #Code from UpFront objs product, should be refactored to remove cruft
    security.declareProtected('SignupSheet: View Registrants', 'exportCSV')
    def exportCSV(self, fields=None, coding=None, delimiter='semicolon', export_type='Registrant'):
        """
        Exports a list of objs as a CSV file.  Wraps generateCSV.       
        """    
               
        #updates schema if not done before export
        self.atse_updateManagedSchema(portal_type=export_type,schema_template='signupsheet_schema_editor') 
        
        result = self.generateCSV(fields=fields,delimiter=delimiter)
        
        # encode the result
        charset = self._site_encoding()
        if coding:
            result = result.decode(charset).encode(coding)
        else:
            coding = charset

        # set headers and return
        setheader = self.REQUEST.RESPONSE.setHeader
        setheader('Content-Length', len(result))
        setheader('Content-Type', 
            'text/x-comma-separated-values; charset=%s' % coding)
        setheader('Content-Disposition', 'filename=%s.csv' % self.getId())
        return result
        
        
    #Code based on UpFront objs product, should be refactored to remove cruft
    security.declareProtected('SignupSheet: View Registrants', 'generateCSV')
    def generateCSV(self, objs=None, fields=None, delimiter='semicolon', 
                  quote_char='double_quote', coding=None,
                  export_type='Registrant'):

        """
        Exports a list of objs as a CSV file.
        objs: if None it exports all registrants in the folder.
        fields: field names to export
        """

        #container = self.unrestrictedTraverse(
        #   self.REQUEST.get('current_path'))
        if objs is None:
            objs = self.listFolderContents(
                contentFilter={'portal_type':export_type}
            )

        delim_map = {
            'tabulator':'\t',
            'semicolon':';',
            'colon':':',
            'comma':',',
            'space':' ',
        }

        delimiter = delim_map[delimiter]
        quote_map = {'double_quote':'"', 'single_quote':"'", }
        quote_char = quote_map[quote_char]

        # generate result
        if fields is None:
            result = ''
        else:
            rows = [fields]
            for obj in objs:
                row = []
                #code to append creationDate since it is not part of the fields list
                row.append(obj.CreationDate())
                for fieldname in fields:
                    if fieldname.find('.') != -1:
                        fieldname, key = fieldname.split('.')
                    try:
                        field = obj.Schema()[fieldname]
                        value = field.getAccessor(obj)()
                        row.append(value)
                    except KeyError:
                        row.append('')
                rows.append(row)
            rows[0].insert(0,'date')    
            # convert lists to csv string
            ramdisk = StringIO()
            writer = csv.writer(ramdisk, delimiter=delimiter)
            writer.writerows(rows)
            result = ramdisk.getvalue()
            ramdisk.close()

        return result
 
    
    #used by export_registrant_fields to gather fields for export
    security.declareProtected('SignupSheet: View Registrants', 'registrantFieldNames')
    def registrantFieldNames(self, import_type):
        "Returns the field names for contact type"
        schema = self.atse_getSchemaById(import_type)
        fields = schema.filterFields(isMetadata=0)
        field_names = []
        for field in fields:
            field_names.append(field.getName()) 
        return field_names


    #method to calculate wether the Signupsheet will accept more registrants
    #I dislike using nexstatus but the display button and the registrant creation have different requirements
    def getSignupStatus(self,nextstatus=0):
       """Returns the status of the SignupSheet container"""
       status=''
       event_size = self.getEventsize()
       waitlist_size = self.getWaitlist_size()
       current_size=len(self.contentIds(filter={'portal_type':'Registrant'}))
       max_size = event_size + waitlist_size
       
       if current_size + nextstatus <= event_size:
           status = 'open'     
       elif max_size - current_size <= waitlist_size:
           status = 'waitlist' 

       if current_size >= max_size:
           status = 'full'
       
       if max_size == 0:
           status = 'open'

       return status

    security.declareProtected("View", "getSignupMessage")
    def getSignupMessage(self):
        """ returns signup message for signupsheet_view """
        if self.getSignupStatus(nextstatus=1)=='open':
            msg = utranslate(msgid='sign_up', default='Sign up!', context=self, domain="signupsheet")
        else:
            msg = utranslate(msgid='sign_up_for_waitinglist', default='Signup for waiting list', context=self, domain="signupsheet")        
        return msg

    # i18n Messages

    def _get_thank_you_text_message(self):
        default = u"""<tal:block tal:define="registrant nocall:options/registrant">Thank you for registering, we will contact you shortly. <br/>
You provided the following information:<br />
Name: <strong tal:content="registrant/computeFullname" /><br/>
Email: <strong tal:content="registrant/email" /><br/>
</tal:block>
"""
        if False:
            foo = _(u'default_thank_you_text', default=u"""<tal:block tal:define="registrant nocall:options/registrant">Thank you for registering, we will contact you shortly. <br/>
You provided the following information:<br />
Name: <strong tal:content="registrant/computeFullname" /><br/>
Email: <strong tal:content="registrant/email" /><br/>
</tal:block>
""")
        translation_service = getToolByName(self,'translation_service')
        return translation_service.utranslate(domain='signupsheet',
                                             msgid=u'default_thank_you_text',
                                             default=default,
                                             context=self)

    def _get_email_response_subject_message(self):
        default = u"string:Your registration for ${object/Title} has been received"
        if False:
            foo = _(u'default_email_response_subject', default=u"string:Your registration for ${object/Title} has been received")
        translation_service = getToolByName(self,'translation_service')
        return translation_service.utranslate(domain='signupsheet',
                                             msgid=u'default_email_response_subject',
                                             default=default,
                                             context=self)
    
    def _get_email_response_message(self):
        default = u"""<tal:block tal:define="registrant nocall:options/registrant">Thank you for registering to <tal:s tal:content="context/Title" />
Your status is: <tal:s tal:replace="registrant/computeStatus">registered</tal:s>
Your email is: <tal:e tal:content="registrant/email" />
</tal:block>
"""
        if False:
            foo = _(u'default_email_response_message', default = u"""<tal:block tal:define="registrant nocall:options/registrant">Thank you for registering to <tal:s tal:content="context/Title" />
Your status is: <tal:s tal:replace="registrant/computeStatus">registered</tal:s>
Your email is: <tal:e tal:content="registrant/email" />
</tal:block>
""")
        translation_service = getToolByName(self,'translation_service')
        return translation_service.utranslate(domain='signupsheet',
                                             msgid=u'default_email_response_message',
                                             default=default,
                                             context=self)

    def _get_notify_email_response_subject_message(self):
        default = u"""string:Notification: New registration for ${object/Title} has been received"""
        if False:
            foo = _(u'notify_email_response_subject', default=u"""string:Notification: New registration for ${object/Title} has been received""")
        translation_service = getToolByName(self,'translation_service')
        return translation_service.utranslate(domain='signupsheet',
                                             msgid=u'notify_email_response_subject',
                                             default=default,
                                             context=self)

    def _get_notify_email_response_message(self):
        default = u"""<tal:block tal:define="registrant nocall:options/registrant">New registrant registered for <tal:s tal:content="context/Title" />
Please check current registrans: <tal:s tal:content="string:${context/absolute_url}/view_registrants" />
</tal:block>
"""
        if False:
            foo = _(u'notify_email_response_message', u"""<tal:block tal:define="registrant nocall:options/registrant">New registrant registered for <tal:s tal:content="context/Title" />
Please check current registrans: <tal:s tal:content="string:${context/absolute_url}/view_registrants" />
</tal:block>
""")
        translation_service = getToolByName(self,'translation_service')
        return translation_service.utranslate(domain='signupsheet',
                                             msgid=u'notify_email_response_message',
                                             default=default,
                                             context=self)


    security.declareProtected("SignupSheet: View Registrants", "getRegistrants")
    def getRegistrants(self):
        """Load all contained registrants"""
        catalog = getToolByName(self, 'portal_catalog')
        return catalog(portal_type='Registrant',
                       path='/'.join(self.getPhysicalPath()))

    security.declareProtected("View", "getSeatsLeft")
    def getSeatsLeft(self):
        return self.getEventsize() + self.getWaitlist_size() - len(self.objectIds())

registerType(SignupSheet, config.PROJECTNAME)
