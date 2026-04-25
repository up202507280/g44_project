from classes.gclass import Gclass

class Category(Gclass):
    obj = dict()
    lst = list()
    pos = 0
    sortkey = ''
    att = ['_id','_name']
    header = 'Category'
    des = ['Id','Name']
    
    def __init__(self, id, name):
        super().__init__()
        id = Category.get_id(id)
        self._id = id
        self._name = name
        Category.obj[id] = self
        Category.lst.append(id)
        
    @property
    def id(self):
        return self._id
        
    @property
    def name(self):
        return self._name
        
    @name.setter
    def name(self, name):
        self._name = name