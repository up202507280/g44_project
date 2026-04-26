from classes.company import Company
from classes.gclass import Gclass

class Inspection(Gclass):
    obj = dict()
    lst = list()
    pos = 0
    sortkey = ''
    att = ['_id','_info','_company_id']
    header = 'Inspection'
    des = ['Id','Info','Company_id']
    
    def __init__(self, id, info, company_id):
        super().__init__()
        company_id = int(company_id)
        if company_id in Company.lst:
            id = Inspection.get_id(id)
            self._id = id
            self._info = info
            self._company_id = company_id
            
            Inspection.obj[id] = self
            Inspection.lst.append(id)
        else:
            print('Company ', company_id, ' not found')
            
    @property
    def id(self):
        return self._id

    
    @property
    def info(self):
        return self._info
        
    @info.setter
    def info(self, info):
        self._info = info
        
    @property
    def company_id(self):
        return self._company_id
        
    @company_id.setter
    def company_id(self, company_id):
        if company_id in Company.lst:
            self._company_id = company_id
        else:
            print('Company ', company_id, ' not found')   
            
