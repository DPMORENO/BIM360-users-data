#peticion para obtener todos los Hubs del propietario y los proyctos asociados a ese HUB
def getHubs(token):
        import requests
        url='https://developer.api.autodesk.com/project/v1/hubs'
        auth='Bearer '+ token
        header= {'Authorization': auth}
        hubs=requests.get(url, headers=header).json()['data']
        hubdict=[]
        for hub in hubs:
                type=hub['attributes']['extension']['type']
                if type == 'hubs:autodesk.bim360:Account':
                        name=hub['attributes']['name']
                        id=hub['id']
                        projects=getProjects(token, id)
                        hubdict.append({'name': name, 'id': id, 'type':type, 'content':projects})
        return hubdict


#Peticion para obtener un listado de todos proyectos de un Hub
def getProjects(token, Hubid):
        import requests
        hub_id=Hubid
        url=f'https://developer.api.autodesk.com/project/v1/hubs/{hub_id}/projects'
        auth='Bearer '+ token
        header= {'Authorization': auth}
        projects=requests.get(url, headers=header).json()['data']
        projectdict=[]
        for project in projects:
                name=project['attributes']['name']
                id=project['id']
                projectdict.append({'name': name, 'id': id})
        return projectdict


#Peticion para obtener un listado de todos los usuarios, con info de firstname, lastname, acceslevel, services
def getUsers(token, projectid):
        import requests
        projectId=projectid[1:]
        url=f'https://developer.api.autodesk.com/bim360/admin/v1/projects/{projectId}/users?limit=200&fields=firstName&fields=lastName&fields=accessLevels&fields=services'
        auth='Bearer '+ token
        header= {'Authorization': auth}
        users=requests.get(url, headers=header).json()
        return users

# Hay que modificar el query de la url para que permita mas de 20 consultas y par qeu solo envie los datos que necesitamos