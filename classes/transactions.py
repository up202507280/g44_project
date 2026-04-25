"""
@author: António Brito / Carlos Bragança (2025) - Adaptado
#objective: class Transaction
"""
import datetime
from classes.company import Company
from classes.site import Site
from classes.gclass import Gclass

class Transactions(Gclass):
    obj = dict()
    lst = list()
    pos = 0
    sortkey = ''
    att = ['_id', '_date', '_amount', '_company_id', '_site_id']
    header = 'Transactions'
    des = ['Id', 'Date', 'Amount', 'Company_id', 'Site_id']
    
    def __init__(self, id, date, amount, company_id, site_id):
        super().__init__()
        company_id = int(company_id)
        site_id = int(site_id)    
        if company_id in Company.lst:
            if site_id in Site.lst:
                id = Transactions.get_id(id)
                self._id = id
                self._date = datetime.date.fromisoformat(date.replace('/','-'))
                self._amount = float(amount)
                self._company_id = company_id
                self._site_id = site_id
                Transactions.obj[id] = self
                Transactions.lst.append(id)
            else:
                print('Site ', site_id, ' not found')
        else:
            print('Company ', company_id, ' not found')
            
    @property
    def id(self):
        return self._id
        
    @property
    def date(self):
        return self._date
        
    @date.setter
    def date(self, date):
        self._date = date
        
    @property
    def amount(self):
        return self._amount
        
    @amount.setter
    def amount(self, amount):
        self._amount = float(amount)
        
    @property
    def company_id(self):
        return self._company_id
        
    @property
    def site_id(self):
        return self._site_id
        