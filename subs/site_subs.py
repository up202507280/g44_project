import datetime
from flask import render_template, session, redirect, request, url_for
from classes.company import Company
from classes.site import Site
from classes.transactions import Transactions
from classes.category import Category

def listar_sites():
    ulogin = session.get("user")
    if not ulogin: 
        return redirect(url_for("login"))

    current_company_id = session.get("company_current_id")
    if not current_company_id:
        return "Nenhuma empresa selecionada.", 400

    empresa_obj = Company.obj[int(current_company_id)]
    msg_erro = ""

    action = request.args.get("action")
    site_id_param = request.args.get("site_id") or request.args.get("id")
    modo_edicao = False
    site_editando = None

    if action == "delete" and site_id_param:
        try:
            target_id = int(site_id_param)
            trans_para_remover = []
            for tid in list(Transactions.lst):
                trans_obj = Transactions.obj.get(tid)
                if trans_obj:
                    s_id = getattr(trans_obj, '_site', getattr(trans_obj, 'site_id', getattr(trans_obj, 'site', None)))
                    if s_id and not isinstance(s_id, (int, float, str)):
                        s_id = getattr(s_id, 'id', None)
                    if s_id is not None and int(s_id) == target_id:
                        trans_para_remover.append(tid)
            for tid in trans_para_remover:
                Transactions.remove(tid)
            if target_id in Site.obj:
                Site.remove(target_id)
            return redirect(url_for("sub_site"))
        except Exception as e:
            msg_erro = f"Erro: {str(e)}"
            
    elif action == "edit" and site_id_param:
        target_id = int(site_id_param)
        if target_id in Site.obj:
            modo_edicao = True
            site_obj = Site.obj[target_id]
            cat_id = getattr(site_obj, '_category', getattr(site_obj, 'category_id', getattr(site_obj, 'category', 0)))
            if cat_id and not isinstance(cat_id, (int, float, str)):
                cat_id = getattr(cat_id, 'id', 0)
            nome_mineral = getattr(Category.obj[int(cat_id)], 'name', '') if int(cat_id) in Category.obj else ""
            site_editando = {
                "id": site_obj.id,
                "local": getattr(site_obj, 'title', getattr(site_obj, 'local', '')),
                "mineral": nome_mineral
            }

    if request.method == "POST":
        action_type = request.form.get("action_type", "insert")
        localizacao = request.form.get("localizacao", request.form.get("local", "")).strip()
        mineral_nome = request.form.get("mineral", "").strip()
        id_a_editar = request.form.get("site_id") or request.form.get("id")

        if localizacao and mineral_nome:
            try:
                category_id = None
                for c_id in list(Category.lst):
                    if Category.obj[c_id].name.lower() == mineral_nome.lower():
                        category_id = c_id
                        break
                if category_id is None:
                    category_id = Category.get_id(0)
                    nova_cat = Category(id=category_id, name=mineral_nome)
                    Category.insert(nova_cat.id)

                if action_type == "insert":
                    novo_id_site = Site.get_id(0)
                    obj_site = Site(id=novo_id_site, title=localizacao, category_id=int(category_id))
                    Site.insert(obj_site.id)
                    novo_id_trans = Transactions.get_id(0)
                    data_hoje = datetime.date.today().strftime("%Y-%m-%d")
                    obj_trans = Transactions(id=novo_id_trans, date=data_hoje, amount=0.0, company_id=int(current_company_id), site_id=int(novo_id_site))
                    Transactions.insert(obj_trans.id)
                elif action_type == "edit" and id_a_editar:
                    if int(id_a_editar) in Site.obj:
                        obj_site = Site.obj[int(id_a_editar)]
                        obj_site.title = localizacao
                        obj_site.category_id = int(category_id)
                        Site.update(obj_site.id)
                return redirect(url_for("sub_site"))
            except Exception as e:
                msg_erro = f"Erro: {str(e)}"

    ids_dos_sites = set()
    for transactions_id in list(Transactions.lst):
        trans_obj = Transactions.obj.get(transactions_id)
        if trans_obj:
            comp_id = getattr(trans_obj, '_company', getattr(trans_obj, 'company_id', getattr(trans_obj, 'company', None)))
            if comp_id and not isinstance(comp_id, (int, float, str)):
                comp_id = getattr(comp_id, 'id', None)
            
            
            if comp_id is not None and int(str(comp_id).replace("<", "").replace(">", "").split()[-1].strip("]")) == int(current_company_id):
                s_id = getattr(trans_obj, '_site', getattr(trans_obj, 'site_id', getattr(trans_obj, 'site', None)))
                if s_id is not None:
                    if not isinstance(s_id, (int, float, str)):
                        s_id = getattr(s_id, 'id', None)
                    if s_id is not None:
                        ids_dos_sites.add(int(s_id))

    lista_operacoes = []
    for site_id in ids_dos_sites:
        site_obj = Site.obj.get(site_id)
        if site_obj:
            cat_id = getattr(site_obj, '_category', getattr(site_obj, 'category_id', getattr(site_obj, 'category', None)))
            if cat_id and not isinstance(cat_id, (int, float, str)):
                cat_id = getattr(cat_id, 'id', None)
            categoria_obj = Category.obj.get(cat_id) if cat_id is not None else None
            lista_operacoes.append({
                "id": site_obj.id, 
                "local": getattr(site_obj, 'title', getattr(site_obj, 'local', 'Desconhecido')), 
                "mineral": getattr(categoria_obj, 'name', 'Não Especificado') if categoria_obj else "Não Especificado"
            })
                
    lista_operacoes = sorted(lista_operacoes, key=lambda x: x["id"])
    lista_categorias = [{"id": c_id, "name": Category.obj[c_id].name} for c_id in list(Category.lst) if c_id in Category.obj]

    return render_template(
        "site.html", 
        empresa=empresa_obj,
        name=getattr(empresa_obj, 'name', ''),
        lista_operacoes=lista_operacoes,
        lista_categorias=lista_categorias, 
        ulogin=ulogin,
        modo_edicao=modo_edicao,
        site_editando=site_editando,
        msg_erro=msg_erro
    )