from django.db import models

# Create your models here.

class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True, verbose_name='Nombre')
    
    def __str__(self):
        return self.nombre

class libro(models.Model):
    id= models.AutoField(primary_key=True)
    titulo = models.CharField(max_length=100)
    imagen =  models.ImageField(upload_to='imagenes/', verbose_name='Imagen', null=True)
    descripcion = models.TextField(verbose_name='Descripcion', null=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='libros', verbose_name='Categoría', null=True)
    
    def __str__(self):
        fila = "Título: " + self.titulo + "-" + "Descripción: " + self.descripcion
        return fila
    
    def delete(self, using= None, keep_parent=False):
        self.imagen.storage.delete(self.imagen.name)
        super().delete()

