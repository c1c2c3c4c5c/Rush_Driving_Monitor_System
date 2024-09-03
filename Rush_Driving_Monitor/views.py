from django.contrib.auth import logout, authenticate, login
from django.http import HttpResponseRedirect
from django.shortcuts import render


class AuthenticationViews:
    @staticmethod
    def login(request):
        if request.method == "POST":
            post = dict(request.POST)
            username = post['email-username'][0]
            password = post['password'][0]
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                request_url = request.GET.get('next')
                print(request_url)
                return HttpResponseRedirect(request_url if request_url else '/')
            else:
                return render(request, "login.html", {"error": "invalid", "username": username})
        return render(request, "login.html", {"error": "", "username": ""})

    @staticmethod
    def register(request):
        return render(request, "register.html")

    @staticmethod
    def logout(request):
        if request.user.is_authenticated:
            logout(request)
            return HttpResponseRedirect('/')
        else:
            return HttpResponseRedirect('/')