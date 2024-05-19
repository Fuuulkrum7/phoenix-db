from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from core.forms import AddTutorForm

@login_required
def add_tutor(request):
    """
    @brief Handles the addition of a new tutor.

    This view handles the submission of the AddTutorForm. It processes the form data,
    validates it, and then redirects the user to the curator dashboard upon successful submission.
    If the request method is not POST, it renders the form for the user to fill out.

    @param request The HTTP request object containing metadata about the request.

    @return The rendered add_tutor page with the form if the request method is GET,
            or a redirect to the curator dashboard if the form submission is successful.
    """
    if request.method == 'POST':
        form = AddTutorForm(request.POST)
        if form.is_valid():
            return redirect('curator')  # Redirect to the curator dashboard or any other page
    else:
        form = AddTutorForm()
    
    return render(request, 'core/add_tutor.html', {'form': form})
