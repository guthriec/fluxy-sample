from deals.models import Deal
from django.test import Client 
from django.test import TestCase
import json

class DealTestCase(TestCase):
  fixtures = ['deals.json']
  
  def setUp(self):
    # Create our test client object.
    self.client = Client()

    # Set constants based on test fixture
    self.deal_list = list(range(1, 8))
    self.active_list = [1, 2, 4, 5, 6]
    self.mile_pt = (37.407959, -122.121454)
    self.mile_incl_active = [1, 2]
    self.mile_incl_all = [1, 2, 3]
         
  def test_single_deal(self):
    """
    @author: Chris
    Tests that /deal/2 returns an object with 'title' field
    as expected.
    """
    response = self.client.get('/api/v1/deal/2/')
    deal_obj = json.loads(response.content)[0]
    self.assertEqual(deal_obj['title'], "40% off coffee")
  
  def test_embedded_vendor(self):
    """
    @author: Chris
    Tests that /deal/2 returns an object with 'vendor/name' field
    as expected.
    """
    response = self.client.get('/api/v1/deal/2/')
    deal_obj = json.loads(response.content)[0]
    self.assertEqual(deal_obj['vendor']['name'], "Happy Donuts")
   
  def test_deal_not_found(self):
    """
    @author: Chris
    Tests that hitting a nonexistent deal (id: 100) returns a 404
    """
    response = self.client.get('/api/v1/deal/100/')
    self.assertEqual(response.status_code, 404)

  def test_single_deal_inactive(self):
    """
    @author: Chris
    Tests that hitting an expired deal (/deal/3) returns an object as expected with
    embedded vendor field.
    """
    response = self.client.get('/api/v1/deal/3/')
    deal_obj = json.loads(response.content)[0]
    self.assertEqual(deal_obj['title'], "20% off shitty sandwiches")
    self.assertEqual(deal_obj['vendor']['name'], "Happy Donuts")

  def test_deals_active_only(self):
    """
    @author: Chris
    Tests that /deals only returns active deals
    """
    response = self.client.get('/api/v1/deals/')
    deal_list = json.loads(response.content)
    ids = set()
    for deal in deal_list:
      ids.add(deal['id'])
    self.assertSetEqual(ids, set(self.active_list))

  def test_deals_all(self):
    """
    @author: Chris
    Tests that /deals/all returns all deals
    """
    response = self.client.get('/api/v1/deals/all/')
    deal_list = json.loads(response.content)
    ids = set()
    for deal in deal_list:
      ids.add(deal['id'])
    self.assertSetEqual(ids, set(self.deal_list))

  def test_deals_radius(self):
    """
    @author: Chris
    Tests that /deals radius filter works
    """
    response = self.client.get('/api/v1/deals/', {'latitude': self.mile_pt[0],
                                                  'longitude': self.mile_pt[1],
                                                  'radius': 1})
    deal_list = json.loads(response.content)
    ids = set()
    for deal in deal_list:
      ids.add(deal['id'])
    self.assertSetEqual(ids, set(self.mile_incl_active))

  def test_zero_radius(self):
    """
    @author: Chris
    Tests that /deals radius filter works
    """
    response = self.client.get('/api/v1/deals/', {'latitude': self.mile_pt[0],
                                                  'longitude': self.mile_pt[1],
                                                  'radius': 0})
    deal_list = json.loads(response.content)
    ids = set()
    for deal in deal_list:
      ids.add(deal['id'])
    self.assertSetEqual(ids, set(self.active_list))

  def test_deals_all_radius(self):
    """
    @author: Chris
    Tests that /deals/all radius filter works
    """
    response = self.client.get('/api/v1/deals/all/', {'latitude': self.mile_pt[0],
                                                      'longitude': self.mile_pt[1],
                                                      'radius': 1})
    deal_list = json.loads(response.content)
    ids = set()
    for deal in deal_list:
      ids.add(deal['id'])
    self.assertSetEqual(ids, set(self.mile_incl_all))

  def tearDown(self):
    pass
