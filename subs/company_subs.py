import datetime
from flask import render_template, request, session

from classes.company import Company

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

    return render_template("index.html", butshow=butshow, butedit=butedit, 
                    id=id, name=name, dob=dob, current_action=current_action,
                    ulogin=session.get("user"))
