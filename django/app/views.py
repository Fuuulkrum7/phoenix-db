# app/views.py

from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from .models import LoginData, WorkerByRole
from django.contrib.auth.decorators import login_required
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
                    worker = login_data.worker_id
                    roles = list(WorkerByRole.objects.filter(worker_id=worker).values_list('level_code', flat=True))
                    print(roles)

                    # Сохраняем данные в сессии
                    request.session['username'] = username
                    request.session['user_id'] = worker.worker_id
                    request.session['user_roles'] = roles
                    request.session['user_role'] = roles[0]  # Сохраняем первую роль как основную

                    # Перенаправление в зависимости от ролей
                    if 'A' in roles:
                        return redirect('/admin/')
                    elif 'T' in roles:
                        return redirect('/tutor/')
                    elif 'C' in roles:
                        return redirect('/curator/')
                    elif 'M' in roles:
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

def forbidden(request):
    return render(request, 'core/forbidden.html')