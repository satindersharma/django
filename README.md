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
