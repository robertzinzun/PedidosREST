import requests
import json
datos={"email":"rsuarez@accitesz.com","password":"123"}
url='http://172.16.1.135:5000/alumnos/autenticar'
resp=requests.get(url,json=datos)
o_json=resp.json()
alumno=o_json['alumno']
url='http://172.16.1.135:5000/solicitudes/alumno/'+str(alumno['id'])
resp2=requests.get(url)
#res2=requests.get('http://172.16.1.135:5000/solicitudes/alumno'+alum[)

if __name__=='__main__':
    print(resp.text)
    print(resp2.json())
    o_json=resp2.json()
    solicitudes=o_json['solicitudes']
    for s in solicitudes:
        print(s['proyecto'])