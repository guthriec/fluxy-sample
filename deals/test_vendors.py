from deals.models import Vendor 
from django.test import Client 
from django.test import TestCase
import json

class VendorTestCase(TestCase):
  fixtures = ['deals.json']
  
  def setUp(self):
    self.client = Client()
    # List of all vendors
    self.vendor_list = [1, 2, 3]
         
  def test_get_vendors(self):
    """
    @author: Chris
    Tests that GET on /vendors/ returns a list of all vendors.
    """
    response = self.client.get('/api/v1/vendors/')
    vendor_list = json.loads(response.content)
    ids = set()
    for vendor in vendor_list:
      ids.add(vendor['id'])
    self.assertSetEqual(ids, set(self.vendor_list))
  
  def test_post_vendors(self):
    """
    @author: Chris
    Tests that POST on /vendors/ creates a new vendor and returns 201.
    """
    new_vendor = { 'name': 'Oren\'s Hummus',
                  'address': '261 University Ave, Palo Alto CA 94301',
                  'latitude': 37.445316,
                  'longitude': -122.162197,
                  'web_url': 'http://www.yelp.com/biz/orens-hummus-shop-palo-alto',
                  'yelp_url': 'http://www.yelp.com/biz/orens-hummus-shop-palo-alto',
                  'phone': '650-752-6492'
    }
    response = self.client.post('/api/v1/vendors/', json.dumps(new_vendor), content_type="application/json")
    self.assertEqual(response.status_code, 201)
    orens = Vendor.objects.filter(name="Oren's Hummus")
    self.assertEqual(orens.count(), 1)
 
  def test_extra_fields(self):
    """
    @author: Chris
    Tests that POST on /vendors/ with extra fields returns a 400 
    """
    new_vendor = { 'name': 'Oren\'s Hummus',
                  'address': '261 University Ave, Palo Alto CA 94301',
                  'stripper_name': "Whoren's"
    }
    response = self.client.post('/api/v1/vendors/', json.dumps(new_vendor), content_type="application/json")
    self.assertEqual(response.status_code, 400)
    orens = Vendor.objects.filter(name="Oren's Hummus")
    self.assertEqual(orens.count(), 0)

  def test_single_vendor(self):
    """
    @author: Chris
    Tests that GET on a single vendor returns the expected vendor object
    """
    response = self.client.get('/api/v1/vendor/1/')
    vendor_obj = json.loads(response.content)[0]
    self.assertEqual(vendor_obj['name'], "Happy Donuts")
    self.assertEqual(vendor_obj['phone'], "111-111-1111")

  def test_vendor_not_exist(self):
    """
    @author: Chris
    Tests that GET and PUT on a non-existent vendor returns 404
    """
    response = self.client.get('/api/v1/vendor/100/')
    self.assertEqual(response.status_code, 404)
    
    # TODO: comment below out until put is implemented
    #response = self.client.put('/api/v1/vendor/100/', {})
    #self.assertEqual(response.status_code, 404)
  
  def test_vendor_put(self):
    """
    Tests that PUT on an existing vendor modifies the vendor
    """
    pass

  def tearDown(self):
    pass
