import os, sys
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))

from Testing import ZopeTestCase
from Products.SignupSheet.tests import sstc
from Products.CMFPlone.tests import PloneTestCase
from AccessControl import Unauthorized
from Products.CMFCore.utils import getToolByName

from DateTime import DateTime

default_user = PloneTestCase.default_user

class TestInstallation(sstc.SignupSheetTestCase):
    """Ensure product is properly installed"""

    def afterSetUp(self):
        self.skins           = self.portal.portal_skins
        self.types           = self.portal.portal_types
        self.factory         = self.portal.portal_factory
        self.catalog         = self.portal.portal_catalog
        self.workflow        = self.portal.portal_workflow
        self.properties      = self.portal.portal_properties
        self.transforms      = self.portal.portal_transforms
        self.form_controller = self.portal.portal_form_controller

        self.signupsheetTypes = {'SignupSheet'    : 'signupsheet_workflow',
                                'Registrant' : 'signupsheet_registrant_workflow',
                                }
        #install a fake skin, to simulate installing in a already customised instance
        self.skin_name = "Fake Skin"
        self.skins.addSkinSelection(skinname = self.skin_name, skinpath="", test=0, make_default=1)


    def testSignupSheetInstalled(self):
        self.failUnless('SignupSheet' in self.skins.objectIds())
        for t in self.signupsheetTypes.keys():
            self.failUnless(t in self.types.objectIds())

    def testWorkflowsInstalled(self):
        for k, v in self.signupsheetTypes.items():
            self.failUnless(v in self.workflow.objectIds())
            self.failUnless(self.workflow.getChainForPortalType(k) == (v,))


    def testPortalFactorySetup(self):
        for t in self.signupsheetTypes.keys():
            self.failUnless(t in self.factory.getFactoryTypes())

    def testNotChangingSkinSetup(self):
        self.failUnless(self.skins.getDefaultSkin() == self.skin_name)


class TestContentCreation(sstc.SignupSheetTestCase):
    """Ensure content types can be created"""
    def afterSetUp(self):
        self.createSignupSheet(self.folder, 'signupsheet', title='signupsheet',
                               description='signup description')
        self.signupsheet = self.folder.signupsheet
        self.signupsheet.setEventsize(1)
        self.signupsheet.setWaitlist_size(1)
        self.workflow = self.portal.portal_workflow
    
    def testCreateSignupSheet(self):
        self.failUnless('signupsheet' in self.folder.objectIds())
        self.failUnless(self.signupsheet.Title()=='signupsheet')
        self.failUnless(self.signupsheet.getBodyText()=='<p>One Great Event</p>')
        self.failUnless(self.signupsheet.Description()=='signup description')
        self.failUnless(self.signupsheet.getThankYouText()=='Thank you\n')
        self.failUnless(self.signupsheet.getRegistrantProlog()=='<p>Sign up</p>')
        self.failUnless(self.signupsheet.getEventsize() == 1)
        self.failUnless(self.signupsheet.getWaitlist_size()==1)
        # we need to pass registrant object, because it is used in default field value
        # as options/registrant
        registrant = self.createRegistrant(self.signupsheet)
        self.assertEqual(self.signupsheet.getEmailResponse(**{'registrant':registrant}),
                         u'Thank you for registering to signupsheet\nYour status is: registered\nYour email is: nowhere@localhost.org\n\n')

    def testCreateRegistrant(self):
        self.createRegistrant(self.signupsheet, 'newregistrant')
        self.failUnless('newregistrant' in self.signupsheet.objectIds())
        self.failUnless(self.signupsheet.newregistrant.getEmail() == 'nowhere@localhost.org')
         
     
    def testRegistrantFieldNames(self):
        """check for default field names"""
        fields = self.signupsheet.registrantFieldNames('Registrant')
        self.failUnless(fields == ['id', 'title', 'first_name', 'last_name', 'status', 'email'])

    def testRegistrantSignup(self):
        """Test for singup status"""
        
        #empty singup sheet
        self.failUnless(len(self.signupsheet.contentIds(filter={'portal_type':'Registrant'})) == 0)
        self.failUnless(self.signupsheet.getSignupStatus() == 'open')
        
        
        self.createRegistrant(self.signupsheet, 'registrant1')
        self.failUnless(len(self.signupsheet.contentIds(filter={'portal_type':'Registrant'})) == 1)  
        self.failUnless(self.signupsheet.registrant1.computeStatus() == 'registered')
        self.failUnless(self.signupsheet.getSignupStatus() == 'open')
        
        #test for button state and mail message indicating what the next stat is
        self.failUnless(self.signupsheet.getSignupStatus(1) == 'waitlist')
        
        #this registrant will be on the waiting list
        self.createRegistrant(self.signupsheet, 'registrant2')
        self.failUnless(len(self.signupsheet.contentIds(filter={'portal_type':'Registrant'})) == 2)
        self.failUnless(self.signupsheet.registrant2.computeStatus() == 'waitinglist')
        self.failUnless(self.signupsheet.getSignupStatus() == 'full')
     
    def testComputeStatus(self):
        """Test for correct status if there is no waiting list"""
        self.signupsheet.setEventsize(2)
        self.signupsheet.setWaitlist_size(0)
        
        
         #empty singup sheet
        self.failUnless(len(self.signupsheet.contentIds(filter={'portal_type':'Registrant'})) == 0)
        self.failUnless(self.signupsheet.getSignupStatus() == 'open')
        
        
        self.createRegistrant(self.signupsheet, 'registrant1')
        self.failUnless(len(self.signupsheet.contentIds(filter={'portal_type':'Registrant'})) == 1)  
        self.failUnless(self.signupsheet.registrant1.computeStatus() == 'registered')
        self.failUnless(self.signupsheet.getSignupStatus() == 'open')
        
        #test for button state and mail message indicating what the next stat is
        self.failUnless(self.signupsheet.getSignupStatus(1) == 'open')
        
        #this registrant will be on the waiting list
        self.createRegistrant(self.signupsheet, 'registrant2')
        self.failUnless(len(self.signupsheet.contentIds(filter={'portal_type':'Registrant'})) == 2)
        self.failUnless(self.signupsheet.registrant2.computeStatus() == 'registered')
        self.failUnless(self.signupsheet.getSignupStatus() == 'full')
        
      
    def testComputeStatus2(self):
        """Test for correct status if waiting list is larger than event size"""
        self.signupsheet.setEventsize(1)
        self.signupsheet.setWaitlist_size(2)
        
        
         #empty singup sheet
        self.failUnless(len(self.signupsheet.contentIds(filter={'portal_type':'Registrant'})) == 0)
        self.failUnless(self.signupsheet.getSignupStatus() == 'open')
        
        
        self.createRegistrant(self.signupsheet, 'registrant1')
        self.failUnless(len(self.signupsheet.contentIds(filter={'portal_type':'Registrant'})) == 1)  
        self.failUnless(self.signupsheet.registrant1.computeStatus() == 'registered')
        self.failUnless(self.signupsheet.getSignupStatus() == 'open')
        
        #test for button state and mail message indicating what the next stat is
        self.failUnless(self.signupsheet.getSignupStatus(1) == 'waitlist')
        
        #this registrant will be on the waiting list
        self.createRegistrant(self.signupsheet, 'registrant2')
        self.failUnless(len(self.signupsheet.contentIds(filter={'portal_type':'Registrant'})) == 2)
        self.failUnless(self.signupsheet.registrant2.computeStatus() == 'waitinglist')
        self.failUnless(self.signupsheet.getSignupStatus() == 'waitlist')  
        
          #this registrant will be on the waiting list
        self.createRegistrant(self.signupsheet, 'registrant3')
        self.failUnless(len(self.signupsheet.contentIds(filter={'portal_type':'Registrant'})) == 3)
        self.failUnless(self.signupsheet.registrant3.computeStatus() == 'waitinglist')
        self.failUnless(self.signupsheet.getSignupStatus() == 'full')  


	


class TestCSVExport(sstc.SignupSheetTestCase):
    """Ensures that you can properly export CSV data"""
     
    def afterSetUp(self):
        self.createSignupSheet(self.folder, 'signupsheet', title='signupsheet',
        description='signup description')
        self.signupsheet = self.folder.signupsheet
        self.signupsheet.setEventsize(1)
        self.signupsheet.setWaitlist_size(1)

    #refactor me please    
    def testGenerateCSV(self):
        """test csv generation"""
        fields = self.signupsheet.registrantFieldNames('Registrant')
        self.failUnless(self.signupsheet.generateCSV(fields=fields)=='date;id;title;first_name;last_name;status;email\r\n')
        
        #add field
        self.signupsheet.atse_addField('Registrant', 'default', None, 'testfieldname', None)
        self.signupsheet.invokeFactory(id='datarget', type_name='Registrant')
        ct = getattr(self.signupsheet, 'datarget')
        self.failUnless(ct.Schema().get('testfieldname', None) != None)
        
        #and test again
        fields = self.signupsheet.registrantFieldNames('Registrant')
        #grab date since it is not part of the field set
        date = self.signupsheet.datarget.CreationDate()
        self.assertEqual(self.signupsheet.generateCSV(fields=fields),
                         "date;id;title;first_name;last_name;status;email;testfieldname\r\n"
                         "%s;datarget;test_user_1_;test_user_1_;;registered;;\r\n" % date)
        


class TestCreateObject(sstc.SignupSheetTestCase):
    """Ensures that Schema manager supports factory"""

    def testCreateObjectByDoCreate(self):
        # doCreate should create the real object
        factory = getToolByName(self.portal, 'portal_factory')
        factoryTypes = oldFC = factory.getFactoryTypes().keys()
        factoryTypes.extend(['Registrant'])
        factory.manage_setPortalFactoryTypes(listOfTypeIds=factoryTypes)
        self.createSignupSheet(self.folder, 'signupsheet')
        temp_object = self.folder.signupsheet.restrictedTraverse('portal_factory/Registrant/tmp_id')
        foo = temp_object.portal_factory.doCreate(temp_object, 'foo')
        self.failUnless('foo' in self.folder.signupsheet.objectIds())

    def testRegistrantFirstLastNameCreation(self):
        self.createSignupSheet(self.folder, 'signupsheet', title='signupsheet', description='signup description')
        signupsheet = self.folder.signupsheet
        registrant = self.createRegistrant(signupsheet)

        class Member:
            fullname = "John Smith"
            def getProperty(self, foo):
                return self.fullname
            def getId(self):
                return self.fullname

        member = Member()
        self.assertEqual(registrant._getFirstLastMemberName(member), ('John', 'Smith'))
        member.fullname = ' John\t Smith '
        self.assertEqual(registrant._getFirstLastMemberName(member), ('John', 'Smith'))
        member.fullname = ' John'
        self.assertEqual(registrant._getFirstLastMemberName(member), ('John', ''))
        member.fullname = ''
        self.assertEqual(registrant._getFirstLastMemberName(member), ('', ''))
        member.fullname = 'Dr. John Smith'
        self.assertEqual(registrant._getFirstLastMemberName(member), ('', ''))
        # now switch order of first last name
        self.portal.portal_properties.signupsheet_properties.first_last_name_order = 'lf'
        member.fullname = ' Smith   John '
        self.assertEqual(registrant._getFirstLastMemberName(member), ('John', 'Smith'))
        member.fullname = 'John'
        self.assertEqual(registrant._getFirstLastMemberName(member), ('John', ''))
        member.fullname = 'Smith'
        self.assertEqual(registrant._getFirstLastMemberName(member), ('Smith', ''))


class TestWorkflowActions(sstc.SignupSheetTestCase):
    def afterSetUp(self):
        self.createSignupSheet(self.folder, 'signupsheet', title='signupsheet',
                               description='signup description')
        self.signupsheet = self.folder.signupsheet
        self.signupsheet.setEventsize(1)
        self.signupsheet.setWaitlist_size(1)
        
        self.createRegistrant(self.signupsheet, 'newregistrant')
        self.wf = self.portal.portal_workflow
        self.wf.notifyCreated(self.signupsheet.newregistrant)
        
        #setup MailHost replacement
        from Products.CMFPlone.tests.utils import MockMailHost
        self.portal.MailHost = MockMailHost('MailHost')
        

    def testPostActionAccess(self):
        """Make sure anon can post but not view after the post workflow transition"""
        #anon should be able to post
        self.logout()
        self.wf.doActionFor(self.signupsheet.newregistrant, 'post', comment='this is posted', test='bar')
        
        #should fail for anon viewer should raise Unauthorized
        self.assertRaises(Unauthorized, self.signupsheet.newregistrant.base_view)
         

    def testAnonCanViewSS(self):
        """Make sure anon can see ss (see also #51)"""
        self.signupsheet.setEarlyBirdDate(DateTime())
        self.signupsheet.setRegistrationDeadline(DateTime())
        self.logout()
        # See the page without errors
        self.assertTrue(self.signupsheet.getSignupMessage() in self.signupsheet.base_view())
        self.loginAsPortalOwner()
        self.wf.doActionFor(self.signupsheet, 'close')
        self.logout()
        # See the page without errors
        self.assertTrue('The registration is closed' in self.signupsheet.base_view())

        
    def testPostEmails(self):
         """Test emails sent for notification"""
         self.signupsheet.setNotifyEmail("user@localhost.net")
         
         self.wf.doActionFor(self.signupsheet.newregistrant, 'post', comment='this is posted', test='bar')
         
         #will decode the email message   
         registrationMail = self.portal.MailHost.messages[0].message.get_payload(decode=1)
         registrationText = u'Thank you for registering to signupsheet\nYour status is: registered\nYour email is: nowhere@localhost.org\n\n'
         self.assertEquals(registrationMail, registrationText)

         notificationMail = self.portal.MailHost.messages[1].message.get_payload(decode=1)
         notifyText = u'New registrant registered for signupsheet\nPlease check current registrans: http://nohost/plone/Members/test_user_1_/signupsheet/view_registrants\n\n'
         self.assertEquals(notificationMail, notifyText)

def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestInstallation))
    suite.addTest(makeSuite(TestContentCreation))
    suite.addTest(makeSuite(TestCreateObject))
    suite.addTest(makeSuite(TestCSVExport))
    suite.addTest(makeSuite(TestWorkflowActions))
    return suite

if __name__ == '__main__':
    framework()
