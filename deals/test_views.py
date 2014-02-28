from deals.models import Vendor, Deal
from deals.fixture_dicts import FixtureDicts
import deals.views
from django.test import Client 
from django.test import TestCase

class PostTestCase(TestCase):
  """
  Basic tests for the ability of the app to accept post requests and add
  them to the DB as appropriate.
  """
  def setUp(self):
    """
    Create our test client fixture and test objects.
    """
    self.client = Client()
    self.happy_donuts = FixtureDicts.vendor1
    self.deal1 = FixtureDicts.deal1
         
  def test_vendor_post(self):
    """
    Tests API creation of vendor on empty DB. Posts the happy_donuts dict above
    (key-values in the dict become key-values in the POST request), checks that
    the object can be retrived and contains some expected fields.
    """
    with self.assertRaises(Vendor.DoesNotExist):
      first_vendor = Vendor.objects.get(id=1)
    self.client.post('/api/v1/vendors/', self.happy_donuts)
    first_vendor = Vendor.objects.get(id=1)
    self.assertEqual(first_vendor.name, "Happy Donuts")
    self.assertAlmostEqual(first_vendor.latitude, 40)
    

  def test_deal_post(self):
    """
    Tests API creation of deal on empty DB. Adds a vendor (through the POST
    API as well), then adds deal1 to the database. Checks that the deal
    can be retrieved and contains some expected fields.
    """
    with self.assertRaises(Deal.DoesNotExist):
      first_deal = Deal.objects.get(id=1)
    self.client.post('/api/v1/vendors/', self.happy_donuts)
    self.client.post('/api/v1/deals/', self.deal1)
    first_deal = Deal.objects.get(id=1)
    self.assertEqual(first_deal.vendor.name, "Happy Donuts")
    self.assertEqual(first_deal.radius, 4)

  def tearDown(self):
    pass
