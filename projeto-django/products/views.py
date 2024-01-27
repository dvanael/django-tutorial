from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from .models import Product
from .forms import ProductForm

# Create your views here.
def group_required(*group_name):
    def in_group(user):
        if user.groups.filter(name__in=group_name).exists():
            return True
        return False
    return user_passes_test(in_group, login_url='/login/')

def index(request):
    return render(request, 'index.html')

@group_required('user','admin')
def about(request):
    return render(request, 'about.html')

@group_required('user','admin')
def product_list(request):
    products = Product.objects.filter(user = request.user)
    return render(request, 'products/product-list.html', {'products': products})

@group_required('user','admin')
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'products/product-detail.html', {'product': product})

@group_required('user','admin')
def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.instance.user = request.user
            form.save()
            return redirect('product-list')
    else:
        form = ProductForm()
    context = {'form': form, 'title': 'Cadastrar Produto'}
    return render(request, 'form.html', context)

@group_required('user','admin')
def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product-list')
    else:
        form = ProductForm(instance=product)
    context = {'form': form, 'title': 'Atualizar Produto'}
    return render(request, 'form.html', context)

@group_required('user','admin')
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        return redirect('product-list')
    context = {'object': product, 'title': 'Excluir Produto'}
    return render(request, 'form-delete.html', context)
