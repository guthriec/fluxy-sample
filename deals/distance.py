import math

def distance(lat1, long1, lat2, long2):
  """
  @author: Chris
  @desc: returns the distance between to points defined by the two lat/long
  pairs. See www.johndcook.com/python_longitude_latitude.html

  @param lat1/long1: the lat/long pair of the first point
  @param lat2/long2: the lat/long pair of the second point

  @returns: distance in miles between the points
  """
  degrees_to_radians = math.pi / 180.0
  earth_radius = 3963.1676

  phi1 = (90.0 - lat1) * degrees_to_radians
  phi2 = (90.0 - lat2) * degrees_to_radians

  theta1 = long1 * degrees_to_radians
  theta2 = long2 * degrees_to_radians

  cos = (math.sin(phi1) * math.sin(phi2) * math.cos(theta1-theta2) + 
         math.cos(phi1) * math.cos(phi2))
  arc = math.acos(cos)

  return arc * earth_radius

def in_radius(lat1, long1, lat2, long2, radius):
  """
    @author: Chris
    @desc: returns True if two lat/long points are within a given radius of
    each other

    @param lat1/long1: the lat/long pair of the first point
    @param lat2/long2: the lat/long pair of the second point
    @radius: the radius by which we are checking

    @returns: True if the points are close enough, otherwise False. If radius <=0
    returns True, if a lat/long isn't fully defined returns False.
  """
  if radius <= 0:
    return True
  if None in [lat1, long1, lat2, long2]:
    return False
  return (distance(lat1, long1, lat2, long2) < radius)
