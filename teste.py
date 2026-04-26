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

if Transactions.lst:
    t = Transactions.obj[Transactions.lst[1]]

    nome_empresa = Company.obj[t.company_id].name
    nome_site = Site.obj[t.site_id].title
    id_cat = Site.obj[t.site_id].category_id
    nome_cat = Category.obj[id_cat].name

    print("Resultados da Associação:")
    print(f"ID Transação: {t.id}")
    print(f"Empresa:      {nome_empresa}")
    print(f"Site:         {nome_site}")
    print(f"Categoria:    {nome_cat}")
    print("\nSUCESSO: Todas as classes estão corretamente mapeadas.")
else:
    print("AVISO: A base de dados está vazia.")
    print(Transactions.obj[id])
