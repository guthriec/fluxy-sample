from fluxy.models import FacebookUser, FluxyUser
import json
import urllib2

class FacebookBackend(object):
  '''
  @author: Chris
  @desc: Facebook authentication backend
  '''
  def authenticate(self, access_token=None):
    '''
    @author: Chris
    @desc: authenticates token with Facebook server, then looks up and
           returns corresponding FluxyUser. If no FluxyUser has been
           associated with the user's Facebook acccount, this method
           creates that user, saves it to the DB, and returns it.
    '''
    if access_token:
      fb_profile = urllib2.urlopen('https://graph.facebook.com/me?access_token={0}'.format(access_token)).read()
      fb_profile = json.loads(fb_profile)
      fb_id = fb_profile['id']
      user = None
      try:
        fb_user = FacebookUser.objects.get(facebook_id=fb_id)
        fb_user.access_token = access_token
        fb_user.save()
        user = FluxyUser.objects.get(pk=fb_user.user_id)
      except FacebookUser.DoesNotExist:
        fb_email = fb_profile['email']
        new_user = FluxyUser.objects.create_user(email=fb_email, username=fb_email, password="unsafeunsaferedalert", fb_only=True)
        new_user.save()
        new_fb_user = FacebookUser.objects.create(user_id=new_user.id, facebook_id=fb_id, access_token=access_token)
        user = FluxyUser.objects.get(pk=new_fb_user.user_id)
      return user
    else:
      return None

  def get_user(self, user_id):
    '''
    @author: Chris
    @desc: Basic implementation of get_user, should be identical to default
           behavior
    '''
    try:
      return FluxyUser.objects.get(pk=user_id)
    except FluxyUser.DoesNotExist:
      return None
