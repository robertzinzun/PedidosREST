from sqlalchemy import Column,INTEGER,String
from sqlalchemy import create_engine
from sqlalchemy import MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound
from spyne.model.primitive import Unicode
from spyne.model.complex import ComplexModelBase
from spyne.model.complex import ComplexModelMeta
from sqlalchemy import create_engine,INTEGER,String,Column
db = create_engine('mysql+pymysql://titulatec_soa:Hola.123@localhost:3306/TitulaTEC_SOA')
Session = sessionmaker(bind=db)

class TableModel(ComplexModelBase):
    __metaclass__ = ComplexModelMeta
    __metadata__ = MetaData(bind=db)

class Opcion(TableModel):
    __namespace__ = 'itesz.soa.Opcion'
    __table__='Opciones'
   
    idOpcion = UnsignedInteger32(pk=True)
    nombre= Unicode(32, pattern='\w+( \w+)+')
    descripcion = Unicode(64)
    estatus=Unidcode(32)
    def getOpcion(self,id):
        return self.query.get(id)
    