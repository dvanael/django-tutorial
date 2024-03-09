from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import Group 
from django.contrib.auth import authenticate, login
from django.core.paginator import Paginator

from .utils import *
from .models import Product, Category
from .forms import ProductForm, UserForm
from django.db.models import Q
# Create your views here.

def index(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

@login_required
def product_list(request):
    products = get_admin_objects(request, Product)
    categories = Category.objects.all()

    category =  request.GET.get('category','')
    if category:
        products = products.filter(category__name__icontains=category)

    name = request.GET.get('n', '')    
    if name:
        products = products.filter(Q(name__icontains=name) | Q(description__icontains=name))

    paginator = Paginator(products, 5)

    page_number = request.GET.get('page')
    page_objects = paginator.get_page(page_number)

    context = {
        'page': page_objects,
        'name': name,
        'categories': categories,
        'category': category,
    }
    return render(request, 'products/product-list.html', context)

@login_required
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'products/product-detail.html', {'product': product})

@login_required
def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.instance.user = request.user
            form.save()
            return redirect('product-list')
    else:
        form = ProductForm()
    context = {
        'form': form, 
        'title': 'Cadastrar Produto'
    }
    return render(request, 'form.html', context)

@login_required
def product_update(request, pk):
    product = post_admin_objects(request, Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product-list')
    else:
        form = ProductForm(instance=product)
    context = {
        'form': form, 
        'title': 'Atualizar Produto'
    }
    return render(request, 'form.html', context)

@login_required
def product_delete(request, pk):
    product = post_admin_objects(request, Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        return redirect('product-list')
    context = {
        'object': product, 
        'title': 'Excluir Produto'
    }
    return render(request, 'form-delete.html', context)
    
def register(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save()
            group = get_object_or_404(Group, name='user')
            user.groups.add(group)
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')
    else:
        form = UserForm()
    return render(request, 'registration/register.html', {'form': form})
