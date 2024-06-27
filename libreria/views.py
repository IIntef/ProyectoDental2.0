from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import libro, Categoria
from .forms import LibroForm, CategoriaForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout


def custom_logout(request):
    if request.method == 'GET':
        logout(request)
        return redirect('login')

def start(request):
    return render(request, 'paginas/start.html')

@login_required
def nosotros(request):
    return render(request, 'paginas/nosotros.html')

@login_required
def libros(request):
    return render(request, 'libros/indes.html')

@login_required
def crear(request):
    formulario= LibroForm(request.POST or None, request.FILES or None)
    if formulario.is_valid():
        formulario.save()
        return redirect('libros')
    return render(request, 'libros/crear.html', {'formulario': formulario})

@login_required
def libros(request):
    libros= libro.objects.all()
    return render(request, 'libros/indes.html', {'libros': libros})

@login_required
def editar(request, id):
    libro_ed = libro.objects.get(id=id)
    formulario = LibroForm(request.POST or None, request.FILES or None, instance=libro_ed) 
    if formulario.is_valid():
        formulario.save()
        return redirect('libros')   
    return render(request, 'libros/editar.html', { 'formulario': formulario})

@login_required
def eliminar (request, id):
    libroe= libro.objects.get(id=id)
    libroe.delete()
    return  redirect('libros')

@login_required
def crear_cat(request):
    formulario_cat= CategoriaForm(request.POST or None, request.FILES or None)
    if formulario_cat.is_valid():
        formulario_cat.save()
        return redirect('categorias')
    return render(request, 'libros_cat/crear_cat.html', {'formulario': formulario_cat})

@login_required
def categorias(request):
    categorias= Categoria.objects.all()
    return render(request, 'libros_cat/indes_cat.html', {'libros_cat': categorias})

@login_required
def editar_cat(request, id):
    libro_ed_cat = Categoria.objects.get(id=id)
    formulario_cat = CategoriaForm(request.POST or None, request.FILES or None, instance=libro_ed_cat) 
    if formulario_cat.is_valid():
        formulario_cat.save()
        return redirect('categorias')   
    return render(request, 'libros_cat/editar_cat.html', { 'formulario': formulario_cat})

@login_required
def eliminar_cat (request, id):
    libroe_cat= Categoria.objects.get(id=id)
    libroe_cat.delete()
    return  redirect('categorias')