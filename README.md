# django





#### Django RuntimeWarning
 Django raises a warning when you attempt to save a naive datetime to the database:
```
 RuntimeWarning: DateTimeField ModelName.field_name received a naive
datetime (2012-01-01 00:00:00) while time zone support is active.
```

to handel this warning

use

```python
import django
from sys import argv
import os
from django.utils import timezone
import random
# from time import sleep
from faker import Faker
import warnings
# from django.contrib.auth.hashers import make_password

# the below line is copied from wsgi file
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CelecUserProject.settings')
django.setup()


def random_data(ne=100, es=3):
    for _ in range(ne):
        f = Faker('en_US')
        data = {
            # "date_time": f.date_time_this_century(before_now=True, after_now=False, tzinfo=None),
            # "date_time": timezone.now(), 
            "date_time": f.past_datetime(start_date='-0d', tzinfo=None), # '-30d' for last 30 day data '-0d' means today '-1d' means from yesterday to today
            # "date_time": f.date_time_this_year(before_now=True, after_now=False, tzinfo=None),
            "saving": random.randrange(0, 101),
            "usage": random.randrange(0, 101),
            "energy": round(random.uniform(0, 101), 2),
            "power_factor": round(random.uniform(0, 101), 3),
            "thd": round(random.uniform(0, 101), 2),
            "tdi": round(random.uniform(0, 101), 2),
        }
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            DashboardTable.objects.create(**data)
            # sleep(es)
    print(f'{ne} new data created successfully')


if __name__ == '__main__':
    # autopip8 will shift this to up so imorting here as it should be after django setup
    from ermapp.models import DashboardTable
    print('filling some random data')
    if len(argv) == 1:
        random_data()
    elif len(argv) <= 3:
        # print(argv)
        # when you do python new_data.py 23 here argv[0] is random_post.py, argv[1] is 23
        if len(argv) == 2:
            random_data(ne=int(argv[1]))
        else:
            random_data(ne=int(argv[1]), es=int(argv[2]))
    else:
        random_data()
```





## Update form inital if there is UpdateView:
## Or passing another form model initial to a combine form
```python
class LeadForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(LeadForm, self).__init__(*args, **kwargs)
        # print("intial sevalue", self)
        # print("intial arvalue", args)
        # print("intial arvalue", kwargs)
        # print("cdfd",self.fields["followup_date"].initial)
        c_lead = kwargs.get("instance")
        # c_followup = None
        if c_lead is not None:
            # print(self.fields["followup_date"].value)
            try:
                c_followup = Followup.objects.get(lead_id=c_lead)
                self.fields["followup_status_id"].initial = c_followup.followup_status_id
                self.fields["followup_score_id"].initial = c_followup.followup_score_id
                self.fields["followup_date"].initial = c_followup.followup_date
                self.fields["followup_remarks"].initial = c_followup.followup_remarks
            except Followup.DoesNotExist:
                print("c_followup.DoesNotExist")
```


## comparing date
## or writing error for form field
```python
from django.utils.translation import gettext, gettext_lazy as _
from django.utils import timezone
from django.utils.dateparse import parse_date
    def clean_followup_date(self):
        followup_date = self.cleaned_data.get('followup_date')
        # print("fty",type(followup_date))
        # print("fty",type(timezone.localdate()))
        # print(followup_date < timezone.localdate())
        if followup_date is not None and (followup_date < timezone.localdate()):
            msg = _("Past date not allowed.")
            self.add_error('followup_date', msg)
        return followup_date
```







## How to make email uniqe

add unique_together = ('email',) to the user model
helpful when you inheriting the abstract model and don't want to touch the way abstract define the email
```python
    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        db_table = 'user'
        unique_together = ('email',)
 ```



# from invalid ajax response

#### according ot document.

```python
def form_invalid(self, form):
    response = super().form_invalid(form)
        # queryset = object_list if object_list is not None else self.object_list
        # AttributeError: 'SpareFormView' object has no attribute 'object_list'
    if self.request.is_ajax():
        return JsonResponse(form.errors, status=400)
    return response
```
# But

##### above cause following error if you class inherite ListView alongside of CreateView i.e class MyClass(CreateView, ListView)
        #     # queryset = object_list if object_list is not None else self.object_list
        #     # AttributeError: 'SpareFormView' object has no attribute 'object_list'
to resolve this change form_invalid to this

```python
from django.http import JsonResponse, HttpResponse
def form_invalid(self, form):
    if self.request.is_ajax():
        errors = form.errors.as_json()
        return HttpResponse(errors, status=400, content_type='application/json')
    return super().form_invalid(form)
```



# Run without providing port no in django

as default port for http is 80 as mention here [wikipeida Port](https://en.wikipedia.org/wiki/Port_(computer_networking))

so 


`python manage.py runserver 0.0.0.0:80`


will run app on 
`192.168.0.190` (i.e without providing port no)

or

just by typing `localhost`

so we don't neet to provide port to run in browser


# Make timezone aware

```python

from django.utils import timezone

def make_timezone_aware(i_time):
    """Make datetime with timezone aware(means add timezone info to the datetime(if not))

    Args:
        tz_str (str): Timezone eg. 'Asia/Kolkata'
        i_time (str): datetime eg. '2021-12-28 14:32:14'

    Returns:
        datetime: Timezone aware datetime
    """
    # import pytz
    # from django.utils import timezone
    # current_tz = timezone.get_current_timezone()
    # timezone.activate(pytz.timezone('Asia/Kolkata'))
    # tt = '2021-12-28 14:32:14'
    # from django.utils.dateparse import parse_datetime
    # naive = parse_datetime(tt)
    # timezone.is_aware(naive)
    # new_naive = naive.replace(tzinfo=current_tz)                 
    # timezone.is_aware(new_naive)
    current_tz = timezone.get_current_timezone()
    # as i_time is already a datetime object so no need of 
    # naive = parse_datetime(tt)
    if not timezone.is_aware(i_time):
        new_naive = i_time.replace(tzinfo=current_tz) 
        return new_naive
    # logger.info(f'Time returned: {i_time}')
    return i_time
    
 ```


## access dict key (eg assest-id, or 'first name')

### create folder `templatetags` in your django app
#### create two python file `__init__.py` and `dict_tag.py`

#### in `templatetags/dict_tag.py`

```python
from django import template
register = template.Library()


@register.filter(name='dict_key')
def dict_key(d, key):
   return d.get(key)
```

### in your html

```html

{% load dict_tag %}

{{c_asset.params|dict_key:'unit-name'}}

{{asset|dict_key:'asset-id'}}

```

### django-fcm
#### https://console.firebase.google.com/
Step 1: Create a Firebase Project

Goto firebase console and click on `Add project` to create a new firebase project. Since the goal of using firebase is its cloud messaging feature, you can disable Google Analytics.


Step 2: Download a JSON File Including Project's Credentials

Next to the `Project Overview` on the left menu there is a gear icon which redirects you to the `project settings` page.

Click on the gear icon and select `Project settings`

Then, click on ``Service accounts and then click on `Generate new private key`. Download and store the JSON file on your device.

Security Note: Do NOT keep this file inside the project root and never publish it on Github, Gitlab,...


### urls
```python
      path('base/',
         include(
             ('project.apps.base.api.urls', 'base'),
             namespace='base'
         )
         ),
      path('',
         include(('project.apps.account.urls', 'account'), namespace='account')
         ),
         
         
    path('api/v0.1/',
         include(('project.urls.api', 'api'), namespace='api')
         ),
         
         
    path('account/',
         include(
             ('project.apps.account.api.urls', 'account'),
             namespace='account'
         )
         ),
         
```



### adding user on form_valid
###### https://docs.djangoproject.com/en/4.1/topics/class-based-views/generic-editing/#model-forms
```python
class AuthorCreateView(LoginRequiredMixin, CreateView):
    model = Author
    fields = ['name']

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return CreateView.form_valid(self, form)
        
```



### How to write API

#### API View
####  `view.py`

```python

import logging
from .serializers import SerializerAPIAccount
from .response_format import format_API_response
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.status import HTTP_400_BAD_REQUEST
from rest_framework.views import APIView

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------
# ViewAPIAccount
# ---------------------------------------------------------------
class ViewAPIAccount(APIView):

    serializer_class = SerializerAPIAccount

    # ---------------------------------------------------------------
    # get_serializer
    # ---------------------------------------------------------------
    def get_serializer(self, *args, **kwargs):
        """
        Return the serializer instance
        """
        return serl.serializer_class(*args, **kwargs)

    # ---------------------------------------------------------------
    # post
    # ---------------------------------------------------------------
    def post(self, request, *args, **kwargs):

        serializer = self.serializer_class(
            data=request.data,
            context={'request': request}
        )

        if serializer.is_valid():
            response = serializer.save()
            data = {
                'code': 200,
                'status': 'success',
                'result': response,
                'message':'Registered successfully'
            }
            return Response(
                data,
                status=HTTP_200_OK
            )
        data = {
            'code': 400,
            'status': 'error',
            'result': serializer.errors,
            # 'message':'Registration failed. Please try again.'
        }
        return Response(
            data,
            status=HTTP_400_BAD_REQUEST
        )


```

### Custom Pagination

`custom_pagination.py`

```python
from collections import OrderedDict
import logging

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

logger = logging.getLogger(__name__)


#-------------------------------------------------------------------------------
# CustomPageNumberPagination
#-------------------------------------------------------------------------------
class CustomPageNumberPagination(PageNumberPagination):

    page_size = 5
    current_page = 1
    page_size_query_param = 'page_size'

    #---------------------------------------------------------------------------
    # get_paginated_response
    #---------------------------------------------------------------------------
    def get_paginated_response(self, data):

        previous_page_number = next_page_number = 0
        if self.get_next_link():
            next_page_number = self.page.number + 1

        if self.get_previous_link():
            previous_page_number = self.page.number - 1 if self.page.number > 0 else 1

        pagination = OrderedDict([
            ('lastPage', self.page.paginator.num_pages),
            ('last_page', self.page.paginator.num_pages),
            ('pageSize', self.page_size),
            ('page_size', self.page_size),
            ('totalItems', self.page.paginator.count),
            ('total_items', self.page.paginator.count),
            ('current', self.page.number),
            ('next', next_page_number),
            ('previous', previous_page_number),
            ('previous_page_link', self.get_previous_link()),
            ('next_page_link', self.get_next_link())
        ])

        return Response(
            OrderedDict([
                ('pagination', pagination),
                ('results', data),
            ])
        )
```



