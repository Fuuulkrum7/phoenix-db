# app/views.py
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from .models import LoginData, WorkerByRole, Role
from django.http import HttpResponse

# app/views.py
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from app.models import LoginData, WorkerByRole

# app/views.py
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from app.models import LoginData, WorkerByRole

def custom_login(request):
    if request.user.is_authenticated:
        try:
            login_data = LoginData.objects.get(worker_login=request.user.username)
            worker = login_data.worker.worker
            worker_role = WorkerByRole.objects.get(worker=worker)
            role = worker_role.level_code.level_code
            request.session['user_id'] = worker.worker_id
            request.session['user_role'] = role
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

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                request.session['username'] = username
                try:
                    login_data = LoginData.objects.get(worker_login=username)
                    worker = login_data.worker.worker
                    worker_role = WorkerByRole.objects.get(worker=worker)
                    role = worker_role.level_code.level_code
                    request.session['user_id'] = worker.worker_id
                    request.session['user_role'] = role

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
