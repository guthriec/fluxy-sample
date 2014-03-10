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
    @desc:
    """
    data = {'username': 'kingofpaloalto', 'password': 'password'}
    response = self.client.post('/user/auth/', data=json.dumps(data))
    self.assertEqual(response.statusCode, 200)

  def test_auth_invalid_username(self):
    """
    @author: Rahul
    @desc:
    """
    data = {'username': 'invalid', 'password': 'password'}
    response = self.client.post('/user/auth/', data=data)
    self.assertEqual(response.statusCode, 401)

  def test_auth_invalid_userjk(self):
    """
    @author: Rahul
    @desc:
    """
    data = {'username': 'invalid', 'password': 'password'}
    response = self.client.post('/user/auth/', data=data)
    self.assertEqual(response.statusCode, 401)

  def test_register(self):
    """
    @author: Rahul
    @desc:
    """

  def test_register_existing_user(self):
    """
    @author: Rahul
    @desc:
    """

  def test_logout(self):
    """
    @author: Rahul
    @desc:
    """

  def test_logout_without_logged_in_user(self):
    """
    @author: Rahul
    @desc:
    """

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
