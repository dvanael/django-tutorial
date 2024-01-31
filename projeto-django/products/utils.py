from django.contrib.auth.decorators import user_passes_test, login_required
from django.shortcuts import get_object_or_404

# Verifica o Grupo do usuário
def group_required(*group_name):
    def in_group(user):
        if user.groups.filter(name__in=group_name).exists():
            return True
        return False
    return user_passes_test(in_group, login_url='/login/')
    
# Se Admin get
def get_admin(request, model):
    if request.user.groups.filter(name='admin').exists():
        return model.objects.all()
    else:
        return model.objects.filter(user=request.user)
        
# Se Admin post
def post_admin(request, model, pk):
    if request.user.groups.filter(name='admin').exists():
        return get_object_or_404(model, pk=pk)
    else:
        return get_object_or_404(model, pk=pk, user=request.user)
