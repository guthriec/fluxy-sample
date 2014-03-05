fluxy_web_app
=============

Fluxy Web Stack 


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

API (planned)
-----------
Endpoints supporting GET and POST:
```
/deals
```
Returns all active deals, including those that are maxed out.

```
/deals/all
```
Returns all deals ever created.

```
/deal/{id}
```
Returns full 


```
/vendors
```

Endpoints supporting GET only:
```
/api/v1/deals/{id}
/api/v1/vendors/{id}
/api/v1/vendors/{id}/deals
```

Mock API
-------------
Supports only GET:
```
/api/mock/deals
/api/mock/vendors
/api/mock/deals/{id}
/api/mock/vendors/{id}
```
