from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import IntegrityError
from .models import rlAgentRegistration
from app_deligator.models import materials
import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import QuantileRegressor
import warnings
warnings.filterwarnings('ignore')
import math


# Create your views here.
def agent_home(request):
    return render(request, 'agent/agent_home.html')


def agent_register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        contact = request.POST['contact']
        date_of_birth = request.POST['dob']
        address = request.POST['address']
        password = request.POST['password']
        try:
            rlAgentRegistration(username=username, email=email, contact=contact,
                                date_of_birth=date_of_birth, address=address,
                                password=password).save()
            messages.info(request, "Agent successfully registered")
            return redirect('/agent_login/')
        except IntegrityError as e:
            messages.info(request, "Email already exists")
            return redirect('/agent_register/')
    return render(request, 'agent/agent_register.html')


def agent_login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        try:
            r = rlAgentRegistration.objects.get(email=email, password=password)
            request.session['agent'] = r.email
            if r is not None:
                messages.info(request, 'Welcome to Agent Page')
                return redirect('/agent_home/')
        except rlAgentRegistration.DoesNotExist as e:
            messages.info(request, 'Wrong Credentials')
            return redirect('/agent_login/')
    else:
        return render(request, 'agent/agent_login.html')
    return render(request, 'agent/agent_login.html')


def agent_logout(request):
    if 'agent' in request.session:
        request.session.pop('agent', None)
        messages.success(request, "Agent Logout Success")
        return redirect('/')
    else:
        return redirect('/agent_home/')


def material_view(request):
    d = materials.objects.filter(send_agent=True)
    return render(request, 'agent/agent_material_view.html', {'d': d})


def to_process(request, id):
    d = materials.objects.get(id=id)
    d.progress_bar = True
    d.save()
    messages.success(request, "Aluminium Production Process Finished")
    return redirect('/progress_bar/')


def progress_bar(request):
    d = materials.objects.filter(progress_bar=True, send_agent=True)
    return render(request, 'agent/agent_progress_bar.html', {'d': d})


def algorithm(datas,r):
    # print(datas)
    # data = pd.DataFrame(pd.read_excel("aluminium dataset.xlsx"))
    # read_file = pd.read_excel("aluminium dataset.xlsx")
    # read_file.to_csv("aluminium dataset.csv", header=True, index=False)
    data = pd.DataFrame(pd.read_csv("aluminium dataset.csv"))
    # data = pd.read_csv('Construction Cost.csv')
    data_x = data.iloc[:, :-1]
    data_y = data.iloc[:, -1]
    string_datas = [i for i in data_x.columns if data_x.dtypes[i] == np.object_]

    LabelEncoders = []
    for i in string_datas:
        newLabelEncoder = LabelEncoder()
        data_x[i] = newLabelEncoder.fit_transform(data_x[i])
        LabelEncoders.append(newLabelEncoder)
    ylabel_encoder = None
    if type(data_y.iloc[1]) == str:
        ylabel_encoder = LabelEncoder()
        data_y = ylabel_encoder.fit_transform(data_y)

    model = QuantileRegressor()
    model.fit(data_x, data_y)
    value = {data_x.columns[i]: datas[i] for i in range(len(datas))}
    l = 0
    for i in string_datas:
        z = LabelEncoders[l]
        value[i] = z.transform([value[i]])[0]
        l += 1
    value = [i for i in value.values()]
    predicted = model.predict([value])
    if ylabel_encoder:
        predicted = ylabel_encoder.inverse_transform(predicted)
    return predicted[0]
# a = algorithm([15, 330, 310, 220])
# print(int(a))


def analyse(request):
    d = materials.objects.all()
    return render(request, 'agent/agent_analyse.html', {'d':d})


def apply_algorithm(request, id):
    if 'agent' in request.session:
        details = materials.objects.get(id=id)
        r = details.id
        details.aluminium_predict = True
        details.save()
        input_value = []
        a = details.bauxite
        b = details.aluminiumoxide
        c = details.carbon
        d = details.aluminiumfluoride
        e = details.cryolite
        f = details.electricalenergy
        print(a)
        print(b)
        print(c)
        print(d)
        print(e)
        print(f)
        print(f'id: {r}')
        input_value.append(a)
        input_value.append(b)
        input_value.append(c)
        input_value.append(d)
        input_value.append(e)
        input_value.append(f)
        print(input_value)
        algo = math.ceil(algorithm(input_value,r))
        print(f'Target: {algo}')
        materials.objects.filter(id=r).update(aluminium=algo)
        messages.success(request, 'Analysation Finished')
    return redirect('/analyse/')


def residue_page(request):
    d = materials.objects.all()
    return render(request, 'agent/agent_residue_page.html', {'d': d})


def create_residue(request, id):
    d = materials.objects.get(id=id)
    balance = d.aluminium / 2
    redMud = int(d.aluminium + balance)
    print(redMud)
    d.red_mud = redMud
    d.residue = True
    d.save()
    print(d.red_mud)
    messages.success(request, f"{redMud}Kgs of residue is created and Sent to Scrap Management")
    return redirect('/residue_page/')

