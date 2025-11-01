from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import IntegrityError
from .models import materials
import pandas as pd
import matplotlib.pyplot as plt, seaborn as sns


# Create your views here.
def deligator_home(request):
    return render(request, 'deligator/deligator_home.html')


def deligator_login(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
        print(email)
        if email == "admin@gmail.com" and password == "admin":
            print(email)
            request.session['deligator'] = "admin@gmail.com"
            messages.info(request, "Successfully Registered")
            return render(request, 'deligator/deligator_home.html')
        elif email != "admin@gmail.com":
            messages.error(request, "Wrong Mail id")
            return render(request, 'deligator/deligator_login.html')
        elif password != "admin":
            messages.error(request, "Wrong password")
            return render(request, 'deligator/deligator_login.html')
        else:
            return render(request, 'deligator/deligator_login.html')
    return render(request, 'deligator/deligator_login.html')


def deligator_logout(request):
    if 'deligator' in request.session:
        request.session.pop('deligator', None)
        messages.success(request, "deligator Logout Success")
        return redirect('/')
    else:
        return redirect('/deligator_home/')


def raw_materials(request):
    if request.method == 'POST':
        bauxite = request.POST['bauxite']
        aluminiumoxide = request.POST['aluminiumoxide']
        carbon = request.POST['carbon']
        aluminiumfluoride = request.POST['aluminiumfluoride']
        cryolite = request.POST['cryolite']
        electricalenergy = request.POST['electricalenergy']
        materials(bauxite=bauxite, aluminiumoxide=aluminiumoxide, carbon=carbon,
                  aluminiumfluoride=aluminiumfluoride, cryolite=cryolite, electricalenergy=electricalenergy).save()
        messages.success(request, "Raw Materials Added Successfully")
    return render(request, 'deligator/deligator_raw_materials.html')


def send_raw_details(request):
    if 'deligator' in request.session:
        d = materials.objects.filter(send_agent=False)
        return render(request, 'deligator/deligator_send_raw_details.html', {'d': d})


def materials_sent(request, id):
    if 'deligator' in request.session:
        d = materials.objects.get(id=id)
        d.send_agent = True
        d.save()
        messages.success(request, "Materials Sent Successfully to Agent")
        return redirect('/send_raw_details/')


def res_details(request):
    d = materials.objects.filter(scrap_send=True)
    return render(request, 'deligator/deligator_residue.html', {'d': d})


def statistics(request):
    return render(request, 'deligator/stati.html')


def stati(request):
    data = pd.read_csv('aluminium dataset.csv')
    data.groupby('bauxite (kg)')['aluminium (kg)'].aggregate(['mean', 'median']).plot.bar()
    plt.show()
    return redirect('/statistics/')