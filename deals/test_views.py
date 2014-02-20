from dateutil import parser
from deals.models import Vendor, Deal
import deals.views
from django.test import Client 
from django.test import TestCase

class PostTestCase(TestCase):
  def setUp(self):
    self.client = Client()
    self.happy_donuts = {'name' : "Happy Donuts",
                         'address' : "111 El Camino",
                         'business_type' : "Restaurant",
                         'latitude' : 40,
                         'longitude' : 80,
                         'web_url' : "http://www.happydonuts.com",
                         'yelp_url' : "http://www.yelp.com/biz/happy_d"}
    self.deal1 = {'vendor_id' : 1,
                  'title' : "50% off donuts",
                  'desc' : "50% off any donut!",
                  'radius' : 4,
                  'time_start' : parser.parse("2014-02-19 05:00 UTC"),
                  'time_end' : parser.parse("2014-02-19 09:00 UTC")}

  def test_vendor_post(self):
    with self.assertRaises(Vendor.DoesNotExist):
      first_vendor = Vendor.objects.get(id=1)
    self.client.post('/vendors/', self.happy_donuts)
    first_vendor = Vendor.objects.get(id=1)
    self.assertEqual(first_vendor.name, "Happy Donuts")
    self.assertAlmostEqual(first_vendor.latitude, 40)
    

  def test_deal_post(self):
    with self.assertRaises(Deal.DoesNotExist):
      first_deal = Deal.objects.get(id=1)
    self.client.post('/vendors/', self.happy_donuts)
    first_vendor = Vendor.objects.get(id=1)
    self.client.post('/deals/', self.deal1)
    first_deal = Deal.objects.get(id=1)
    self.assertEqual(first_deal.vendor.name, "Happy Donuts")
    self.assertEqual(first_deal.radius, 4)

  def tearDown(self):
    pass
