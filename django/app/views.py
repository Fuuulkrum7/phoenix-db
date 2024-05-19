# app/views.py
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from .models import LoginData, WorkerByRole, Role
from django.http import HttpResponse
def custom_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)

                # Определение роли пользователя
                try:
                    login_data = LoginData.objects.get(worker_login=username)
                    worker = login_data.worker.worker
                    worker_role = WorkerByRole.objects.get(worker=worker)
                    role = worker_role.level_code.level_code

                    if role == 'A':
                        return redirect('/admin/')
                    elif role == 'T':
                        return redirect('/tutor/')
                    elif role == 'C':
                        return redirect('/curator/')
                    elif role == 'M':
                        return redirect('/methodist/')
                    else:
                        return redirect('/')
                except LoginData.DoesNotExist:
                    return redirect('/')
                except WorkerByRole.DoesNotExist:
                    return redirect('/')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

def index(request):
    return HttpResponse("Hello, world! This is the index page.")
