# capa de vista/presentación

from django.shortcuts import redirect, render
from .layers.services import services
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.core.paginator import Paginator

def index_page(request):
    return render(request, 'index.html')

# esta función obtiene 2 listados que corresponden a las imágenes de la API y los favoritos del usuario, y los usa para dibujar el correspondiente template.
# si el opcional de favoritos no está desarrollado, devuelve un listado vacío.
def home(request):
    images = services.getAllImages()
    favourite_list = services.getAllFavourites(request)
    
    images_por_pag = Paginator(images,40)
    page = request.GET.get('page',1)
    images_page = images_por_pag.get_page(int(page))

    return render(request, 'home.html', { 'images': images_page, 'favourite_list': favourite_list })

def search(request):
    search_msg = request.POST.get('query', request.GET.get('query', ''))

    # si el texto ingresado no es vacío, trae las imágenes y favoritos desde services.py,
    # y luego renderiza el template (similar a home).
    images = []
    favourite_list = []

    if (search_msg != ''):
        images = services.getAllImages(search_msg)         
        favourite_list = services.getAllFavourites(request) 
               
        images_por_pag = Paginator(images,20)
        page = request.GET.get('page',1)
        images_page = images_por_pag.get_page(int(page))

        return render(request, 'home.html', { 'images': images_page, 'favourite_list': favourite_list, 'query': search_msg})
    else:
        return redirect('home')


# Estas funciones se usan cuando el usuario está logueado en la aplicación.
@login_required
def getAllFavouritesByUser(request):
    favourite_list = services.getAllFavourites(request)
    return render(request, 'favourites.html', { 'favourite_list': favourite_list })

@login_required
def saveFavourite(request):
   services.saveFavourite(request)
   return redirect('favoritos')
       

@login_required
def deleteFavourite(request):
    services.deleteFavourite(request)
    return redirect('favoritos')


@login_required
def exit(request):
   logout(request)
   return redirect ('home')