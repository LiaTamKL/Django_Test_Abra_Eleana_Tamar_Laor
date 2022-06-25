In order to turn production mode on, you must switch in wsgi.py, asgi.py and manage.py the variable DJANGO_SETTINGS_MODULE to backend.settings.prod
If you do so, the app will not run on your local version however.

The read field in the message table is for aesthetic purposes only. It is not used to determine which messages are unread (instead, there is a seperate field for that).
It can be removed without effecting how the app determines which message is unread. 
It was added because I did not understand if the assignment wanted me to determine unread status via the message model or via a seperate model so I've placed the read boolean field in message to show that that's an option as well, if you'd like it changed to that.


To use Postman, Abra_Assignment_Eleana_Laor_Complete.postman_collection is the file you need. Import it to Postman to use it
