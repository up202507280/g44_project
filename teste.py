
from classes.category import Category
from classes.company import Company
from classes.site import Site
from classes.inspection import Inspection
from classes.transactions import Transactions

Category.read('data/mining.db')
Company.read('data/mining.db')
Site.read('data/mining.db')
Inspection.read('data/mining.db')
Transactions.read('data/mining.db')

if len(Category.lst) == 0:
    cat1 = Category(0, "Bauxita")
    cat2 = Category.from_string("0;Ouro")
    cat3 = Category(0, "Quartzo")
    Category.insert(cat1.id)
    Category.insert(cat2.id)
    Category.insert(cat3.id)

if len(Company.lst) == 0:
    comp1 = Company(0, "Glover, Ryan and Young", "2020/05/12")
    comp2 = Company.from_string("0;Williams LLC;2023/12/10")
    Company.insert(comp1.id)
    Company.insert(comp2.id)

print('Empresas ordenadas por nome:')
Company.sort('name')
for id in Company.lst:
    print(Company.obj[id])
print('-' * 40)

if len(Site.lst) == 0:
    s1 = Site(0, "Terras Raras do Vale Sistemas", cat1.id)
    s2 = Site(0, "Omega Sistemas de Ouro", cat2.id)
    Site.insert(s1.id)
    Site.insert(s2.id)

if len(Inspection.lst) == 0:
    i1 = Inspection(0, "Avaliação de integridade na frota", comp1.id)
    i2 = Inspection(0, "Teste de carga nos taludes", comp2.id)
    Inspection.insert(i1.id)
    Inspection.insert(i2.id)

if len(Transactions.lst) == 0:
    t1 = Transactions(0, "2025/01/10", 4500.50, comp1.id, s1.id)
    t2 = Transactions(0, "2024/05/20", 3200.00, comp2.id, s2.id)
    Transactions.insert(t1.id)
    Transactions.insert(t2.id)

print('Transações Registadas:')
for id in Transactions.lst:
    print(Transactions.obj[id])
