from social.pipeline.partial import partial
from django.shortcuts import redirect


@partial
def redirect_to_login_form(backend, user, response, *args, **kwargs):
    #print(kwargs['details']['fullname'])
    print(kwargs)
    return redirect('home')
