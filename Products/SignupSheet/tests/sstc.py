from Testing import ZopeTestCase

from DateTime import DateTime

# Make the boring stuff load quietly
ZopeTestCase.installProduct('CMFCore',  )
ZopeTestCase.installProduct('CMFDefault',  )
ZopeTestCase.installProduct('CMFCalendar',  )
ZopeTestCase.installProduct('CMFTopic',  )
ZopeTestCase.installProduct('DCWorkflow',  )
ZopeTestCase.installProduct('CMFQuickInstallerTool',  )
ZopeTestCase.installProduct('CMFFormController',  )
ZopeTestCase.installProduct('GroupUserFolder',  )
ZopeTestCase.installProduct('ZCTextIndex',  )
ZopeTestCase.installProduct('SecureMailHost',  )
ZopeTestCase.installProduct('CMFPlone')
ZopeTestCase.installProduct('Archetypes')
ZopeTestCase.installProduct('PortalTransforms',  )
ZopeTestCase.installProduct('MimetypesRegistry',  )
ZopeTestCase.installProduct('ATSchemaEditorNG')
ZopeTestCase.installProduct('SignupSheet')

from Products.PloneTestCase import PloneTestCase

products = ['SignupSheet']

PloneTestCase.setupPloneSite(products=products)


class SignupSheetTestCase(PloneTestCase.PloneTestCase):

    class Session(dict):
        def set(self, key, value):
            self[key] = value

    def _setup(self):
        PloneTestCase.PloneTestCase._setup(self)
        self.app.REQUEST['SESSION'] = self.Session()
        self.portal.email_from_address='postmaster@demo.netcorps.org'

    def createSignupSheet(self, folder, id, title='', description='',
                        eventSize=1,
                        waitList=2,
                        thank_you_text="Thank you",
                        text="One Great Event",
                        registrantProlog="Sign up",
                        ):
        """Create a SignupSheet in the given folder"""
        self.setRoles(['Manager'])
        folder.invokeFactory('SignupSheet', id)
        signupsheet = getattr(folder, id)
        signupsheet.setTitle(title)
        signupsheet.setDescription(description)
        signupsheet.setEventsize(eventSize)
        signupsheet.setWaitlist_size(waitList)
        signupsheet.setText(text)
        signupsheet.setThank_you_text(thank_you_text)
        signupsheet.setRegistrantProlog(registrantProlog)
        signupsheet.reindexObject()
        return signupsheet

    def createRegistrant(self, signupsheet, title='New Registrant', ):
        
        """Create an issue in the given signupsheet, and perform workflow and
        rename-after-creation initialisation"""
        #newId = self.portal.generateUniqueId('Registrant')
        #oldIds = signupsheet.objectIds()
        signupsheet.invokeFactory('Registrant', title)
        registrant = getattr(signupsheet, title)
        registrant.setFirst_name('')
        registrant.setTitle(title)
        registrant.setEmail('nowhere@localhost.org')
        #self.portal.portal_workflow.doActionFor(registrant, 'post')
        registrant._renameAfterCreation()
        registrant.reindexObject()
        return registrant
