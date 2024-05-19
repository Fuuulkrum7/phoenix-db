# core/views/curator_views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from core.forms import AddChildForm

@login_required
def add_child(request):
    if request.method == 'POST':
        form = AddChildForm(request.POST)
        if form.is_valid():
            # Process the form data here (e.g., save to the database)
            # For now, we will just print it
            print(form.cleaned_data)
            return redirect('curator')  # Redirect to the curator dashboard or any other page
    else:
        form = AddChildForm()
    
    return render(request, 'core/add_child.html', {'form': form})
