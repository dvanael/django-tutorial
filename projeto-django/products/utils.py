from django.contrib.auth.decorators import user_passes_test, login_required
from django.shortcuts import get_object_or_404

# Verifica o Grupo do usuário
def group_required(*group_name):
    def in_group(user):
        if user.groups.filter(name__in=group_name).exists():
            return True
        return False
    return user_passes_test(in_group, login_url='/login/')
    
# Filtra todos para Admin, método GET
def get_admin_objects(request, model):
    if request.user.groups.filter(name='admin').exists():
        return model.objects.all()
    else:
        return model.objects.filter(user=request.user)
        
# Permite Admin editar/deletar qualquer objeto, método POST
def post_admin_objects(request, model, pk):
    if request.user.groups.filter(name='admin').exists():
        return get_object_or_404(model, pk=pk)
    else:
        return get_object_or_404(model, pk=pk, user=request.user)
