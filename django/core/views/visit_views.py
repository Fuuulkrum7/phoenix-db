# core/views/visit_views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from app.models import Child, Visits, GroupClass
from core.forms.visit_forms import VisitForm

## \fn add_visit
## \brief View for adding a visit record for children.
## \param request The HTTP request object.
## \param class_id The ID of the group class for which visits are being recorded.
## \return Rendered HTML page for adding visit records.
@login_required
def add_visit(request, class_id):
    group_class = get_object_or_404(GroupClass, pk=class_id)  # Get the group class instance.
    children = Child.objects.filter(current_group=group_class.group)  # Get children in the current group.
    
    if request.method == 'POST':
        formset = [VisitForm(request.POST, prefix=str(child.child_id)) for child in children]
        if all([form.is_valid() for form in formset]):
            for form in formset:
                visit = form.save(commit=False)
                visit.child = Child.objects.get(pk=form.prefix)
                visit.group_class = group_class
                visit.save()
            return redirect('add_visit', class_id=class_id)  # Redirect to the same page or another success page.
    else:
        formset = [VisitForm(prefix=str(child.child_id)) for child in children]

    child_form_list = [{'child': child, 'form': form} for child, form in zip(children, formset)]

    context = {
        'group_class': group_class,
        'child_form_list': child_form_list,
    }
    return render(request, 'core/add_visit.html', context)  # Render the form page.
