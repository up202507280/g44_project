import datetime
from classes.gclass import Gclass

class Company(Gclass):
    obj = dict()
    lst = list()
    pos = 0
    sortkey = ''
    att = ['_id','_name', '_created_date']
    header = 'Company'
    des = ['Id','Name', 'Created Date']
    
    def __init__(self, id, name, created_date):
        super().__init__()
        id = Company.get_id(id)
        self._id = id
        self._name = name
        self._created_date = datetime.date.fromisoformat(created_date.replace('/','-'))
        
        Company.obj[id] = self
        Company.lst.append(id)
        
    @property
    def id(self):
        return self._id
        
    @property
    def name(self):
        return self._name
        
    @name.setter
    def name(self, name):
        self._name = name

    @property
    def created_date(self):
        return self._created_date
        
    @created_date.setter
    def created_date(self, created_date):
        self._created_date = created_date
