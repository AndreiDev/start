"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from contacts.models import Contact
from django.test.client import Client
from django.test import LiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver


class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)

class ContactTests(TestCase):
    """Contact model tests."""
    
    def test_str(self):
        
        contact = Contact(first_name='John', last_name='Smith')
        
        self.assertEquals(
                          str(contact),
                          'John Smith',
                          )

class ContactListViewTests(TestCase):
    """Contact list view tests."""
    
    def test_contacts_in_the_context(self):
        
        client = Client()
        response = client.get('/')
        
        self.assertEquals(list(response.context['object_list']), [])
        
        Contact.objects.create(first_name='foo', last_name='bar')
        response = client.get('/')
        self.assertEquals(response.context['object_list'].count(), 1)
        
class ContactListIntegrationTests(LiveServerTestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.selenium = WebDriver()
        super(ContactListIntegrationTests, cls).setUpClass()
        
    @classmethod    
    def tearDownClass(cls):
        cls.selenium.quit()
        super(ContactListIntegrationTests, cls).tearDownClass()
        
    def test_contact_listed(self):
        
        # create a test contact
        Contact.objects.create(first_name='foo', last_name='bar')
        
        # make sure it's listed as <first> <last> on the list
        self.selenium.get('%s%s' % (self.live_server_url, '/'))
        self.assertEqual(
                         self.selenium.find_elements_by_css_selector('.contact')[0].text,
                         'foo bar (edit)'
                         )
        
    def test_add_contact_linked(self):
        
        self.selenium.get('%s%s' % (self.live_server_url, '/'))
        self.assert_(
                     self.selenium.find_element_by_link_text('add contact')
                     )
        
    def test_add_contact(self):
        
        self.selenium.get('%s%s' % (self.live_server_url, '/'))
        self.selenium.find_element_by_link_text('add contact').click()
        
        self.selenium.find_element_by_id('id_first_name').send_keys('test')
        self.selenium.find_element_by_id('id_last_name').send_keys('contact')
        self.selenium.find_element_by_id('id_email').send_keys('test@example.com')
        
        self.selenium.find_element_by_id("save_contact").click()
        self.assertEqual(
                         self.selenium.find_elements_by_css_selector('.contact')[-1].text,
                         'test contact (edit)'
                         )
