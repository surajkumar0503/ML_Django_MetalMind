from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import IntegrityError
from .models import ScrapRegistration
from app_deligator.models import materials


# Create your views here.
def scrap_home(request):
    return render(request, 'scrap/scrap_home.html')


def scrap_register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        contact = request.POST['contact']
        date_of_birth = request.POST['dob']
        address = request.POST['address']
        password = request.POST['password']
        try:
            ScrapRegistration(username=username, email=email, contact=contact,
                                date_of_birth=date_of_birth, address=address,
                                password=password).save()
            messages.info(request, "scrap successfully registered")
            return redirect('/scrap_login/')
        except IntegrityError as e:
            messages.info(request, "Email already exists")
            return redirect('/scrap_register/')
    return render(request, 'scrap/scrap_register.html')


def scrap_login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        try:
            r = ScrapRegistration.objects.get(email=email, password=password)
            request.session['scrap'] = r.email
            if r is not None:
                messages.info(request, 'Welcome to scrap Page')
                return redirect('/scrap_home/')
        except ScrapRegistration.DoesNotExist as e:
            messages.info(request, 'Wrong Credentials')
            return redirect('/scrap_login/')
    else:
        return render(request, 'scrap/scrap_login.html')
    return render(request, 'scrap/scrap_login.html')


def scrap_logout(request):
    if 'scrap' in request.session:
        request.session.pop('scrap', None)
        messages.success(request, "scrap Logout Success")
        return redirect('/')
    else:
        return redirect('/scrap_home/')


def residue_details(request):
    d = materials.objects.all()
    return render(request, 'scrap/scrap_residue_details.html', {'d':d})


def residue_details_send(request):
    d = materials.objects.filter(scrap_send=False)
    return render(request, 'scrap/scrap_details_send.html', {'d':d})


def residue_send(request, id):
    d = materials.objects.get(id=id)
    d.scrap_send = True
    d.save()
    messages.success(request, "Details sent to Deligator")
    return redirect('/residue_details_send/')
