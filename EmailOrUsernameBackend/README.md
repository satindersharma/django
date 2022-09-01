### allow user to login with email or username

#### assume your app name is users 

#### create file backends.py in users app
```
users/backends.py
```
##### in settings.py
```python
AUTHENTICATION_BACKENDS = ['users.backends.EmailOrUsernameModelBackend', 'django.contrib.auth.backends.ModelBackend']
```
