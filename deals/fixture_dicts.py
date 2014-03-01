from dateutil import parser

class FixtureDicts:
  '''
  Class to supply dictionaries corresponding to mock vendors and deals.
  No methods, just access the dicts directly.
  '''
  vendor1 = {'name' : "Happy Donuts",
             'address' : "111 El Camino",
             'business_type' : "Restaurant",
             'latitude' : 37.4225,
             'longitude' : 122.1653,
             'web_url' : "http://www.happydonuts.com",
             'yelp_url' : "http://www.yelp.com/biz/happy_d"}
  vendor2 = {'name' : "Thaiphoon",
             'address' : "111 Emerson",
             'business_type' : "Restaurant",
             'latitude' : 37.43,
             'longitude' : 122.166,
             'web_url' : "http://www.thaiphoon.com",
             'yelp_url' : "http://www.yelp.com/biz/thaiphoon"}
  vendors = [vendor1, vendor2]
  deal1 = {'vendor_id' : 1,
            'title' : "50% off donuts",
            'desc' : "50% off any donut!",
            'radius' : 4,
            'time_start' : "2014-02-19 05:00 UTC",
            'time_end' : "2014-02-19 09:00 UTC"}
  deal2 = {'vendor_id' : 1,
            'title' : "20% off coffee",
            'desc' : "20% off coffee coffee! coffee! coffee! coffee!\
                      coffee! coffee! coffee! coffee! coffee! coffee!\
                       coffee! coffee! coffee! coffee! coffee!!",
            'radius' : 4,
            'time_start' : "2014-02-27 05:00 UTC",
            'time_end' : "2014-02-28 09:00 UTC"}
  deals = [deal1, deal2]

