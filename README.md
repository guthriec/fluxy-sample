Fluxy Web Stack
===============


Deploying
-----------
To deploy latest commit from ```master``` to ```prod```, you want to follow the following command.
**Please be sure you want to deploy. Otherwise we should follow a deployment schedule.**
```sh
ssh [username]@fluxyapp.com
cd /srv/www/fluxyapp.com/public
git fetch origin
git rebase origin/master
```

Fixtures
----------
Feel free to update the fixtures, but beware that some tests we're writing currently hardcode properties of the fixtures. If you update the fixtures and see failing tests, first check to be sure you don't have to update these properties (all of which should be instance variables of the test class).

For example, if you add a deal that should be inactive, in test_deals.py be sure to update self.deal_list and self.inactive_list.

API
-----------
* ``` /deal/{id} ```
  * Accepts GET.
  * Returns a full deal object, serializing vendor information as an embedded object.

* ``` /deals ```
  * Accepts GET.
  * Returns all active deals, including those that are maxed out.
  * If all of the following GET parameters are set: "lat", "long", and "radius," the returned set is limited to deals within 'radius' of the given coordinates. Radius <= 0 is taken as an unlimited radius.

* ``` /deals/all ```
  * Accepts GET.
  * Returns all deals ever created.
  * If all of the following GET parameters are set: "lat", "long", and "radius," the returned set is limited to deals within 'radius' of the given coordinates. Radius <= 0 is taken as an unlimited radius.

* ``` /user/ ```
  * Accepts GET.
  * If user is authenticated, returns the user object associated with the user. Otherwise, returns a 403.

* ``` /user/auth ```
  * Accepts POST.
  * Takes POST parameters 'username' and 'password', attempts to authenticate the user, returns 200 on success, 401 on inability ot authenticate. Authentication lasts until cookie is cleared (for now).

* ``` /user/vendor ```
  * Accepts GET.
  * If user is authenticated, returns the vendor objects associated with the user. If the user is not associated with a vendor, returns an empty object. If the user is not authenticated, returns 403.

* ``` /user/claimed_deals ```
  * Accepts GET, POST.
  * GET returns a list of active ClaimedDeal objects associated with the user. POST creates a new ClaimedDeal object associated with the user. Returns 400 on bad POST. If the user is not authenticated, returns 403.

* ``` /user/claimed_deals/all ```
  * Accepts GET.
  * If user is authenticated, returns a list of all ClaimedDeal objects associated with the user. If the user is not authenticated, returns 403.

* ``` /user/register ```
  * Accepts POST.
  * Registers 'username' and 'password' POST fields as a new user with minimal permissions, returns 201 on success. If the user is already registered, returns 409.

* ``` /user/logout ```
  * Accepts GET.
  * Logs out current user, returns 200 on success.

* ``` /vendors ```
  * Accepts GET, POST.
  * GET returns a list of all vendors. 200 on success. POST creates a vendor object. 201 on success, 403 if no permissions, 400 on bad POST.

* ``` /vendor/{id} ```
  * Accepts GET, PUT.
  * GET returns full vendor object associated with {id}, PUT modifies this object. Returns 200 on success. If user does not have PUT permissions, returns 403. If no vendor of {id} exists on a PUT request, returns 404.

* ``` /vendor/{id}/deals ```
  * Accepts GET, POST.
  * GET returns all active deals associated with {id}, with no embedded vendor object. Returns 200 on success. POST creates a deal associated with {id}, returns 201 on success. If user does not have POST permissions for {id}, returns 403. If no vendor of {id} exists returns 404.

* ``` /vendor/{id}/deals/{id} ```
  * Accepts GET, PUT.
  * Get returns deal associated with {id} with no embedded vendor object. Returns 200 on success. If user does not have PUT permissions, returns 403. If no vendor of {id} exists, returns 404. If no deal of {id} exists on a PUT request, returns 404.

* ``` /vendor/{id}/deals/all ```
  * Accepts GET.
  * Returns all deals associated with {id}. Returns 200 on success, 404 if no vendor of {id} exists.

* ``` /vendor/{id}/claimed_deals ```
  * Accepts GET.
  * Returns all active claimed_deals objects associated with {id}. Returns 200 on success, 404 if no vendor of {id} exists.

* ``` /vendor/{id}/claimed_deals/all ```
  * Accepts GET.
  * Returns all claimed_deals objects associated with {id}. Returns 200 on success, 404 if no vendor of {id} exists.

