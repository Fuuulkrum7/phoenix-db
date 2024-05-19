# app/views.py
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from .models import LoginData, WorkerByRole

from .models import LoginData, WorkerByRole, Role
from django.http import HttpResponse


## Custom login view that handles user authentication and role-based redirection.
#  @param request The HTTP request object.
#  Authenticates the user, determines their role, and redirects to the appropriate page based on their role.
#  If the user is already authenticated, it immediately redirects based on the role saved in the session.
#  If the login fails or user data is not found, it redirects to the login page.
#  Supports roles like Admin ('A'), Tutor ('T'), Curator ('C'), and Methodist ('M').
#
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
                    worker = login_data.worker
                    worker_roles = WorkerByRole.objects.filter(worker=worker)
                    roles = [role.level_code.level_code for role in worker_roles]

                    # Сохраняем данные в сессии
                    request.session['username'] = username
                    request.session['user_id'] = worker.worker_id
                    request.session['user_roles'] = roles

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