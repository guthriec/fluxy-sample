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
