from django.shortcuts import render

# Create your views here.
def nosotros(request):
    return render(request, 'paginas/nosotros.html')

def libros(request):
    return render(request, 'libros/indes.html')

def start(request):
    return render(request, 'paginas/start.html')

def crear(request):
    return render(request, 'libros/crear.html')

def editar(request):
    return render(request, 'libros/editar.html')