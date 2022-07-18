from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required


from django.contrib.auth.models import Group 


@staff_member_required
def user_manual(request):
    if request.user in Group.objects.get(name='Gerente').user_set.all():
        return render(request, 'admin/UMG.html')
    if request.user in Group.objects.get(name='Colaborador').user_set.all():
        return render(request, 'admin/UMC.html')
    #for superuser and admin
    if request.user.is_superuser:
        return render(request, 'admin/AM.html')