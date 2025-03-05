from django.shortcuts import render

from .models import Ledger


# Create your views here.


def index(request):
    
    if request.method == "GET":
        
        return render(request, "index.html",)

def about(request):
    
    if request.method == "GET":
        
        return render(request, "about.html",)


def ledger(request):
    
    if request.method == "GET":
        
        return render(request, "ledger.html",)

def add_ledger(request):
    if request.method == "GET":
        return render(request, "add-ledger.html")

    if request.method == "POST":
        name = request.POST.get("name")
        ledger_type = request.POST.get("type")  # Avoid using 'type' as a variable name

        if name and ledger_type:
            Ledger.objects.create(name=name, ledger_type=ledger_type)  # Ensure this field exists in your model
            return redirect("ledger")

        return render(request, "add-ledger.html", {"error": "All fields are required!"})


def wallet(request):
    
    if request.method == "GET":
        
        return render(request, "wallet.html",)


def service(request):
    
    if request.method == "GET":
        
        return render(request, "service.html",)

def contact(request):
    
    if request.method == "GET":
        
        return render(request, "contact.html",)
