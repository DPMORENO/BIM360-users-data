from django.shortcuts import render, redirect
import requests
from .sesiones import sesiones
from .datamanage import getHubs, getUsers
from django.http import JsonResponse


# Lanza la aplicacion del viewer verificando si esta autorizado. SI no lo esta te redirige hacia la pagian de autodesk
def dashboard(request):
    sesion = sesiones(request)
    if sesion.isAuthorised():
        Hubs=getHubs(sesion.getToken())
        return render(request, 'index.html', {'Hubs': Hubs})
    else:
        url = sesion.getCode()
        return redirect(url)

    
#recibe el codigo que envia autodesk para hacer la verificacion de 3 patas.
def oauth(request):
#Coge el codigo que recibe para la primera pata de al verificación, obtiene los tokens y los guarda en la sesion.
    code = request.GET.get('code')
    sesion = sesiones(request)
    sesion.setToken(code)
#Hay que redireccionar a la pagina principal ya con los datos almacenados en la sesion
    return redirect('dashboard')


#Envia el listado de proyectos de un Hub --> ver como hacer para obtener el id del proyecto y usarlo
def Users(request):
    Hubid=request.headers['Content-Id'][1:]
    sesion = sesiones(request)
    Users=getUsers(sesion.getToken(), Hubid)
    return JsonResponse(data={'Users':Users}, safe=False)

