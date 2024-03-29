Fluxy Web Stack
===============

Getting started
---------------
We assume that you have ```pip``` installed. If you do not, use ```brew``` to
install it.

Make sure you have ```virtualenv``` installed by running:
```sh
[sudo] pip install virtualenv
```

Next we create the virtual environment and load the necessary dependencies:
```sh
virtualenv venv
. venv/bin/activate
pip install -r requirements.txt
```

Next we need to make sure you create a local database. Run the following and
follow the instructions:
```sh
python manage.py syncdb
```

Good, you are now setup. Close this terminal window and follow the instructions
in the "Starting your local enviornment" part of the README.

Starting your local enviornment
-------------------------------
Assuming you are in the correct directory, you need to activate the virtual
environment and run the server. Run:
```sh
. venv/bin/activate
python manage runserver
```

You can now access the web stack at: ```127.0.0.1:8000```

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
For all POST and PUT requests, data must be encoded using JSON.  Remember to
set the request's CONTENT-TYPE header to '/application/json'.

Deals have 5 stages:
  * 0 = Expired: The deal's end time has passed.
  * 1 = Live: The deal can currently be redeemed at its vendor.
  * 2 = Active: The deal cannot yet be redeemed but it is claimable.
  * 3 = Scheduled: The deal cannot yet be claimed.
  * 4 = Cancelled.

* ``` /deals/{id} ```
  * Accepts GET.
  * Returns a full deal object, serializing vendor information as an embedded object.

* ``` /deals ```
  * Accepts GET.
  * Returns all active deals, including those that are maxed out.
  * If all of the following GET parameters are set: "lat", "long", and "radius," the returned set is limited to deals within 'radius' of the given coordinates. Radius <= 0 is taken as an unlimited radius.
  * If the "lat" and "long" parameters are set: the returned set will include a
    "distance" attribute for each deal which indicates the number of miles to
    the vendor who posted the deal

* ``` /deals/all ```
  * Accepts GET.
  * Returns all deals ever created.
  * If all of the following GET parameters are set: "lat", "long", and "radius," the returned set is limited to deals within 'radius' of the given coordinates. Radius <= 0 is taken as an unlimited radius.

* ``` /user/ ```
  * Accepts GET.
  * If user is authenticated, returns the user object associated with the user. Otherwise, returns a 403.

* ``` /user/auth ```
  * Accepts POST.
  * Takes POST parameters 'email' and 'password', attempts to authenticate the user. If POST parameter is instead 'access_token', authenticates the user through Facebook. Returns a 200 on success, 401 on bad credentials, a 400 on a bad request, or a 403 if the user submits no authentication token but has only ever authenticated via Facebook. Has JSON, whose 'success' key indicates if the login credentials were valid or not. Authentication lasts until cookie is cleared (for now).

* ``` /user/vendors ```
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
  * Accepts GET, PUT, DELETE.
  * Get returns deal associated with {id} with no embedded vendor object. Returns 200 on success. If user does not have PUT or DELETE permissions, returns 403. If no vendor of {id} exists, returns 404. If no deal of {id} exists on a PUT or DELETE request, returns 404.

* ``` /vendor/{id}/deals/all ```
  * Accepts GET.
  * Returns all deals associated with {id}. Returns 200 on success, 404 if no vendor of {id} exists.

* ``` /vendor/{id}/claimed_deals ```
  * Accepts GET.
  * Returns all active claimed_deals objects associated with {id}. Returns 200 on success, 403 if logged in user doesn't have permissions for vendor of {id}, 404 if no vendor of {id} exists.

* ``` /vendor/{id}/claimed_deals/all ```
  * Accepts GET.
  * Returns all claimed_deals objects associated with {id}. Returns 200 on success, 403 if logged in user doesn't have permissions for vendor of {id}, 404 if no vendor of {id} exists.

* ``` /vendor/{id}/photos/ ```
  * Accepts GET, POST, DELETE.
  * GET returns a list of all photos for a vendor. POST expects a
    multipart/form-data encoded request with the image stored under the key
    'photo'. Returns a 201 on success. Returns a 403 if the user doesn't have
    permissions for vendor with id {id}. DELETE returns a 200 if the user has
    permissions and the photo exists. It deletes the database object and the
    file itself from the server.

* ``` /feedback/ ```
  * Accepts POST.
  * POST requests requires a single key, 'message', which is stored along with
    the user as a Feedback object. Returns a 201.

=======
APPENDIX A - Notes About Libraries
----------------------------------
* ```JQuery UI``` - Requires: Spinner with Smoothness Theme
