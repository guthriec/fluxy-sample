from fluxy.models import FluxyUser
from deals.models import ClaimedDeal
from django.test import Client, TestCase
import json, random

class UserApiTestCase(TestCase):
  fixtures = ['deals.json']

  def setUp(self):
    self.client = Client()
    self.kingofpaloalto_vendor_ids = [1, 2]
    self.active_claimed_deals = [1, 2]
    self.all_claimed_deals = [1, 2, 3]

  def test_auth_valid(self):
    """
    @author: Rahul
    @desc: Test the auth endpoint with a valid username and password.
    """
    data = { 'email': 'kingofpaloalto', 'password': 'password' }
    response = self.client.post('/api/v1/user/auth/', data=data)
    self.assertEqual(response.status_code, 200)
    self.assertEqual(self.client.session['_auth_user_id'], 1)

  def test_auth_valid_json(self):
    """
    @author: Rahul
    @desc: Test the auth endpoint with username and password encoded as JSON
    instead of form data. Important for Backbone.
    """
    data = { 'email': 'kingofpaloalto', 'password': 'password' }
    response = self.client.post('/api/v1/user/auth/', data=json.dumps(data),
    content_type='application/json')
    self.assertEqual(response.status_code, 200)
    self.assertEqual(self.client.session['_auth_user_id'], 1)

  def test_auth_invalid_username(self):
    """
    @author: Rahul
    @desc: Test the auth endpoint with a nonexistent username.
    """
    data = { 'email': 'invalid', 'password': 'password' }
    response = self.client.post('/api/v1/user/auth/', data=data)
    self.assertEqual(response.status_code, 401)
    self.assertNotIn('auth_user_id', self.client.session)

  def test_auth_invalid_password(self):
    """
    @author: Rahul
    @desc: Test the auth endpoint with a valid username and invalid password.
    """
    data = { 'email': 'kingofpaloalto', 'password': 'invalid' }
    response = self.client.post('/api/v1/user/auth/', data=data)
    self.assertEqual(response.status_code, 401)
    self.assertNotIn('auth_user_id', self.client.session)

  def test_auth_invalid_data(self):
    """
    @author: Rahul
    @desc: Test the auth endpoint without password data.
    """
    data = { 'email': 'kingofpaloalto' }
    response = self.client.post('/api/v1/user/auth/', data=data)
    self.assertEqual(response.status_code, 400)
    self.assertNotIn('auth_user_id', self.client.session)

  def test_register(self):
    """
    @author: Rahul
    @desc: Test registration of a new user.
    """
    data = { 'email': 'testuser', 'password': 'password', 'password_confirm': 'password' }
    response = self.client.post('/api/v1/user/register/', data=data)
    self.assertEqual(response.status_code, 201)

    response = self.client.post('/api/v1/user/auth/', data=data)
    self.assertEqual(response.status_code, 200)

  def test_register_json(self):
    """
    @author: Rahul
    @desc: Test registration of a new user using a JSON formatted POST.
    """
    data = { 'email': 'testuser', 'password': 'password', 'password_confirm': 'password' }
    response = self.client.post('/api/v1/user/register/', json.dumps(data),
                                content_type='application/json')
    self.assertEqual(response.status_code, 201)

    response = self.client.post('/api/v1/user/auth/', json.dumps(data), content_type='application/json')
    self.assertEqual(response.status_code, 200)

  def test_register_existing_user(self):
    """
    @author: Rahul
    @desc: Test registration of an already existing username.
    """
    data = { 'email': 'kingofpaloalto', 'password': 'password' }
    response = self.client.post('/api/v1/user/register/', data=data)
    self.assertEqual(response.status_code, 400)

  def test_register_invalid_data(self):
    """
    @author: Rahul
    @desc: Test registration without a username field.
    """
    data = { 'password': 'password' }
    response = self.client.post('/api/v1/user/register/', data=data)
    self.assertEqual(response.status_code, 400)

  def test_user_details(self):
    """
    @author: Rahul
    @desc: Test user details api endpoint with a currently authenticated user.
    """
    data = { 'email': 'kingofpaloalto', 'password': 'password' }
    response = self.client.post('/api/v1/user/auth/', data=data)
    self.assertEqual(response.status_code, 200)

    response = self.client.get('/api/v1/user/')
    self.assertEqual(response.status_code, 200)

    user_list = json.loads(response.content)
    self.assertEqual(len(user_list), 1)
    user_obj = user_list[0]
    self.assertEqual(user_obj['first_name'], 'Al')
    self.assertEqual(user_obj['last_name'], 'H')
    self.assertEqual(user_obj['email'], 'alh@alh.com')

  def test_user_details_without_logged_in_user(self):
    """
    @author: Rahul
    @desc: Test user details api endpoint without a currently authenticated
    user.
    """
    response = self.client.get('/api/v1/user/')
    self.assertEqual(response.status_code, 401)

  def test_logout(self):
    """
    @author: Rahul
    @desc: Test user logout with a currently authenticated user. Logs the user
    in, logs the user out, and then tries to get details of the currently
    logged in user.
    """
    data = { 'email': 'kingofpaloalto', 'password': 'password' }
    response = self.client.post('/api/v1/user/auth/', data=data)
    self.assertEqual(response.status_code, 200)

    response = self.client.get('/api/v1/user/logout/')
    self.assertEqual(response.status_code, 200)
    self.assertNotIn('_auth_user_id', self.client.session)

  def test_logout_without_logged_in_user(self):
    """
    @author: Rahul
    @desc: Test user logout without a currently authenticated
    user. Expects a 302 temporary redirect.
    """
    response = self.client.get('/api/v1/user/logout/')
    self.assertEqual(response.status_code, 302)

  def test_user_vendors(self):
    """
    @author: Rahul
    @desc: Test user vendors api endpoint. Expects a JSON encoded array of all
    vendor objects associated with user.
    """
    data = { 'email': 'kingofpaloalto', 'password': 'password' }
    response = self.client.post('/api/v1/user/auth/', data=data)
    self.assertEqual(response.status_code, 200)

    response = self.client.get('/api/v1/user/vendors/')
    self.assertEqual(response.status_code, 200)

    vendors = json.loads(response.content)
    vendor_ids = set()
    for vendor in vendors:
      vendor_ids.add(vendor['pk'])
    self.assertSetEqual(vendor_ids, set(self.kingofpaloalto_vendor_ids))


  def test_user_vendors_empty(self):
    """
    @author: Rahul
    @desc: Test user vendors api endpoint with a user without any associated
    vendors. Expects an empty JSON array.
    """
    data = { 'email': 'idontownrestaurants', 'password': 'password' }
    response = self.client.post('/api/v1/user/auth/', data=data)
    self.assertEqual(response.status_code, 200)

    response = self.client.get('/api/v1/user/vendors/')
    self.assertEqual(response.status_code, 200)

    vendors = json.loads(response.content)
    vendor_ids = set()
    for vendor in vendors:
      vendor_ids.add(vendor['pk'])
    self.assertSetEqual(vendor_ids, set([]))

  def test_user_vendors_without_logged_in_user(self):
    """
    @author: Rahul
    @desc: Test user vendors api endpoint without a logged in user. Expects a
    401.
    """
    response = self.client.get('/api/v1/user/vendors/')
    self.assertEqual(response.status_code, 401)

  def test_active_claimed_deals(self):
    """
    @author: Rahul
    @desc: Test user claimed deal endpoint with authenticated user. Expects a
    list of active claimed deals.
    """
    data = { 'email': 'idontownrestaurants', 'password': 'password' }
    response = self.client.post('/api/v1/user/auth/', data=data)
    self.assertEqual(response.status_code, 200)

    response = self.client.get('/api/v1/user/claimed_deals/')
    self.assertEqual(response.status_code, 200)

    claimed_deals = json.loads(response.content)
    claimed_deal_ids = set()
    for claimed_deal in claimed_deals:
      claimed_deal_ids.add(claimed_deal['pk'])
    self.assertSetEqual(claimed_deal_ids, set(self.active_claimed_deals))

  def test_active_claimed_deals_without_logged_in_user(self):
    """
    @author: Rahul
    @desc: Test user claimed deal endpoint without an authenticated user.
    Expects a 401.
    """
    response = self.client.get('/api/v1/user/claimed_deals/')
    self.assertEqual(response.status_code, 401)

  def test_all_claimed_deals(self):
    """
    @author: Rahul
    @desc: Test user all claimed deals endpoint with an authenticated user.
    Expects a list of all claimed deals, including those expired and those
    which have yet to start.
    """
    data = { 'email': 'idontownrestaurants', 'password': 'password' }
    response = self.client.post('/api/v1/user/auth/', data=data)
    self.assertEqual(response.status_code, 200)

    response = self.client.get('/api/v1/user/claimed_deals/all/')
    self.assertEqual(response.status_code, 200)

    claimed_deals = json.loads(response.content)
    claimed_deal_ids = set()
    for claimed_deal in claimed_deals:
      claimed_deal_ids.add(claimed_deal['pk'])
    self.assertSetEqual(claimed_deal_ids, set(self.all_claimed_deals))

  def test_claim_deal(self):
    """
    @author: Rahul
    @desc: Test claiming a deal for an authenticated user. Authenticates the
    user, creates a deal, and then checks that the deal is returned when
    hitting the all user claimed deals endpoint.
    """
    data = { 'email': 'kingofpaloalto', 'password': 'password' }
    response = self.client.post('/api/v1/user/auth/', data=data)
    self.assertEqual(response.status_code, 200)

    random_lat = round(random.random() * 180, 3)
    data = { 'deal_id': 2, 'latitude': random_lat }
    response = self.client.post('/api/v1/user/claimed_deals/', data=data)
    self.assertEqual(response.status_code, 201)

    self.assertEqual(ClaimedDeal.objects.last().claimed_latitude, random_lat)

  def test_claim_deal_json(self):
    """
    @author: Rahul
    @desc: Test claiming a deal for an authenticated user. Authenticates the
    user, creates a deal, and then checks that the deal is returned when
    hitting the all user claimed deals endpoint. POSTs the data as JSON.
    """
    data = { 'email': 'kingofpaloalto', 'password': 'password' }
    response = self.client.post('/api/v1/user/auth/', data=json.dumps(data),
                                content_type='application/json')
    self.assertEqual(response.status_code, 200)

    random_lat = round(random.random() * 180, 3)
    data = { 'deal_id': 2, 'latitude': random_lat }
    response = self.client.post('/api/v1/user/claimed_deals/', data=data)
    self.assertEqual(response.status_code, 201)

    self.assertEqual(ClaimedDeal.objects.last().claimed_latitude, random_lat)

  def test_claim_deal_without_logged_in_user(self):
    """
    @author: Rahul
    @desc: Test claiming a deal for a user without an authenticated user.
    Expects a 401.
    """
    response = self.client.post('/api/v1/user/claimed_deals/')
    self.assertEqual(response.status_code, 401)

  def test_claim_deal_with_nonexistent_deal(self):
    """
    @author: Rahul
    @desc: Test claiming a nonexistent deal for an authenticated user. Expects
    a 400 response.
    """
    data = { 'email': 'kingofpaloalto', 'password': 'password' }
    response = self.client.post('/api/v1/user/auth/', data=json.dumps(data),
                                content_type='application/json')
    self.assertEqual(response.status_code, 200)

    random_lat = round(random.random() * 180, 3)
    data = { 'deal_id': -10, 'latitude': random_lat }
    response = self.client.post('/api/v1/user/claimed_deals/', data=data)
    self.assertEqual(response.status_code, 400)

    self.assertNotEqual(ClaimedDeal.objects.last().claimed_latitude, random_lat)

  def test_claim_deal_with_maxed_claim_count(self):
    """
    @author: Rahul
    @desc: Test claiming a completely claimed deal with an authenticated user.
    Expects a 400 response.
    """
    self.assertEqual(0, 1) # TODO implement this!

  def test_claim_deal_with_expired_deal(self):
    """
    @author: Rahul
    @desc: Test claiming an expired deal for an authenticated user. Expects a
    400 response.
    """
    data = { 'email': 'kingofpaloalto', 'password': 'password' }
    response = self.client.post('/api/v1/user/auth/', data=json.dumps(data),
                                content_type='application/json')
    self.assertEqual(response.status_code, 200)

    random_lat = round(random.random() * 180, 3)
    data = { 'deal_id': 3, 'latitude': random_lat }
    response = self.client.post('/api/v1/user/claimed_deals/', data=data)
    self.assertEqual(response.status_code, 400)

    self.assertNotEqual(ClaimedDeal.objects.last().claimed_latitude, random_lat)

  def tear_down(self):
    pass
