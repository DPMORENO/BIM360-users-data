from .variables import bim_id, bim_secret, bim_url, bim_urlencode

class sesiones:
    
    def __init__(self, request):
        self.session=request.session
    
# Se redirecciona para conseguir el code de autorización
    def getCode(self):       
        client_id = bim_id     
        callback_url = bim_urlencode
        return f'https://developer.api.autodesk.com/authentication/v1/authorize?response_type=code&client_id={client_id}&redirect_uri={callback_url}&scope=data:read account:read'


# Se guarda dentro de la sesion el token
    def setToken(self, code):
        import requests
        import datetime
        ID = bim_id      
        SECRET = bim_secret
        #modificar una vez se suba a la nube
        URL = bim_url
        url='https://developer.api.autodesk.com/authentication/v1/gettoken'
        header= {'Content-Type':'application/x-www-form-urlencoded'}
        body = {'client_id':ID, 'client_secret':SECRET, 'grant_type': 'authorization_code', 'code':code, 'redirect_uri': URL}
        response = requests.post(url, headers=header, data = body)
        self.session['acces_token'] = response.json().get("access_token")
        self.session['refresh_token'] = response.json().get('refresh_token')
        expdate = datetime.datetime.now() + datetime.timedelta(seconds=response.json().get('expires_in'))
        self.session['expiration'] = expdate.isoformat(timespec='seconds')

#actualiza el token

    def refreshToken(self):
        import requests
        import datetime
        ID = bim_id
        SECRET = bim_secret
        url='https://developer.api.autodesk.com/authentication/v1/refreshtoken'
        header= {'Content-Type':'application/x-www-form-urlencoded'}
        body = {'client_id':ID, 'client_secret':SECRET, 'grant_type': 'refresh_token', 'refresh_token': self.session['refresh_token']}
        response = requests.post(url, headers=header, data=body)
        if response.status_code == 200:
            self.session['acces_token'] = response.json().get("access_token")
            self.session['refresh_token'] = response.json().get('refresh_token')
            expdate = datetime.datetime.now() + datetime.timedelta(seconds=response.json().get('expires_in'))
            self.session['expiration'] = expdate.isoformat(timespec='seconds')
            return True
        else:
            return False


#Se verifica si la persona esta autorizada (falta verificar si esta actualizado)
    def isAuthorised(self):
        import datetime
#Verifica primero si hay un access token dentro de la session, para ver si se ha registrado antes
        if 'acces_token' in self.session:
#Verifica que la sesion no ha caducado y devuelve True si es el caso
            if datetime.datetime.fromisoformat(self.session['expiration']) > datetime.datetime.now():
                return True
#En el caso que la sesion haya caducado, procede a refescar el Token y devuelve True
            else:
                if self.refreshToken():
                    return True
                else:
                    return False
#En el caso que no haya sesion, reenvia a False
        else:
            return False

# devuelve el accestoken (falta verificar si esta actualizado)
    def getToken(self):
        return self.session['acces_token']

    def delsession(self):
        self.session.flush()

