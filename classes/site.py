from classes.category import Category
from classes.gclass import Gclass

class Site(Gclass):
    obj = dict()
    lst = list()
    pos = 0
    sortkey = ''
    att = ['_id','_title','_category_id']
    header = 'Site'
    des = ['Id','Title','Category_id']
    
    def __init__(self, id, title, category_id):
        super().__init__()
        category_id = int(category_id)
        if category_id in Category.lst:
            id = Site.get_id(id)
            self._id = id
            self._title = title
            self._category_id = category_id
            
            Site.obj[id] = self
            Site.lst.append(id)
        else:
            print('Category ', category_id, ' not found')
            
    @property
    def id(self):
        return self._id
        
    @property
    def title(self):
        return self._title
        
    @title.setter
    def title(self, title):
        self._title = title
        
    @property
    def category_id(self):
        return self._category_id
        
    @category_id.setter
    def category_id(self, category_id):
        if category_id in Category.lst:
            self._category_id = category_id
        else:
            print('Category ', category_id, ' not found')