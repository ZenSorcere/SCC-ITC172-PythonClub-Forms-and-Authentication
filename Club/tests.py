from django.test import TestCase
from .models import Meeting, Minutes, Resource, Event
from .views import index, getmeetings, getresources
from django.contrib.auth.models import User
from django.urls import reverse

class MinutesTest(TestCase):
    def test_string(self):
        minutes=Minutes(Meeting.mtgId=='1') #minutes_id
        self.assertEqual(str(minutes), str(Meeting.mtgId)) #minutes_id

    def test_table(self):
        self.assertEqual(str(Minutes._meta.db_table), 'minutes')

class MeetingTest(TestCase):
    def test_string(self):
        mtg=Meeting(mtgtitle="Test Meeting")
        self.assertEqual(str(mtg), mtg.mtgtitle)

    def test_table(self):
        self.assertEqual(str(Meeting._meta.db_table), 'meeting')

class EventTest(TestCase):
    def test_string(self):
        event=Event(eventtitle="Lab")
        self.assertEqual(str(event), event.eventtitle)

    def test_table(self):
        self.assertEqual(str(Event._meta.db_table), 'event')

class ResourcesTest(TestCase):
    #set up one time sample data
    def setup(self):
        type = Resource(resourcetype='stapler')
        res=Resource(resourcename='Redline', resourcetype='stapler', resourcedesc='Important office tool')
        return res

    def test_string(self):
        res = self.setup()
        #res=Resource(resourcename="stapler")
        self.assertEqual(str(res), res.resourcename)

    def test_type(self):
        res=self.setup()
        self.assertEqual(str(res.resourcetype), 'stapler')

    def test_table(self):
        self.assertEqual(str(Resource._meta.db_table), 'resource')

# Views Test cases -- minus "meeting details", which looks like it would require a bunch of setup
class IndexTest(TestCase):
    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

class GetMeetings(TestCase):
    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('meetings'))
        self.assertEqual(response.status_code, 200)

class GetResources(TestCase):
    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('resources'))
        self.assertEqual(response.status_code, 200)

class GetEvents(TestCase):
    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('events'))
        self.assertEqual(response.status_code, 200)

# Testing for authenticated users, using the resources form
class New_Resource_authentication_test(TestCase):
    def setUp(self):
        self.test_user=User.objects.create_user(username='testuser1', password='P@ssw0rd1')
        self.name=Resource.objects.create (resourcename='redline')
        self.type=Resource.objects.create(resourcetype='stapler')
        self.date=Resource.objects.create (dateentered ='2019-04-02')
        self.prod = Resource.objects.create(resourcename=self.name, resourcetype=self.type, user=self.test_user, dateentered=self.date,resourceurl= 'http://www.officedepo.com', resourcedesc="Important office tool")
        return self.setUp

    def test_redirect_if_not_logged_in(self):
        response=self.client.get(reverse('newresource'))
        self.assertRedirects(response, '/accounts/login/?next=/Club/newResource/')

    def test_Logged_in_uses_correct_template(self):
        login=self.client.login(username='testuser1', password='P@ssw0rd1')
        response=self.client.get(reverse('newresource'))
        self.assertEqual(str(response.context['user']), 'testuser1')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'Club/newresource.html')