from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import IntegrityError
from .models import rlEnvironmentRegistration


# Create your views here.
def environment_home(request):
    return render(request, 'environment/environment_home.html')


def environment_register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        contact = request.POST['contact']
        date_of_birth = request.POST['dob']
        address = request.POST['address']
        password = request.POST['password']
        try:
            rlEnvironmentRegistration(username=username, email=email, contact=contact,
                                date_of_birth=date_of_birth, address=address,
                                password=password).save()
            messages.info(request, "environment successfully registered")
            return redirect('/environment_login/')
        except IntegrityError as e:
            messages.info(request, "Email already exists")
            return redirect('/environment_register/')
    return render(request, 'environment/environment_register.html')


def environment_login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        try:
            r = rlEnvironmentRegistration.objects.get(email=email, password=password)
            request.session['environment'] = r.email
            if r is not None:
                messages.info(request, 'Welcome to environment Page')
                return redirect('/environment_home/')
        except rlEnvironmentRegistration.DoesNotExist as e:
            messages.info(request, 'Wrong Credentials')
            return redirect('/environment_login/')
    else:
        return render(request, 'environment/environment_login.html')
    return render(request, 'environment/environment_login.html')


def environment_logout(request):
    if 'environment' in request.session:
        request.session.pop('environment', None)
        messages.success(request, "environment Logout Success")
        return redirect('/')
    else:
        return redirect('/environment_home/')
