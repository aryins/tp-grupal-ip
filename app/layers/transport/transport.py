# capa de transporte/comunicación con otras interfaces o sistemas externos.

import requests
from ...config import config

def getUltimaPag (search):
    
    if search == '-1':
        json_response = requests.get(config.DEFAULT_REST_API_URL + config.DEFAULT_PAGE).json()
        object = json_response['info']
        cantidadPaginas = object['pages']
        
    else:
        json_response = requests.get(config.DEFAULT_REST_API_URL + "1&name=" + search).json()
        object = json_response['info']
        cantidadPaginas = object['pages']
        
    return int(cantidadPaginas)


#Obtenemos una lista con todas las paginas de la API de las cuales queremos obtener informacion
def getApiUrl (search, cant_pages): 
    url = config.DEFAULT_REST_API_URL
    lista_Urls = []
    if search == '-1':
        for page in range (1, 43):
            lista_Urls.append(url + str(page)) 
    else:
        for page in range (1, cant_pages + 1):
            lista_Urls.append(url + str(page) + "&name=" + search)
    return lista_Urls    

# comunicación con la REST API.
# este método se encarga de "pegarle" a la API y traer una lista de objetos JSON crudos (raw).
def getAllImages(input=None):
    json_collection = []
    lista_Urls_Api = []
    
    if input is None:
        lista_Urls_Api = getApiUrl('-1', getUltimaPag ('-1'))
    else:
        lista_Urls_Api = getApiUrl(input, getUltimaPag (input))
    
    for url in lista_Urls_Api:
        json_response = requests.get(url).json()

        # si la búsqueda no arroja resultados, entonces retornamos una lista vacía de elementos.
        if 'error' in json_response:
            print("[transport.py]: la búsqueda no arrojó resultados.")
            return json_collection

        for object in json_response['results']:
            try:
                if 'image' in object:  # verificar si la clave 'image' está presente en el objeto (sin 'image' NO nos sirve, ya que no mostrará las imágenes).
                    json_collection.append(object)
                else:
                    print("[transport.py]: se encontró un objeto sin clave 'image', omitiendo...")

            except KeyError: 
                # puede ocurrir que no todos los objetos tenga la info. completa, en ese caso descartamos dicho objeto y seguimos con el siguiente en la próxima iteración.
                pass

    return json_collection
