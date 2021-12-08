from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse

from authapp.models import ShopUser
from authapp.forms import ShopUserRegisterForm
from mainapp.models import ProductCategory, Product
from mainapp.views import get_basket
from adminapp.forms import ShopUserAdminEditForm, ProductCategoryForm, ProductForm


@user_passes_test(lambda u: u.is_superuser)
def users(request):
    context = {
        'object_list': ShopUser.objects.all().order_by('-is_active')
    }
    return render(request, 'adminapp/users_list.html', context)


@user_passes_test(lambda u: u.is_superuser)
def user_create(request):
    if request.method == 'POST':
        user_form = ShopUserRegisterForm(request.POST, request.FILES)
        if user_form.is_valid():
            user_form.save()
            return HttpResponseRedirect(reverse('adminapp:users'))
    else:
        user_form = ShopUserRegisterForm()
    context = {
        'form': user_form
    }
    return render(request, 'adminapp/user_form.html', context)


@user_passes_test(lambda u: u.is_superuser)
def user_update(request, pk):
    current_user = get_object_or_404(ShopUser, pk=pk)
    if request.method == 'POST':
        user_form = ShopUserAdminEditForm(request.POST, request.FILES, instance=current_user)
        if user_form.is_valid():
            user_form.save()
            return HttpResponseRedirect(reverse('adminapp:users'))
    else:
        user_form = ShopUserAdminEditForm(instance=current_user)
    context = {
        'form': user_form
    }
    return render(request, 'adminapp/user_form.html', context)


@user_passes_test(lambda u: u.is_superuser)
def user_delete(request, pk):
    current_user = get_object_or_404(ShopUser, pk=pk)

    if request.method == 'POST':
        current_user.is_active = False
        current_user.save()
        return HttpResponseRedirect(reverse('adminapp:users'))

    context = {
        'object': current_user
    }
    return render(request, 'adminapp/user_delete.html', context)


@user_passes_test(lambda u: u.is_superuser)
def categories(request):
    context = {
        'object_list': ProductCategory.objects.all()
    }

    return render(request, 'adminapp/categories_list.html', context)


@user_passes_test(lambda u: u.is_superuser)
def category_create(request):
    if request.method == 'POST':
        form = ProductCategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('adminapp:categories'))
    else:
        form = ProductCategoryForm()
    context = {
        'form': form
    }
    return render(request, 'adminapp/category_form.html', context)


@user_passes_test(lambda u: u.is_superuser)
def category_update(request, pk):
    category_item = get_object_or_404(ProductCategory, pk=pk)
    if request.method == 'POST':
        form = ProductCategoryForm(request.POST, instance=category_item)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('adminapp:categories'))
    else:
        form = ProductCategoryForm(instance=category_item)
    context = {
        'form': form
    }
    return render(request, 'adminapp/category_form.html', context)


@user_passes_test(lambda u: u.is_superuser)
def category_delete(request, pk):
    category_item = get_object_or_404(ProductCategory, pk=pk)

    if request.method == 'POST':
        category_item.is_active = False
        category_item.save()
        return HttpResponseRedirect(reverse('adminapp:categories'))

    context = {
        'object': category_item
    }
    return render(request, 'adminapp/category_delete.html', context)


@user_passes_test(lambda u: u.is_superuser)
def products(request, pk):
    context = {
        'object_list': Product.objects.filter(category__pk=pk)
    }

    return render(request, 'adminapp/products_list.html', context)


@user_passes_test(lambda u: u.is_superuser)
def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('adminapp:categories'))
    else:
        form = ProductForm()
    context = {
        'form': form
    }
    return render(request, 'adminapp/product_form.html', context)


@user_passes_test(lambda u: u.is_superuser)
def product_update(request, pk):
    item = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('adminapp:categories'))
    else:
        form = ProductForm(instance=item)
    context = {
        'form': form
    }
    return render(request, 'adminapp/product_form.html', context)


@user_passes_test(lambda u: u.is_superuser)
def product_delete(request, pk):
    item = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        item.is_active = False
        item.save()
        return HttpResponseRedirect(reverse('adminapp:categories'))

    context = {
        'object': item
    }
    return render(request, 'adminapp/product_delete.html', context)


@user_passes_test(lambda u: u.is_superuser)
def product_read(request, pk):
    links_menu = ProductCategory.objects.all()
    context = {
        'links_menu': links_menu,
        'product': get_object_or_404(Product, pk=pk),
        'basket': get_basket(request.user)
    }
    return render(request, 'mainapp/product.html', context)
