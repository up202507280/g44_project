from flask import render_template, session, redirect, request, url_for
from classes.company import Company
from classes.inspection import Inspection

def listar_inspecoes():
    ulogin = session.get("user")
    if not ulogin: 
        return redirect(url_for("login"))
        
    current_company_id = session.get("company_current_id")
    if not current_company_id:
        return "Nenhuma empresa selecionada.", 400

    empresa_obj = Company.obj[int(current_company_id)]
    msg_erro = ""

    action = request.args.get("action")
    insp_id_param = request.args.get("insp_id") or request.args.get("id")
    modo_edicao = False
    inspecao_editando = None

    if action == "delete" and insp_id_param:
        try:
            Inspection.remove(int(insp_id_param))
            return redirect(url_for("sub_inspection"))
        except Exception as e:
            msg_erro = f"Erro: {str(e)}"
            
    elif action == "edit" and insp_id_param:
        target_id = int(insp_id_param)
        if target_id in Inspection.obj:
            modo_edicao = True
            insp_obj = Inspection.obj[target_id]
            inspecao_editando = {
                "id": insp_obj.id,
                "descricao": getattr(insp_obj, 'info', getattr(insp_obj, 'descricao', ''))
            }

    if request.method == "POST":
        action_type = request.form.get("action_type", "insert")
        descricao_nota = request.form.get("descricao", "").strip()
        id_a_editar = request.form.get("insp_id") or request.form.get("id")

        if descricao_nota:
            try:
                if action_type == "insert":
                    novo_id = Inspection.get_id(0)
                    string_objeto = f"{novo_id};{descricao_nota};{current_company_id}"
                    obj_inspecao = Inspection.from_string(string_objeto)
                    Inspection.insert(obj_inspecao.id)
                elif action_type == "edit" and id_a_editar:
                    if int(id_a_editar) in Inspection.obj:
                        obj_inspecao = Inspection.obj[int(id_a_editar)]
                        obj_inspecao.info = descricao_nota
                        Inspection.update(obj_inspecao.id)
                return redirect(url_for("sub_inspection"))
            except Exception as e:
                msg_erro = f"Erro: {str(e)}"

    lista_inspecoes = []
    for inspection_id in list(Inspection.lst):
        insp_obj = Inspection.obj.get(inspection_id)
        if insp_obj:
            comp_id = getattr(insp_obj, '_company', getattr(insp_obj, 'company_id', getattr(insp_obj, 'company', None)))
            if comp_id and not isinstance(comp_id, (int, float, str)):
                comp_id = getattr(comp_id, 'id', None)
            
            # CORREÇÃO CRÍTICA: Compara diretamente com o ID da SESSÃO
            if comp_id is not None and int(str(comp_id).replace("<", "").replace(">", "").split()[-1].strip("]")) == int(current_company_id):
                lista_inspecoes.append({
                    "id": insp_obj.id,
                    "descricao": getattr(insp_obj, 'info', getattr(insp_obj, 'descricao', 'Sem descrição'))
                })
                
    lista_inspecoes = sorted(lista_inspecoes, key=lambda x: x["id"])

    return render_template(
        "inspection.html", 
        empresa=empresa_obj,
        name=getattr(empresa_obj, 'name', ''),
        lista_inspecoes=lista_inspecoes, 
        ulogin=ulogin,
        modo_edicao=modo_edicao,
        inspecao_editando=inspecao_editando,
        msg_erro=msg_erro
    )