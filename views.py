from django.shortcuts import redirect, render  # type: ignore
from .layers.services import services
from django.contrib.auth.decorators import login_required  # type: ignore
from django.contrib.auth import logout  # type: ignore
from django.contrib import messages  # Para manejar mensajes al usuario

def index_page(request):
    return render(request, 'index.html')

def index(request):
    return render(request, 'index.html')  # Asegúrate de tener una plantilla llamada 'index.html'

# Esta función obtiene 2 listados que corresponden a las imágenes de la API y los favoritos del usuario, y los usa para dibujar el correspondiente template.
# Si el opcional de favoritos no está desarrollado, devuelve un listado vacío.
def home(request):
    images = services.getAllImages()  # Trae una lista con todos los personajes al cargar la galería
    favourite_list = [services.getAllFavourites(request)]  # Corrige la lista para evitar anidación
    return render(request, 'home.html', {'images': images, 'favourite_list': favourite_list})

def search(request):
    search_msg = request.POST.get('query', '')
    if search_msg:  # Términos de búsqueda
        images = services.getAllImages(search_msg)  # Llama a la API con el término de búsqueda
        if images:  # Si hay resultados
            return render(request, 'home.html', {'images': images, 'query': search_msg})
        else:  # No hay resultados
            messages.info(request, "No se encontraron resultados para tu búsqueda.")
            return render(request, 'home.html', {'images': [], 'query': search_msg})
    else:
        messages.warning(request, "Por favor, ingresa un término de búsqueda.")
        return redirect('home')

# Estas funciones se usan cuando el usuario está logueado en la aplicación.
@login_required
def getAllFavouritesByUser(request):
    favourite_list = [] 
    return render(request, 'favourites.html', {'favourite_list': favourite_list})

@login_required
def saveFavourite(request):
    if request.method == 'POST':
        item_id = request.POST.get('item_id')  # Obtener el ID del ítem que el usuario quiere guardar
        if item_id:
            # Aquí suponemos que 'translator.fromRequestIntoCard' puede ser utilizado para obtener una Card
            fav = translator.fromRequestIntoCard(item_id)  # Convertir el item a una Card
            fav.user = request.user  # Asignar el usuario que está guardando el favorito
            return repositories.saveFavourite(fav)  # Guardar el favorito en la base de datos
        else:
            return None  # Si no hay ID, no hacer nada
    return None  # Si no es un POST, tampoco hacer nada

@login_required
def deleteFavourite(request):
    if request.method == 'POST':
        item_id = request.POST.get('item_id')
        if item_id:
            result = services.deleteFavourite(request.user, item_id)
            if result:
                messages.success(request, "El ítem se ha eliminado de tus favoritos.")
            else:
                messages.error(request, "No se pudo eliminar el ítem de tus favoritos.")
        else:
            messages.error(request, "Falta el ID del ítem.")
    return redirect('favoritos')

@login_required
def exit(request):
    logout(request)  # Cierra la sesión del usuario
    messages.success(request, "Has cerrado sesión exitosamente.")  # Mensaje de confirmación
    return redirect('index_page')  # Redirige a la página principal

