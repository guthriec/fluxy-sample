from deals.api_tools import make_get_response
from functools import wraps

def api_login_required(methods):
  """
  @author: Chris
  @desc: Checks if any user is logged in. If a user is logged in, returns
         None. Otherwise, returns an appropriate JSON error response.
  """
  def decorator(func):
    def inner_decorator(request, *args, **kwargs):
      if request.method in methods:
        if not request.user.is_authenticated():
          known_error = { 'code': 403, 'message': 'No logged in user' }
          return make_get_response(None, known_error)
      return func(request, *args, **kwargs)

    return wraps(func)(inner_decorator)

  return decorator

def api_vendor_required(methods):
  """
  @author: Chris
  @desc: Checks if the user is logged in and if the logged-in user has
         permissions for vendor_id.
         If the user has permissions, returns None.
         Otherwise, returns an appropriate JSON error response.
  """
  def decorator(func):
    def inner_decorator(request, *args, **kwargs):
      if request.method in methods:
        vendor_id = kwargs['vendor_id']
        if not request.user.is_authenticated():
          known_error = { 'code': 403, 'message': 'No logged in user' }
          return make_get_response(None, known_error)
        elif int(vendor_id) not in [vendor.id for vendor in request.user.vendors.all()]:
          known_error = { 'code': 403, 'message': 'User does not own vendor' }
          return make_get_response(None, known_error)
      return func(request, *args, **kwargs)

    return wraps(func)(inner_decorator)

  return decorator
