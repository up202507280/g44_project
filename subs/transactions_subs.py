import datetime
from flask import render_template, session, redirect, request, url_for
from classes.company import Company
from classes.site import Site
from classes.transactions import Transactions

def listar_transacoes():
    ulogin = session.get("user")
    if not ulogin: 
        return redirect(url_for("login"))

  
    current_company_id = session.get("company_current_id")
    if not current_company_id:
        return "Nenhuma empresa selecionada.", 400

    empresa_obj = Company.obj[int(current_company_id)]
    modo_edicao = None
    msg_erro = ""

    action = request.args.get("action")
    trans_id_param = request.args.get("trans_id") or request.args.get("id")

    if action == "delete" and trans_id_param:
        try:
            Transactions.remove(int(trans_id_param))
            return redirect(url_for("sub_transactions"))
        except Exception as e:
            msg_erro = f"Erro ao apagar transação: {str(e)}"
            
    elif action == "edit" and trans_id_param:
        t_id = int(trans_id_param)
        if t_id in Transactions.obj:
            modo_edicao = Transactions.obj[t_id]

    if request.method == "POST":
        data_trans = request.form.get("data", "").strip()
        valor_trans = request.form.get("valor", "").strip()
        site_id_trans = request.form.get("site_id", "").strip()
        trans_id = request.form.get("trans_id", "0").strip()
        action_type = request.form.get("action_type", "insert").strip()

        if data_trans and valor_trans and site_id_trans:
            try:
                if action_type == "edit" or (trans_id != "0" and int(trans_id) in Transactions.obj): 
                    obj_transacao = Transactions.obj[int(trans_id)]
                    obj_transacao.date = datetime.date.fromisoformat(data_trans.replace('/', '-'))
                    obj_transacao.amount = float(valor_trans)
                    if hasattr(obj_transacao, 'site_id'):
                        obj_transacao.site_id = int(site_id_trans)
                    else:
                        obj_transacao.site = int(site_id_trans)
                    Transactions.update(obj_transacao.id)
                else: 
                    novo_id = Transactions.get_id(0)
                    valor_float = float(valor_trans)
                    string_objeto = f"{novo_id};{data_trans};{valor_float};{current_company_id};{site_id_trans}"
                    obj_transacao = Transactions.from_string(string_objeto)
                    Transactions.insert(obj_transacao.id)
                return redirect(url_for("sub_transactions"))
            except Exception as e:
                msg_erro = f"Erro crítico: {str(e)}"

    lista_render = []
    for transactions_id in list(Transactions.lst):
        trans_obj = Transactions.obj.get(transactions_id)
        if trans_obj:
            comp_id = getattr(trans_obj, '_company', getattr(trans_obj, 'company_id', getattr(trans_obj, 'company', None)))
            if comp_id and not isinstance(comp_id, (int, float, str)):
                comp_id = getattr(comp_id, 'id', None)
                
            
            if comp_id is not None and int(str(comp_id).replace("<", "").replace(">", "").split()[-1].strip("]")) == int(current_company_id):
                s_id = getattr(trans_obj, '_site', getattr(trans_obj, 'site_id', getattr(trans_obj, 'site', None)))
                site_obj = Site.obj.get(s_id) if (s_id is not None and isinstance(s_id, (int, float))) else None
                
                t_date = str(getattr(trans_obj, 'date', getattr(trans_obj, 'data', ''))).split()[0]
                t_amount = getattr(trans_obj, 'amount', getattr(trans_obj, 'valor', 0))
                s_title = getattr(site_obj, 'title', getattr(site_obj, 'local', 'Operação')) if site_obj else "Operação"

                lista_render.append({
                    "id": trans_obj.id,
                    "site": s_title,
                    "valor": f"{t_amount:,.2f} €" if isinstance(t_amount, (int, float)) else f"{t_amount} €",
                    "data": t_date
                })
                
    lista_render = sorted(lista_render, key=lambda x: x["id"])
    lista_sites = [{"id": s_id, "title": getattr(Site.obj[s_id], 'title', getattr(Site.obj[s_id], 'local', ''))} for s_id in list(Site.lst) if s_id in Site.obj]

    edit_trans_mapeado = None
    if modo_edicao:
        s_id_edit = getattr(modo_edicao, '_site', getattr(modo_edicao, 'site_id', getattr(modo_edicao, 'site', 0)))
        if s_id_edit and not isinstance(s_id_edit, (int, float, str)):
            s_id_edit = getattr(s_id_edit, 'id', 0)
        edit_trans_mapeado = {
            "id": modo_edicao.id,
            "date": str(getattr(modo_edicao, 'date', getattr(modo_edicao, 'data', ''))).split()[0],
            "amount": getattr(modo_edicao, 'amount', getattr(modo_edicao, 'valor', 0)),
            "site_id": int(s_id_edit)
        }

    return render_template(
        "transactions.html", 
        empresa=empresa_obj,
        name=getattr(empresa_obj, 'name', ''),
        lista_transacoes=lista_render, 
        lista_sites=lista_sites, 
        modo_edicao=modo_edicao, 
        edit_trans=edit_trans_mapeado,
        ulogin=ulogin,
        msg_erro=msg_erro
    )