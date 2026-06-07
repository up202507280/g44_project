import datetime
from flask import Flask, render_template, request, session, redirect, url_for
from classes.company import Company
from classes.category import Category
from classes.site import Site
from classes.transactions import Transactions
from classes.inspection import Inspection
from classes.userlogin import Userlogin
from datefile import filename
from subs.apps_plot import apps_plot 
from subs.apps_plotly import apps_plotly
from subs import inspection_subs
from subs import site_subs
from subs import transactions_subs

app = Flask(__name__)
app.secret_key = 'BAD_SECRET_KEY'

Company.read(filename + 'mining.db')
Category.read(filename + 'mining.db')
Site.read(filename + 'mining.db')
Transactions.read(filename + 'mining.db')
Inspection.read(filename + 'mining.db')
Userlogin.read(filename + 'business.db')

@app.route("/", methods=["POST", "GET"])
def index():
    ulogin = session.get("user")
    if not ulogin:
        return render_template("index.html", ulogin=None)
   
    user_clean = str(ulogin).strip().lower()
    
    if user_clean in ["admin", "administrator", "root", "user1"]:
        group = "admin"
        is_company_locked = False
    else:
        group = "user"
        is_company_locked = True

    option = request.args.get("option") or request.form.get("option", "")
    prev_option = request.form.get("prev_option", "")

    if group != "admin" and (option in ["delete", "insert"] or prev_option == "insert"):
        return "Acesso Negado.", 403
    
    if group != "admin":
        if "empresa_" in user_clean:
            try:
                current_id = int(user_clean.split("empresa_")[1])
            except Exception:
                current_id = Company.lst[0] if len(Company.lst) > 0 else None
        else:
            current_id = Company.lst[0] if len(Company.lst) > 0 else None
        session["company_current_id"] = current_id
    else:
        current_id = session.get("company_current_id")
        if (not current_id or current_id not in Company.obj) and option != "insert" and prev_option != "insert":
            current_id = Company.lst[0] if len(Company.lst) > 0 else None
            session["company_current_id"] = current_id

    if current_id and current_id in Company.obj and option != "insert":
        Company.current(current_id)

    butshow, butedit = "disabled", "enabled"
    msg = ""

    if option == "edit":
        butshow, butedit = "enabled", "disabled"
        current_action = "edit"
    elif option == "insert" and group == "admin":
        butshow, butedit = "enabled", "disabled"
        current_action = "insert"
        id_view = 0
        name = ""
        dob = ""
        return render_template("company.html", butshow=butshow, butedit=butedit, id=id_view,
                               name=name, dob=dob, current_action=current_action, 
                               ulogin=ulogin, msg=msg, is_company_locked=is_company_locked)
        
    elif request.method == "POST" and prev_option == 'edit':
        if current_id and current_id in Company.obj:
            obj = Company.obj[current_id]
            obj.name = request.form["name"]
            date_str = request.form["dob"].replace('/', '-')
            obj.created_date = datetime.date.fromisoformat(date_str)
            Company.update(obj.id)
            msg = "Alterações guardadas com sucesso!"
        current_action = "edit"

   
    elif request.method == "POST" and prev_option == 'insert' and group == "admin":
        try:
            name_input = request.form["name"]
            date_str = request.form["dob"].replace('/', '-')
            created_date = datetime.date.fromisoformat(date_str)
            
           
            obj = Company(0, name_input, created_date)
            Company.insert(obj.id)
            
            current_id = obj.id
            session["company_current_id"] = current_id
            Company.current(current_id)
            
            msg = "Nova empresa inserida com sucesso!"
            butshow, butedit = "disabled", "enabled"
        except Exception:
            msg = "Erro ao inserir a nova empresa. Verifica os dados introduzidos."
            butshow, butedit = "enabled", "disabled"
        current_action = "edit"
    else:
        current_action = "edit"

    if is_company_locked:
        option = "" 

    if option in ["first", "previous", "next", "last"] and not is_company_locked:
        if len(Company.lst) > 0:
            try: curr_idx = Company.lst.index(current_id)
            except ValueError: curr_idx = 0
            if option == "first": curr_idx = 0
            elif option == "previous" and curr_idx > 0: curr_idx -= 1
            elif option == "next" and curr_idx < len(Company.lst) - 1: curr_idx += 1
            elif option == "last": curr_idx = len(Company.lst) - 1
            current_id = Company.lst[curr_idx]
            session["company_current_id"] = current_id
            Company.current(current_id)

    elif option == 'exit':
        session.clear()
        return redirect(url_for("login"))

   
    if current_id in Company.obj:
        obj_empresa = Company.obj[current_id]
        id_view = obj_empresa.id
        name = obj_empresa.name
        dob = obj_empresa.created_date.strftime("%Y-%m-%d") if isinstance(obj_empresa.created_date, datetime.date) else str(obj_empresa.created_date).split()[0]
    else:
        id_view, name, dob = 0, "", ""

    return render_template("company.html", butshow=butshow, butedit=butedit, id=id_view,
                           name=name, dob=dob, current_action=current_action, 
                           ulogin=ulogin, msg=msg, is_company_locked=is_company_locked)


@app.route("/Userlogin", methods=["POST", "GET"])
def userlogin():
    ulogin = session.get("user")
    if not ulogin: 
        return redirect(url_for("login"))
   
    user_id = Userlogin.get_user_id(ulogin)
    
    user_clean = str(ulogin).strip().lower()
    if user_clean in ["admin", "administrator", "root", "user1"]:
        group = "admin"
    else:
        group = Userlogin.obj[user_id].usergroup if user_id in Userlogin.obj else "user"

    msg = ""
    butshow, butedit = "enabled", "disabled"
    
    option = request.args.get("option") if request.method == "GET" else request.form.get("option")
    if not option:
        option = request.args.get("option")
        
    prev_option = session.get("user_prev_option", "")

    if group != "admin":
        if option in ["delete", "insert"] or (prev_option == "insert" and option == "save"):
            return "Acesso Negado: Não tem permissões de Administrador.", 403

    if group == "admin":
        current_view_id = session.get("user_view_id")
        if (current_view_id not in Userlogin.lst) and len(Userlogin.lst) > 0:
            current_view_id = Userlogin.lst[0]
    else:
        current_view_id = user_id

    if option == "edit":
        butshow, butedit = "disabled", "enabled"
    elif option == "cancel":
        butshow, butedit = "enabled", "disabled"
    elif option == "delete" and group == "admin":
        if current_view_id and current_view_id != user_id:
            Userlogin.remove(current_view_id)
            current_view_id = Userlogin.lst[0] if len(Userlogin.lst) > 0 else None
        else:
            msg = 'Não pode eliminar o utilizador ligado atualmente.'
    elif option == "insert" and group == "admin":
        butshow, butedit = "disabled", "enabled"
        

    elif option == 'save':
        if request.method == "POST" and prev_option == 'insert' and group == "admin":
            user_input = request.form["user"]
            if len(Userlogin.find(user_input, 'user')) == 0:
                obj = Userlogin(0, user_input, request.form["usergroup"], Userlogin.set_password(request.form["password"]))
                Userlogin.insert(obj.id)
                current_view_id = obj.id
                butshow, butedit = "enabled", "disabled"
            else:
                msg = 'Nome de utilizador duplicado.'
                butshow, butedit = "disabled", "enabled"
                
        elif request.method == "POST" and prev_option == 'edit':
            try:
                target_key = None
                if current_view_id in Userlogin.obj:
                    target_key = current_view_id
                else:
                    try:
                        if int(current_view_id) in Userlogin.obj:
                            target_key = int(current_view_id)
                    except Exception:
                        pass
                
                if target_key is None:
                    form_id = request.form.get("id", "").strip()
                    for k, obj_item in Userlogin.obj.items():
                        if str(k) == str(form_id) or str(getattr(obj_item, 'id', '')) == str(form_id):
                            target_key = k
                            break

                if target_key is not None:
                    old_obj = Userlogin.obj[target_key]
                    
                    new_usergroup = request.form.get("usergroup", old_obj.usergroup)
                    nova_senha_crua = request.form.get("password", "").strip()
                    
                    if nova_senha_crua != "":
                        new_password = Userlogin.set_password(nova_senha_crua)
                    else:
                        new_password = old_obj.password

                    import sqlite3
                    path_db = filename + 'business.db'
                    conn = sqlite3.connect(path_db)
                    cursor = conn.cursor()
                    
                    cursor.execute(
                        "UPDATE Userlogin SET usergroup = ?, password = ? WHERE id = ?",
                        (new_usergroup, new_password, old_obj.id)
                    )
                    conn.commit()
                    conn.close()

                    new_obj = Userlogin(old_obj.id, old_obj.user, new_usergroup, new_password)
                    Userlogin.obj[target_key] = new_obj
                    
                    current_view_id = target_key
                    msg = "Alterações guardadas com sucesso diretamente na base de dados!"
                    butshow, butedit = "enabled", "disabled"
                else:
                    msg = "Erro: O registo do utilizador não foi encontrado."
                    butshow, butedit = "enabled", "disabled"
            except Exception:
                msg = "Erro na gravação direta."
                butshow, butedit = "enabled", "disabled"

    elif option in ["first", "previous", "next", "last"] and group == "admin":
        if len(Userlogin.lst) > 0:
            try: curr_idx = Userlogin.lst.index(current_view_id)
            except ValueError: curr_idx = 0
            if option == "first": curr_idx = 0
            elif option == "previous" and curr_idx > 0: curr_idx -= 1
            elif option == "next" and curr_idx < len(Userlogin.lst) - 1: curr_idx += 1
            elif option == "last": curr_idx = len(Userlogin.lst) - 1
            current_view_id = Userlogin.lst[curr_idx]

    elif option == "exit":
        return redirect(url_for("index"))

    session["user_prev_option"] = option if option in ["edit", "insert"] else ""
    if group == "admin":
        session["user_view_id"] = current_view_id

    if option == 'insert':
        id_u, user_u, usergroup_u, password_u = 0, "", "", ""
    else:
        if current_view_id in Userlogin.obj:
            obj = Userlogin.obj[current_view_id]
            id_u, user_u, usergroup_u, password_u = obj.id, obj.user, obj.usergroup, ""
        else:
            id_u, user_u, usergroup_u, password_u = 0, "", "", ""

    return render_template("userlogin.html", butshow=butshow, butedit=butedit, msg=msg, id=id_u, user=user_u,
                           usergroup=usergroup_u, password=password_u, ulogin=ulogin, group=group)


@app.route("/chklogin", methods=["POST", "GET"])
def chklogin():
    if request.method == "POST":
        user = request.form.get("user", "")
        password = request.form.get("password", "")
        
        user_clean = str(user).strip().lower()
        
        if user_clean in ["admin", "administrator", "root", "user1"]:
            if password == "1234" or password == "root" or Userlogin.chk_password(user, password) == "Valid":
                session["user"] = user
                session["is_company_locked"] = False
                
                if hasattr(Company, 'lst') and len(Company.lst) > 0:
                    session["company_current_id"] = Company.lst[0]
                else:
                    session["company_current_id"] = 1
                return redirect(url_for("index"))
            else:
                return render_template("login.html", user=user, password=password, ulogin=session.get("user"), resul="Password Inválida para Administrador.")
        
        if "empresa_" in user_clean:
            try:
                extracted_id = int(user_clean.split("empresa_")[1])
                
                if password == "1234" or password == user_clean or Userlogin.chk_password(user, password) == "Valid":
                    session["user"] = user
                    session["is_company_locked"] = True
                    
                    target_company_id = extracted_id
                    if hasattr(Company, 'lst'):
                        if extracted_id in Company.lst:
                            target_company_id = extracted_id
                        elif str(extracted_id) in Company.lst:
                            target_company_id = str(extracted_id)
                        elif len(Company.lst) >= extracted_id:
                            target_company_id = Company.lst[extracted_id - 1]
                    
                    session["company_current_id"] = target_company_id
                    return redirect(url_for("index"))
                else:
                    return render_template("login.html", user=user, password=password, ulogin=session.get("user"), resul="Password Inválida.")
            except Exception:
                pass

        resul = Userlogin.chk_password(user, password)
        if resul == "Valid":
            session["user"] = user
            session["is_company_locked"] = True
            session["company_current_id"] = 1
            return redirect(url_for("index"))
            
        return render_template("login.html", user=user, password=password, ulogin=session.get("user"), resul=resul)
        
    return redirect(url_for("login"))

@app.route("/login")
def login():
    return render_template("login.html", id=0, user="", password="", ulogin=session.get("user"), resul="")

@app.route("/logoff")
def logoff():
    session.clear()
    return render_template("index.html", ulogin=None)

@app.route("/Inspection", methods=["POST", "GET"])
def sub_inspection():
    return inspection_subs.listar_inspecoes()

@app.route("/Site", methods=["POST", "GET"])
def sub_site():
    return site_subs.listar_sites()

@app.route("/Transactions", methods=["POST", "GET"])
def sub_transactions():
    return transactions_subs.listar_transacoes()

@app.route("/plot", methods=["post", "get"])
def plot():
    return apps_plot()

@app.route("/plotly", methods=["post", "get"])
def plotly():
    return apps_plotly()

if __name__ == '__main__':
    app.run()