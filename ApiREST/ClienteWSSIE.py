from suds.client import Client


if __name__=='__main__':
    url='http://172.16.1.125:8080/WSSIE/SIEService?wsdl'
    url2='http://localhost:8090/WSSIE/SIEService?WSDL'
    cliente = Client(url2)
    print(cliente)
    docente=cliente.service.consultarDocente(noDocente=10)
    alumno=cliente.factory.create('alumno')
    print(alumno)
    print(docente)
    #print(cliente.service.hello("Roberto"))
    #alumno=cliente.service.consultarAlumno('14010001')
    #print(alumno['nombreCompleto'])
