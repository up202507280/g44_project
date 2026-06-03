from flask import render_template, session, redirect, request
from classes.company import Company
from classes.inspection import Inspection

cid=request.args.get("cid")

def listar_inspecoes(empresa_id):
    if not session.get("user"):
        return redirect("/login")
    
    # Sincroniza a empresa ativa usando a arquitetura do projeto
    try:
        Company.current(cid)
    except:
        pass
       
    empresa_obj = Company.current(cid)
    #if not empresa_obj:
    #    empresa_obj = Company.obj.get(empresa_id)
        
    if not empresa_obj:
        return redirect("/")

    lista_inspecoes = []
    try:
        for inspection_id in Inspection.lst:
            insp_obj = Inspection.obj.get(inspection_id)
            if insp_obj:
                comp_id = getattr(insp_obj, '_company', getattr(insp_obj, 'company', None))
                if comp_id and not isinstance(comp_id, (int, float, str)):
                    comp_id = getattr(comp_id, 'id', getattr(comp_id, '_id', None))
                
                if comp_id is not None and int(str(comp_id).replace("<", "").replace(">", "").split()[-1].strip("]")) == empresa_id:
                    desc = getattr(insp_obj, 'info', getattr(insp_obj, 'descricao', getattr(insp_obj, 'description', 'Sem descrição')))
                    lista_inspecoes.append({"id": insp_obj.id, "descricao": desc})
    except Exception as e:
        print(f"Erro ao filtrar Inspection: {e}")

    return render_template("inspection.html", 
                           empresa=empresa_obj, 
                           lista=lista_inspecoes, 
                           id=empresa_id, 
                           name=getattr(empresa_obj, 'name', ''),
                           current_action='view',
                           ulogin=session.get("user"))

