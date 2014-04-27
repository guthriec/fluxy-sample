from deals.models import Deal
from django.test import Client
from django.test import TestCase
import json

class VendorDealTestCase(TestCase):
  fixtures = ['deals.json']

  def setUp(self):
    # Create our test client object.
    self.client = Client()
    self.client.login(username="kingofpaloalto", password="password")
    self.donut_list = list(range(1, 4))
    self.inactive_donuts = [3]

  def test_deals_post(self):
    """
    @author: Chris
    Tests that POSTing to /vendor/1/deals creates a new Happy
    Donuts deal.
    """
    new_deal = { "title": "Meet homeless people",
                 "desc": "homelessss",
                 "time_start": "2014-02-01 00:00:00+00:00",
                 "time_end": "2015-02-01 00:00:00+00:00",
                 "max_deals": 40,
                 "instructions": "Introduce yourself carefully" }

    response = self.client.post('/api/v1/vendor/1/deals/', json.dumps(new_deal),
                                content_type="application/javascript")
    self.assertEqual(response.status_code, 201)
    self.assertEqual(Deal.objects.filter(vendor=1, title="Meet homeless people").count(), 1)

  def test_bad_deals_post(self):
    """
    @author: Chris
    Tests that POSTing to /vendor/1/deals with an extra field gives a 400.
    """
    new_deal = { "title": "Meet homeless people",
                 "desc": "homelessss",
                 "time_start": "2014-02-01 00:00:00+00:00",
                 "time_end": "2015-02-01 00:00:00+00:00",
                 "max_deals": 40,
                 "bad_instructions": "Introduce yourself carefully" }
    response = self.client.post('/api/v1/vendor/1/deals/', json.dumps(new_deal),
                                content_type="application/javascript")
    self.assertEqual(response.status_code, 400)

  def test_deals_active_only(self):
    """
    @author: Chris
    Tests that /vendor/1/deals only returns active deals
    """
    response = self.client.get('/api/v1/vendor/1/deals/')
    deal_list = json.loads(response.content)
    for deal in deal_list:
      self.assertNotIn(deal['id'], self.inactive_donuts)

  def test_deals_all(self):
    """
    @author: Chris
    Tests that /vendor/1/deals/all returns all deals
    """
    response = self.client.get('/api/v1/vendor/1/deals/all/')
    deal_list = json.loads(response.content)
    ids = set()
    for deal in deal_list:
      ids.add(deal['id'])
    self.assertSetEqual(ids, set(self.donut_list))

  def test_bad_vendor(self):
    """
    @author: Chris
    Tests that /vendor/100/deals returns 404
    """
    response = self.client.get('/api/v1/vendor/100/deals/')
    self.assertEqual(response.status_code, 404)

  def test_put(self):
    """
    @author: Chris
    Tests that a valid put on /vendor/1/deal/1 returns 200 and updates
    the deal
    """
    deal_edit = { "desc": "A new description",
                  "max_deals": "300" }
    response = self.client.put('/api/v1/vendor/1/deal/1/',
                               data=json.dumps(deal_edit),
                               content_type="application/json")
    returned_deal = json.loads(response.content)[0]
    self.assertEqual(returned_deal['desc'], "A new description")
    self.assertEqual(returned_deal['max_deals'], "300")
    self.assertEqual(response.status_code, 200)
    db_dealset = Deal.objects.filter(pk=1)
    self.assertEqual(db_dealset.count(), 1)
    self.assertEqual(db_dealset[0].desc, "A new description")
    self.assertEqual(db_dealset[0].max_deals, 300)

  def test_malformed_put(self):
    """
    @author: Chris
    Tests that an invalid put on /vendor/1/deal/1 returns 400 and does not
    update the deal
    """
    deal_edit = { "poop": "A new description",
                  "max_deals": "300" }
    response = self.client.put('/api/v1/vendor/1/deal/1/',
                               data=json.dumps(deal_edit),
                               content_type="application/json")
    self.assertEqual(response.status_code, 400)
    db_dealset = Deal.objects.filter(pk=1)
    self.assertEqual(db_dealset.count(), 1)
    self.assertEqual(db_dealset[0].max_deals, 30)

  def test_bad_vendor_put(self):
    """
    @author: Chris
    Tests that a valid put on /vendor/100/deal/1 returns 404
    """
    deal_edit = { "desc": "A new description",
                  "max_deals": "300" }
    response = self.client.put('/api/v1/vendor/100/deal/1/',
                               data=json.dumps(deal_edit),
                               content_type="application/json")
    self.assertEqual(response.status_code, 404)
    db_dealset = Deal.objects.filter(pk=1)
    self.assertEqual(db_dealset.count(), 1)
    self.assertEqual(db_dealset[0].max_deals, 30)

  def test_bad_deal_put(self):
    """
    @author: Chris
    Tests that a valid put on /vendor/1/deal/100 returns 404
    """
    deal_edit = { "desc": "A new description",
                  "max_deals": "300" }
    response = self.client.put('/api/v1/vendor/1/deal/100/',
                               data=json.dumps(deal_edit),
                               content_type="application/json")
    self.assertEqual(response.status_code, 404)

  def tearDown(self):
    pass
