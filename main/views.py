from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import RepairRequest

def home(request):
    return render(request, 'main/home.html')

def about(request):
    return render(request, 'main/about.html')

def contacts(request):
    return render(request, 'main/contacts.html')

@login_required
def create_request(request):
    if request.method == 'POST':
        RepairRequest.objects.create(
            user=request.user,
            full_name=request.POST.get('full_name'),
            phone=request.POST.get('phone'),
            email=request.POST.get('email'),
            company=request.POST.get('company'),
            locomotive_type=request.POST.get('locomotive_type'),
            locomotive_model=request.POST.get('locomotive_model'),
            locomotive_number=request.POST.get('locomotive_number'),
            repair_type=request.POST.get('repair_type'),
            problem_description=request.POST.get('problem_description'),
            urgent=request.POST.get('urgent') == 'on'
        )
        messages.success(request, 'Заявка успешно отправлена!')
        return redirect('profile')
    return render(request, 'main/create_request.html')