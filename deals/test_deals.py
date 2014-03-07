from deals.models import Deal
from django.test import Client 
from django.test import TestCase
import json

class DealTestCase(TestCase):
  fixtures = ['deals.json']
  
  def setUp(self):
    """
    Create our test client object.
    """
    self.client = Client()
    self.deal_list = list(range(1, 8))
    self.inactive_list = [3, 7]
    self.mile_pt = (37.407959, -122.121454)
    self.mile_incl_active = [1, 2]
    self.mile_incl_all = [1, 2, 3]
         
  def test_single_deal(self):
    response = self.client.get('/api/v1/deal/2')
    print response.content
    deal_obj = json.loads(response.content)[0]
    self.assertEqual(deal_obj['title'], "40% off coffee")
    self.assertEqual(deal_obj['vendor']['name'], "Happy Donuts")
   
  def test_deal_not_found(self):
    response = self.client.get('/api/v1/deal/100')
    self.assertEqual(response.status_code, 404)

  def test_single_deal_inactive(self):
    response = self.client.get('/api/v1/deal/3')
    print response.content
    deal_obj = json.loads(response.content)[0]
    # Should still return the object
    self.assertEqual(deal_obj['title'], "20% off shitty sandwiches")
    self.assertEqual(deal_obj['vendor']['name'], "Happy Donuts")

  def test_deals_active_only(self):
    response = self.client.get('/api/v1/deals')
    print response.content
    deal_list = json.loads(response.content)
    for deal in deal_list:
      self.assertNotIn(deal['pk'], self.inactive_list)

  def test_deals_all(self):
    response = self.client.get('/api/v1/deals/all')
    deal_list = json.loads(response.content)
    pks = set()
    for deal in deal_list:
      pks.add(deal['pk'])
    self.assertSetEqual(pks, set(self.deal_list))

  def test_deals_radius(self):
    response = self.client.get('/api/v1/deals', {'lat': self.mile_pt[0],\
                                                 'long': self.mile_pt[1],\
                                                 'radius': 1})
    deal_list = json.loads(response.content)
    pks = set()
    for deal in deal_list:
      pks.add(deal['pk'])
    self.assertSetEqual(pks, set(self.mile_incl_active))

  def test_deals_all_radius(self):
    response = self.client.get('/api/v1/deals/all', {'lat': self.mile_pt[0],\
                                                     'long': self.mile_pt[1],\
                                                     'radius': 1})
    deal_list = json.loads(response.content)
    pks = set()
    for deal in deal_list:
      pks.add(deal['pk'])
    self.assertSetEqual(pks, set(self.mile_incl_all))

  def tearDown(self):
    pass
