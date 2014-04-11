from deals.models import ClaimedDeal, Deal, Vendor
from django.test import Client, TestCase
from fluxy.models import FluxyUser
import json, random

class ApiPermissionsTestCase(TestCase):
  fixtures = ['deals.json']

  def setUp(self):
    self.client = Client()
    self.kopa_vendor_ids = [1, 2]
    self.active_claimed_deals = [1, 2]
    self.all_claimed_deals = [1, 2, 3]
    self.new_deal = { "title": "Meet homeless people",
                       "desc": "homelessss",
                       "time_start": "2014-02-01 00:00:00+00:00",
                       "time_end": "2015-02-01 00:00:00+00:00",
                       "max_deals": 40,
                       "insructions": "Introduce yourself carefully" }
    self.new_vendor = { 'name': 'Oren\'s Hummus',
                        'address': '261 University Ave, Palo Alto CA 94301',
                        'latitude': 37.445316,
                        'longitude': -122.162197,
                        'web_url': 'http://www.yelp.com/biz/orens-hummus-shop-palo-alto',
                        'yelp_url': 'http://www.yelp.com/biz/orens-hummus-shop-palo-alto',
                        'phone': '650-752-6492' }
    self.new_claimed_deal = { "deal_id": 7 }

  def test_other_vendor_create_deal(self):
    """
    @author: Chris
    @desc: test that a user can't create a deal belonging to a vendor that
           does not belong to the user
    """
    self.client.login(username="kingofpaloalto", password="password")
    response = self.client.post('/api/v1/vendor/3/deals/',
                                json.dumps(self.new_deal),
                                content_type="application/javascript")
    self.assertEqual(response.status_code, 403)
    with self.assertRaises(Deal.DoesNotExist):
      Deal.objects.get(title=self.new_deal["title"])

  def test_other_vendor_edit_deal(self):
    """
    @author: Chris
    @desc: test that a user can't edit a deal belonging to a vendor that
           does not belong to the user
    TODO: implement PUT /vendor/id/deals
    """
    pass

  def test_other_vendor_delete_deal(self):
    """
    @author: Chris
    @desc: test that a user can't delete a deal belonging to a vendor that
           does not belong to the user
    TODO: implement DELETE /vendor/id/deals
    """
    pass

  def test_other_vendor_edit(self):
    """
    @author: Chris
    @desc: test that a user can't edit information for a vendor that
           does not belong to the user
    TODO: implement PUT /vendor/id
    """
    pass

  def test_other_vendor_delete(self):
    """
    @author: Chris
    @desc: test that a user can't delete a vendor that does not belong to
           the user
    TODO: implement DELETE /vendor/id
    """
    pass

  def test_other_vendor_get_claimed_deal(self):
    """
    @author: Chris
    @desc: test that a user can't get claimed deals for a vendor that does not
           belong to the user
    """
    self.client.login(username="kingofpaloalto", password="password")
    response = self.client.get('/api/v1/vendor/3/claimed_deals/',
                                content_type="application/javascript")
    self.assertEqual(response.status_code, 403)
    response = self.client.get('/api/v1/vendor/3/claimed_deals/all/',
                                content_type="application/javascript")
    self.assertEqual(response.status_code, 403)

  def test_logged_out_create_deal(self):
    """
    @author: Chris
    @desc: test that a logged out user can't create a deal
    """
    response = self.client.post('/api/v1/vendor/1/deals/',
                                json.dumps(self.new_deal),
                                content_type="application/javascript")
    self.assertEqual(response.status_code, 403)
    with self.assertRaises(Deal.DoesNotExist):
      Deal.objects.get(title=self.new_deal["title"])

  def test_logged_out_edit_deal(self):
    """
    @author: Chris
    @desc: test that a logged out user can't edit a deal
    TODO: implement PUT /vendor/id/deal/id
    """
    pass

  def test_logged_out_delete_deal(self):
    """
    @author: Chris
    @desc: test that a logged out user can't delete a deal
    TODO: implement DELETE /vendor/id/deal/id
    """
    pass

  def test_logged_out_claim_deal(self):
    """
    @author: Chris
    @desc: test that a logged out user can't claim a deal
    """
    response = self.client.post('/api/v1/user/claimed_deals/',
                                json.dumps(self.new_claimed_deal),
                                content_type="application/javascript")
    self.assertEqual(response.status_code, 403)
    with self.assertRaises(ClaimedDeal.DoesNotExist):
      ClaimedDeal.objects.get(deal=self.new_claimed_deal["deal_id"])

  def test_logged_out_get_claimed_deal(self):
    """
    @author: Chris
    @desc: test that a logged out user can't view claimed deals
    """
    response = self.client.get('/api/v1/user/claimed_deals/',
                                content_type="application/javascript")
    self.assertEqual(response.status_code, 403)
    response = self.client.get('/api/v1/vendor/1/claimed_deals/',
                                content_type="application/javascript")
    self.assertEqual(response.status_code, 403)
    response = self.client.get('/api/v1/user/claimed_deals/all/',
                                content_type="application/javascript")
    self.assertEqual(response.status_code, 403)

  def test_logged_out_create_vendor(self):
    """
    @author: Chris
    @desc: test that a logged out user can't create vendors
    """
    response = self.client.post('/api/v1/vendors/',
                                json.dumps(self.new_vendor),
                                content_type="application/javascript")
    self.assertEqual(response.status_code, 403)
    with self.assertRaises(Vendor.DoesNotExist):
      Vendor.objects.get(name=self.new_vendor["name"])

  def test_logged_out_edit_vendor(self):
    """
    @author: Chris
    @desc: test that a logged out user can't edit vendors
    TODO: implement PUT /vendors/id/
    """
    pass

  def test_logged_out_delete_vendor(self):
    """
    @author: Chris
    @desc: test that a logged out user can't delete vendors
    TODO: implement DELETE /vendors/id/
    """
    pass

  def tear_down(self):
    pass
