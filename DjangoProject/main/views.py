from django.shortcuts import render
from main.forms import UserForm
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


class IndexView(TemplateView):
    template_name = "main/index.html"


def register(request):
    """
    Allows user to register
    Author: Rana El-Garem

    """
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)

        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            registered = True

        else:
            print user_form.errors
    else:
        user_form = UserForm()

    return render(request, 'main/register.html',
                  {'user_form': user_form, 'registered': registered})


def user_login(request):
    """
    ALlows User to login
    Author: Rana El-Garem

    """
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/main/')
            else:
                return HttpResponse("Your account has been disabled")

        else:
            print "Invalid login details: {0}, {1}".format(username, password)
            return HttpResponse("Invalid login details supplied.")

    else:
        return render(request, 'main/login.html', {})


@login_required
def user_logout(request):
    """
    Allows user to logout
    Author: Rana El-Garem

    """
    logout(request)
    return HttpResponseRedirect('/main/')
