import math
import warnings
import numpy as np
import pandas as pd
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import IntegrityError
from sklearn.linear_model import QuantileRegressor
from sklearn.exceptions import NotFittedError
from .models import rlAgentRegistration
from app_deligator.models import materials

warnings.filterwarnings("ignore")


# ----------  BASIC VIEWS  ----------
def agent_home(request):
    return render(request, "agent/agent_home.html")


def agent_register(request):
    if request.method == "POST":
        data = {
            "username": request.POST["username"],
            "email": request.POST["email"],
            "contact": request.POST["contact"],
            "date_of_birth": request.POST["dob"],
            "address": request.POST["address"],
            "password": request.POST["password"],
        }
        try:
            rlAgentRegistration.objects.create(**data)
            messages.success(request, "Agent successfully registered")
            return redirect("/agent_login/")
        except IntegrityError:
            messages.error(request, "Email already exists")
            return redirect("/agent_register/")
    return render(request, "agent/agent_register.html")


def agent_login(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
        try:
            agent = rlAgentRegistration.objects.get(email=email, password=password)
            request.session["agent"] = agent.email
            messages.success(request, "Welcome to Agent Page")
            return redirect("/agent_home/")
        except rlAgentRegistration.DoesNotExist:
            messages.error(request, "Wrong Credentials")
    return render(request, "agent/agent_login.html")


def agent_logout(request):
    request.session.pop("agent", None)
    messages.success(request, "Agent Logout Success")
    return redirect("/")


# ----------  MATERIAL FLOW ----------
def material_view(request):
    mats = materials.objects.filter(send_agent=True)
    return render(request, "agent/agent_material_view.html", {"d": mats})


def to_process(request, id):
    mat = materials.objects.get(id=id)
    mat.progress_bar = True
    mat.save()
    messages.success(request, "Aluminium Production Process Finished")
    return redirect("/progress_bar/")


def progress_bar(request):
    mats = materials.objects.filter(progress_bar=True, send_agent=True)
    return render(request, "agent/agent_progress_bar.html", {"d": mats})


# ----------  MACHINE LEARNING ALGORITHM ----------
def algorithm(datas, _):
    """
    Modernized Quantile Regression predictor.
    Handles NaN, dtype coercion, and missing dataset safely.
    """
    try:
        df = pd.read_csv("aluminium dataset.csv", engine="python", on_bad_lines="skip")
    except FileNotFoundError:
        return 0.0

    X = df.iloc[:, :-1].apply(pd.to_numeric, errors="coerce").fillna(0)
    y = pd.to_numeric(df.iloc[:, -1], errors="coerce").fillna(0)

    model = QuantileRegressor()
    try:
        model.fit(X.astype(float), y.astype(float))
        val = np.array(datas, dtype=float).reshape(1, -1)
        pred = model.predict(val)
        return float(pred[0])
    except (ValueError, NotFittedError, Exception):
        return float(y.mean())


# ----------  ANALYSIS ----------
def analyse(request):
    mats = materials.objects.all()
    return render(request, "agent/agent_analyse.html", {"d": mats})


def apply_algorithm(request, id):
    if "agent" not in request.session:
        return redirect("/agent_login/")

    details = materials.objects.get(id=id)
    details.aluminium_predict = True
    details.save()

    inputs = [
        details.bauxite,
        details.aluminiumoxide,
        details.carbon,
        details.aluminiumfluoride,
        details.cryolite,
        details.electricalenergy,
    ]

    result = algorithm(inputs, id)
    if math.isnan(result):
        result = 0
    result = math.ceil(result)

    materials.objects.filter(id=id).update(aluminium=result)
    messages.success(request, f"Analysis Finished – Predicted yield: {result} kg")
    return redirect("/analyse/")


# ----------  RESIDUE CREATION ----------
def residue_page(request):
    mats = materials.objects.all()
    return render(request, "agent/agent_residue_page.html", {"d": mats})


def create_residue(request, id):
    mat = materials.objects.get(id=id)
    balance = mat.aluminium / 2
    red_mud = int(mat.aluminium + balance)
    mat.red_mud = red_mud
    mat.residue = True
    mat.save()
    messages.success(
        request, f"{red_mud} kg of residue created and sent to Scrap Management"
    )
    return redirect("/residue_page/")