import datetime
from flask import render_template, request, session

from classes.company import Company
from classes.site import Site
from classes.category import Category
from classes.transactions import Transactions
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
        
        empresa_id_int = int(obj_empresa.id)
        empresa_id_str = str(obj_empresa.id)
        
        for inspection_id in Inspection.lst:
            insp_obj = Inspection.obj.get(inspection_id)
            
            if insp_obj:
                comp_id_na_insp = getattr(insp_obj, 'company_id', getattr(insp_obj, 'company', getattr(insp_obj, 'id_company', None)))
                if comp_id_na_insp is not None and (int(comp_id_na_insp) == empresa_id_int or str(comp_id_na_insp) == empresa_id_str):
                    desc = getattr(insp_obj, 'info', getattr(insp_obj, 'descricao', getattr(insp_obj, 'description', 'Sem descrição')))
                    lista_inspecoes.append({
                        "id": insp_obj.id,           
                        "descricao": desc   
                    })

        lista_inspecoes = sorted(lista_inspecoes, key=lambda x: x["id"])

        ids_dos_sites = set()
        for transactions_id in Transactions.lst:
            trans_obj = Transactions.obj.get(transactions_id)
            if trans_obj:
                comp_id_na_trans = getattr(trans_obj, 'company_id', getattr(trans_obj, 'company', getattr(trans_obj, 'id_company', None)))
                
                if comp_id_na_trans is not None and (int(comp_id_na_trans) == empresa_id_int or str(comp_id_na_trans) == empresa_id_str):
                    s_id = getattr(trans_obj, 'site_id', getattr(trans_obj, 'site', getattr(trans_obj, 'id_site', None)))
                    
                    
                    if s_id is not None:
                        ids_dos_sites.add(int(s_id))
                    
                    site_obj = Site.obj.get(s_id) if s_id is not None else None
                    
                    t_date_raw = getattr(trans_obj, 'date', getattr(trans_obj, 'data', ''))
                    if isinstance(t_date_raw, datetime.date):
                        t_date = t_date_raw.strftime("%Y-%m-%d")
                    else:
                        t_date = str(t_date_raw).split()[0] if t_date_raw else ""
                    
                    t_amount = getattr(trans_obj, 'amount', getattr(trans_obj, 'valor', 0))
                    if isinstance(t_amount, (float, int)):
                        valor_formatado = f"{t_amount:,.2f} €"
                    else:
                        valor_formatado = f"{t_amount} €"

                    s_title = getattr(site_obj, 'title', getattr(site_obj, 'local', getattr(site_obj, 'nome', f"ID: {s_id}"))) if site_obj else f"ID: {s_id}"

                    lista_transacoes.append({
                        "id": trans_obj.id,
                        "site": s_title,
                        "valor": valor_formatado,
                        "data": t_date
                    })
        lista_transacoes = sorted(lista_transacoes, key=lambda x: x["id"])


        for site_id in ids_dos_sites:
            site_obj = Site.obj.get(site_id)
            if site_obj:
                cat_id = getattr(site_obj, 'category_id', getattr(site_obj, 'category', getattr(site_obj, 'id_category', None)))
                categoria_obj = Category.obj.get(cat_id) if cat_id is not None else None
                
                s_local = getattr(site_obj, 'title', getattr(site_obj, 'local', getattr(site_obj, 'nome', 'Desconhecido')))
                c_name = getattr(categoria_obj, 'name', getattr(categoria_obj, 'title', getattr(categoria_obj, 'nome', 'Não Especificado'))) if categoria_obj else "Não Especificado"

                lista_operacoes.append({
                    "id": site_obj.id,
                    "local": s_local,
                    "mineral": c_name
                })
        lista_operacoes = sorted(lista_operacoes, key=lambda x: x["id"])

    return render_template("index.html", butshow=butshow, butedit=butedit, 
                    id=id, name=name, dob=dob, current_action=current_action,
                    lista_inspecoes=lista_inspecoes, lista_operacoes=lista_operacoes, lista_transacoes=lista_transacoes,
                    ulogin=session.get("user"))
