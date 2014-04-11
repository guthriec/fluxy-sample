from fluxy.models import FluxyUser
from deals.models import ClaimedDeal, Deal
from django.test import Client, TestCase
import json, random

class ApiPermissionsTestCase(TestCase):
  fixtures = ['deals.json']

  def setUp(self):
    self.client = Client()
    self.kopa = FluxyUser.objects.get(username="kingofpaloalto")
    self.kopa_vendor_ids = [1, 2]
    self.active_claimed_deals = [1, 2]
    self.all_claimed_deals = [1, 2, 3]
    self.new_deal = { "title": "Meet homeless people",
                       "desc": "homelessss",
                       "time_start": "2014-02-01 00:00:00+00:00",
                       "time_end": "2015-02-01 00:00:00+00:00",
                       "max_deals": 40,
                       "instructions": "Introduce yourself carefully" }


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
    pass
  def test_logged_out_create_deal(self):
    pass
  def test_logged_out_edit_deal(self):
    pass
  def test_logged_out_delete_deal(self):
    pass
  def test_logged_out_claim_deal(self):
    pass
  def test_logged_out_get_claimed_deal(self):
    pass
  def test_logged_out_create_vendor(self):
    pass
  def test_logged_out_edit_vendor(self):
    pass
  def test_logged_out_delete_vendor(self):
    pass
  def tear_down(self):
    pass
