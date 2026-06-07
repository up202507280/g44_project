
import io
import base64
import pandas as pd
from sqlalchemy import create_engine
import matplotlib.pyplot as plt
import plotly.express as px
from flask import render_template, session, redirect, url_for


from classes.company import Company
from datefile import filename

def apps_plot(reload_databases_fn):

    ulogin = session.get("user")
    if not ulogin:
        return redirect(url_for("login"))
        
  
    reload_databases_fn()
    
  
    engine = create_engine('sqlite:///' + filename + 'mining.db')
    df_transactions = pd.read_sql('Transactions', con=engine)
    
 
    result = df_transactions.groupby('company_id')['amount'].sum()
    
   
    c_ids = result.index
    c_names = []
    for c_id in c_ids:
        if c_id in Company.obj:
            c_names.append(Company.obj[c_id].name)
        else:
            c_names.append(f"Empresa {c_id}")
            
    amounts = result.values
    
  
    fig, ax = plt.subplots()
    plt.bar(c_names, amounts, width=0.4, label='Company_id')
    x_index = range(len(c_names))
    plt.xticks(ticks=x_index, labels=c_names)
    plt.xlabel('Company Name')
    plt.ylabel('Total Amount')
    plt.title('Total Transactions by Company (Matplotlib)')
    
  
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close(fig)
    buf.seek(0)
    image = base64.b64encode(buf.getvalue()).decode('utf-8')
    
    return render_template("plot.html", image=image, ulogin=ulogin)


def apps_plotly(reload_databases_fn):
   
    ulogin = session.get("user")
    if not ulogin:
        return redirect(url_for("login"))
        
    
    reload_databases_fn()
    
  
    engine = create_engine('sqlite:///' + filename + 'mining.db')
    df_transactions = pd.read_sql('Transactions', con=engine)
    
   
    result = df_transactions.groupby('company_id')['amount'].sum()
    
    c_ids = result.index
    c_names = []
    for c_id in c_ids:
        if c_id in Company.obj:
            c_names.append(Company.obj[c_id].name)
        else:
            c_names.append(f"Empresa {c_id}")
            
    amounts = result.values
    
   
    fig = px.bar(x=c_names, y=amounts, labels={'x': 'Company Name', 'y': 'Total Amount'}, title='Total Transactions by Company (Plotly)')
    plot_div = fig.to_html(full_html=False, div_id='my-plot')
    
    return render_template("plotly.html", plot_div=plot_div, ulogin=ulogin)