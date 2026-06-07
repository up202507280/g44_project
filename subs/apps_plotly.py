from flask import render_template, session
from classes.company import Company
from datefile import filename

import pandas as pd
from sqlalchemy import create_engine
import plotly.express as px

def apps_plotly():
    
    engine = create_engine('sqlite:///' + filename + 'mining.db')
    df_transactions = pd.read_sql('Transactions', con=engine)
    
 
    result = df_transactions.groupby('company_id')['amount'].sum()
    
    
    c_ids = result.index
    c_names = []
    for c_id in c_ids:
        c_obj = Company.obj[c_id]
        c_names.append(c_obj.name)
        
    amounts = result.values
    
   
    fig = px.bar(x=c_names, y=amounts, labels={'x': 'Company Name', 'y': 'Total Amount'}, title='Total Transactions by Company')
    
    plot_div = fig.to_html(full_html=False, div_id='my-plot')
    
    return render_template("plotly.html", plot_div=plot_div, ulogin=session.get("user"))
