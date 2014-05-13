from django.core import serializers
from django.http import HttpResponse, HttpResponseRedirect
import json

def list_from_qset(qset, include_nested=False, flatten=True):
  """
  @author: Ayush, Chris
  @desc: Takes a Django QuerySet and from that generates a JSON-serializable list,
  with a form determined by other parameters.

  @param qset: QuerySet to turn into a list
  @param include_nested: Boolean value that decides if foreign object
  information should be included. Only goes through first level.
  @param flatten: Should the list have structure [pk, model, fields = [xyz]] or
                                                    [xyz] (flattened)
  """
  json_data = serializers.serialize("json", qset, use_natural_keys=include_nested)
  obj_list = json.loads(json_data)
  return_list = []

  for obj in obj_list:
    if flatten:
      attrs = obj['fields']
      attrs['id'] = obj['pk']
      return_list.append(attrs)
    else:
      return_list.append(obj)
  return return_list

def make_post_response(obj_list, redirect_addr=None, known_error=None):
  """
  @author: Ayush, Chris
  @desc: Helper function that generates appropriate response given any "known
  error" dict. Creates an appropriate response to POST request.

  @param obj_list: object that was created, in JSON-serializable list form
  @param redirect_addr: address to redirect to
  @param known_error: Any known errors to include/encode in POST response

  @return: JSON HttpResponse with status 200 on sucess otherwise with error
  """
  response = { 'status': 201,
               'error': None,
               'detail': None,
               'data': None,
               'success': True }
  if known_error:
    response['status'] = known_error['status']
    response['detail'] = known_error['detail']
    response['success'] = False
  response['data'] = obj_list
  if redirect_addr:
    return HttpResponseRedirect(redirect_addr, json.dumps(response),
                                content_type="application/json",
                                status=response['status'])
  else:
    return HttpResponse(json.dumps(response),
                        content_type="application/json",
                        status=response['status'])

def make_get_response(resp_list, known_error=None):
  """
  @author: Ayush, Chris
  @desc: Helper function to take a JSON-serializable list and an optional
  "known error" dict (with keys 'message' and 'code'), and create an appropriate
  response to a GET request.

  @param resp_list: JSON-serializable list to include in GET response
  @param known_error: Any known errors to include/encode in GET response

  @returns: JSON HttpResponse with status 200 on success
            JSON HttpResponse with appropriate error code if known_error
  """
  if known_error:
    code = known_error['status']
    return HttpResponse(json.dumps(known_error),\
                        content_type="application/json", status=code)
  else:
    json_out = json.dumps(resp_list)
    return HttpResponse(json_out, content_type="application/json", status=200)

def make_put_response(single_obj_list, known_error=None):
  response = { 'status': 200,
               'error': None,
               'detail': None,
               'success': True,
               'data': single_obj_list }
  if known_error:
    response['status'] = known_error['status']
    response['error'] = known_error['error']
    response['detail'] = known_error['detail']
    response['success'] = False
  return HttpResponse(json.dumps(response), content_type="application/json",
                      status=response['status'])

def custom_serialize(qset, options = None):
  """
  @author: Rahul
  @desc: Helper function to serialize models in a non-standard manner.
  Expects the model that makes up the passed-in qlist to have a method
  get_custom_serializable which returns an object with the desired properties.

  @param qset: A query-set containing the objects to be serialized

  @returns: An array of the customized models.
  """
  return map(lambda obj: obj.get_custom_serializable(options), qset)
