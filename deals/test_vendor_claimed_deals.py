from deals.models import Deal
from django.test import Client 
from django.test import TestCase
import json

class VendorClaimedDealTestCase(TestCase):
  fixtures = ['deals.json']
  
  def setUp(self):
    self.client = Client()
    self.donut_tuples_list = [(4, 1), (4, 2), (4, 3)]
    self.active_donut_tuples_list = [(4, 1), (4, 2)]
         
  def test_claimed_deals(self):
    """
    @author: Chris
    Tests that /vendor/1/claimed_deals returns all active claimed
    Happy Donuts deals
    """
    response = self.client.get('/api/v1/vendor/1/claimed_deals/')
    self.assertEqual(response.status_code, 200)
    user_deal_tuples = set()
    claimed_deal_list = json.loads(response.content)
    for claimed_deal in claimed_deal_list:
      user_deal_tuples.add((claimed_deal['user'], claimed_deal['deal']))
    self.assertSetEqual(user_deal_tuples, set(self.active_donut_tuples_list))

  def test_claimed_deals_all(self):
    """
    @author: Chris
    Tests that /vendor/1/claimed_deals/all returns all claimed
    Happy Donuts deals
    """
    response = self.client.get('/api/v1/vendor/1/claimed_deals/all/')
    self.assertEqual(response.status_code, 200)
    user_deal_tuples = set()
    for claimed_deal in json.loads(response.content):
      user_deal_tuples.add((claimed_deal['user'], claimed_deal['deal']))
    self.assertSetEqual(user_deal_tuples, set(self.donut_tuples_list))

  def test_bad_vendor(self):
    """
    @author: Chris
    Tests that /vendor/100/claimed_deals returns 404
    """
    response = self.client.get('/api/v1/vendor/100/claimed_deals/')
    self.assertEqual(response.status_code, 404)

  def test_bad_vendor_all(self):
    """
    @author: Chris
    Tests that /vendor/100/claimed_deals/all returns 404
    """
    response = self.client.get('/api/v1/vendor/100/claimed_deals/all/')
    self.assertEqual(response.status_code, 404)
  
  def tearDown(self):
    pass
