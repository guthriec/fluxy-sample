import django.contrib.auth
from django.contrib.auth.models import check_password
from fluxy.models import FluxyUser

class FacebookEnabledBackend(object):
  def authenticate(self, username=None, password=None, access_token=None):
    if access_token:
      fb_profile = urllib.urlopen('https://graph.facebook.com/me?access_token={0}'.format(access_token))
      fb_profile = json.loads(fb_profile)
      fb_id = fb_profile['id']
      user = None
      try:
        fb_user = FacebookUser.objects.get(facebook_id=fb_id)
        fb_user.access_token = access_token
        fb_user.save()
        user = FluxyUser.objects.get(pk=fb_user.user_id)
      except FacebookUser.DoesNotExist:
        fb_email = fb_profile.email
        new_user = FluxyUser.objects.create_user(email=fb_email, username=fb_email, password="unsafeunsaferedalert", fb_only=True)
        new_user.save()
        new_fb_user = FacebookUser.objects.create(user_id=new_user.id, facebook_id=fb_id, access_token=access_token)
        user = FluxyUser.objects.get(pk=new_fb_user.user_id)
    else:
      user = django.contrib.auth.authenticate(username=username, password=password)
      if user:
        if user.fb_only:
          user = None
    return user

  def get_user(self, user_id):
    try:
      return FluxyUser.objects.get(pk=user_id)
    except FluxyUser.DoesNotExist:
      return None
