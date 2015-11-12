from django.http import HttpResponseRedirect
from django.contrib.auth import logout as auth_logout
from django.core.urlresolvers import reverse


# logout function
def get_logout(request):

    auth_logout(request)
    return HttpResponseRedirect(reverse("home"))
