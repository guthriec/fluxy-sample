from fluxy.models import FluxyUser
from django.test import Client, TestCase
import json

class UserApiTestCase(TestCase):
  fixtures = ['deals.json']

  def setUp(self):
    self.client = Client()

  def test_auth_valid(self):
    """
    @author: Rahul
    @desc: Test the auth endpoint with a valid username and password.
    """
    data = {'username': 'kingofpaloalto', 'password': 'password'}
    response = self.client.post('/user/auth/', data=data)
    self.assertEqual(response.status_code, 200)

  def test_auth_valid_json(self):
    """
    @author: Rahul
    @desc: Test the auth endpoint with username and password encoded as JSON
    instead of form data. Important for Backbone.
    """
    data = {'username': 'kingofpaloalto', 'password': 'password'}
    response = self.client.post('/user/auth/', data=json.dumps(data),
    content_type='application/json')
    self.assertEqual(response.status_code, 200)

  def test_auth_invalid_username(self):
    """
    @author: Rahul
    @desc: Test the auth endpoint with a nonexistent username.
    """
    data = {'username': 'invalid', 'password': 'password'}
    response = self.client.post('/user/auth/', data=data)
    self.assertEqual(response.status_code, 401)

  def test_auth_invalid_password(self):
    """
    @author: Rahul
    @desc: Test the auth endpoint with a valid username and invalid password.
    """
    data = {'username': 'kingofpaloalto', 'password': 'invalid'}
    response = self.client.post('/user/auth/', data=data)
    self.assertEqual(response.status_code, 401)

  def test_auth_invalid_data(self):
    """
    @author: Rahul
    @desc: Test the auth endpoint without password data.
    """
    data = {'username': 'kingofpaloalto'}
    response = self.client.post('/user/auth/', data=data)
    self.assertEqual(response.status_code, 400)

  def test_register(self):
    """
    @author: Rahul
    @desc: Test registration of a new user.
    """
    data = {'username': 'testuser', 'password': 'password'}
    response = self.client.post('/user/register/', data=data)
    self.assertEqual(response.status_code, 200)
    response = self.client.post('/user/auth/', data=data)
    self.assertEqual(response.status_code, 200)

  def test_register_json(self):
    """
    @author: Rahul
    @desc: Test registration of a new user using a JSON formatted POST.
    """
    data = {'username': 'testuser', 'password': 'password'}
    response = self.client.post('/user/register/', data=json.dumps(data),
                                content_type='application/json')
    self.assertEqual(response.status_code, 200)
    response = self.client.post('/user/auth/', data=data)
    self.assertEqual(response.status_code, 200)

  def test_register_existing_user(self):
    """
    @author: Rahul
    @desc: Test registration of an already existing username.
    """
    data = {'username': 'kingofpaloalto', 'password': 'password'}
    response = self.client.post('/user/register/', data=data)
    self.assertEqual(response.status_code, 400)

  def test_register_invalid_data(self):
    """
    @author: Rahul
    @desc: Test registration without a username field.
    """
    data = {'password': 'password'}
    response = self.client.post('/user/register/', data=data)
    self.assertEqual(response.status_code, 400)

  def test_user_details(self):
    """
    @author: Rahul
    @desc: Test user details api endpoint with a currently authenticated user.
    """
    data = {'username': 'kingofpaloalto', 'password': 'password'}
    response = self.client.post('/user/auth/', data=data)
    self.assertEqual(response.status_code, 200)
    response = self.client.get('/api/v1/user/')
    self.assertEqual(response.status_code, 200)
    user_obj = json.loads(response.content)
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
    self.assertEqual(response.status_code, 403)

  def test_logout(self):
    """
    @author: Rahul
    @desc: Test user logout with a currently authenticated user. Logs the user
    in, logs the user out, and then tries to get details of the currently
    logged in user.
    """
    data = {'username': 'kingofpaloalto', 'password': 'password'}
    response = self.client.post('/user/auth/', data=data)
    self.assertEqual(response.status_code, 200)
    response = self.client.get('/user/logout/')
    self.assertEqual(response.status_code, 200)
    response = self.client.get('/api/v1/user/')
    self.assertEqual(response.status_code, 403)

  def test_logout_without_logged_in_user(self):
    """
    @author: Rahul
    @desc: Test user logout without a currently authenticated
    user. Expects a 302 temporary redirect.
    """
    response = self.client.get('/user/logout/')
    self.assertEqual(response.status_code, 302)

  def test_active_claimed_deals(self):
    """
    @author: Rahul
    @desc:
    """

  def test_active_claimed_deals_without_logged_in_user(self):
    """
    @author: Rahul
    @desc:
    """

  def test_all_claimed_deals(self):
    """
    @author: Rahul
    @desc:
    """

  def test_claim_deal(self):
    """
    @author: Rahul
    @desc:
    """

  def test_claim_deal_without_logged_in_user(self):
    """
    @author: Rahul
    @desc:
    """

  def test_claim_deal_with_nonexistent_deal(self):
    """
    @author: Rahul
    @desc:
    """

  def test_claim_deal_with_maxed_claim_count(self):
    """
    @author: Rahul
    @desc:
    """

  def test_claim_deal_with_expired_deal(self):
    """
    @author: Rahul
    @desc:
    """

  def tear_down(self):
    pass
