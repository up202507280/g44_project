import datetime
from flask import render_template, request, session

from classes.company import Company
from classes.site import Site
from classes.transactions import Transactions
from classes.category import Category
from classes.inspection import Inspection

prev_option = ""

def index(path):
    global prev_option
    butshow, butedit = "disabled","enabled"
    option = request.args.get("option")
    prev_option = request.form.get("prev_option", "") 

    if option == "edit":
        butshow, butedit ="enabled","disabled"
        
    elif option == "delete":
        obj = Company.current()
        if obj:
            Company.remove(obj.id)
            if not Company.previous():
                Company.first()
                
    elif option == "insert":
        butshow, butedit = "enabled","disabled"
        
    elif option == 'cancel':
        pass
        
    elif option == 'save':
        if prev_option == 'insert':
            strobj = str(Company.get_id(0))
            strobj = strobj + ';' + request.form["name"] + ';' + request.form["dob"] 
            obj = Company.from_string(strobj)
            Company.insert(obj.id)
            Company.last()
        elif prev_option == 'edit':
            obj = Company.current()
            if obj:
                obj.name = request.form["name"]
                obj.created_date = request.form["dob"]
                Company.update(obj.id)
            
    elif option == "first":
        Company.first()
    elif option == "previous":
        Company.previous()
    elif option == "next":
        Company.nextrec()
    elif option == "last":
        Company.last()
    elif option == 'exit':
        return "<h1>Obrigado por usar o sistema de mineração!</h1>"
        
    obj_empresa = Company.current()
    if option == 'insert' or len(Company.lst) == 0:
        id = Company.get_id(0)
        name = dob = ""
        current_action = 'insert' 
    else:
        id = obj_empresa.id
        name = obj_empresa.name
        if isinstance(obj_empresa.created_date, datetime.date):
            dob = obj_empresa.created_date.strftime("%Y-%m-%d")
        else:
            dob = str(obj_empresa.created_date).split()[0] if obj_empresa.created_date else ""
            
        current_action = option if option in ['edit', 'insert'] else ''

    
    lista_inspecoes = []
    lista_operacoes = []
    lista_transacoes = []

    if obj_empresa and option != 'insert' and len(Company.lst) > 0:
        
        for inspection_id in Inspection.lst:
            insp_obj = Inspection.obj.get(inspection_id)
            
            if insp_obj and insp_obj.company_id == obj_empresa.id:
                
                lista_inspecoes.append({
                    "id": insp_obj.id,           
                    "descricao": insp_obj.info   
                })

        lista_inspecoes = sorted(lista_inspecoes, key=lambda x: x["id"])

      
        sites_da_empresa = set()
        for transactions_id in Transactions.lst:
            trans = Transactions.obj.get(transactions_id)
            if trans and trans.company_id == obj_empresa.id:
                sites_da_empresa.add(trans.site_id)

        for site_id in sites_da_empresa:
            site_obj = Site.obj.get(site_id)
            if site_obj:
                categoria_obj = Category.obj.get(site_obj.category_id)
                lista_operacoes.append({
                    "id": site_obj.id,
                    "local": site_obj.title,
                    "mineral": categoria_obj.name if categoria_obj else "Não Especificado"
                })

        lista_operacoes = sorted(lista_operacoes, key=lambda x: x["id"])


        for transactions_id in Transactions.lst:
            trans_obj = Transactions.obj.get(transactions_id)
            if trans_obj and trans_obj.company_id == obj_empresa.id:
                site_obj = Site.obj.get(trans_obj.site_id)
                
                if isinstance(trans_obj.date, datetime.date):
                    t_date = trans_obj.date.strftime("%Y-%m-%d")
                else:
                    t_date = str(trans_obj.date).split()[0] if trans_obj.date else ""
                
                
                if isinstance(trans_obj.amount, (float, int)):
                    valor_formatado = f"{trans_obj.amount:,.2f} €"
                else:
                    valor_formatado = f"{trans_obj.amount} €"

                lista_transacoes.append({
                    "id": trans_obj.id,
                    "site": site_obj.title if site_obj else f"ID: {trans_obj.site_id}",
                    "valor": valor_formatado,
                    "data": t_date
                })

        lista_transacoes = sorted(lista_transacoes, key=lambda x: x["id"])

    return render_template("index.html", butshow=butshow, butedit=butedit, 
                    id=id, name=name, dob=dob, current_action=current_action,
                    lista_inspecoes=lista_inspecoes, lista_operacoes=lista_operacoes, lista_transacoes=lista_transacoes,
                    ulogin=session.get("user"))    
