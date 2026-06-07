from flask import render_template, session
from classes.company import Company
from datefile import filename

import pandas as pd
from sqlalchemy import create_engine
import matplotlib.pyplot as plt
import io
import base64

def apps_plot():
    engine = create_engine('sqlite:///' + filename + 'mining.db')
    df_transactions = pd.read_sql('Transactions', con=engine)
    result = df_transactions.groupby('company_id')['amount'].sum()
    result = result.sort_values(ascending=True)
    c_ids = result.index
    c_names = []
    for c_id in c_ids:
        c_obj = Company.obj[c_id]
        c_names.append(c_obj.name)
    amounts = result.values
    

    num_companies = len(c_names)
    fig_height = max(6, num_companies * 0.25) 
    
  
    fig, ax = plt.subplots(figsize=(10, fig_height), dpi=100)
    
  
    plt.barh(c_names, amounts, height=0.5, color='#0ea5e9', label='Company_id')
    
   
    ax.set_ylim(-0.5, num_companies - 0.5)
  
    
    plt.xlabel('Total Amount')
    plt.ylabel('Company Name')
    plt.title('Total Transactions by Company')
    
  
    plt.grid(axis='x', linestyle='--', alpha=0.5)
    
    plt.tight_layout()
    
 
    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=100)
    plt.close(fig)
    buf.seek(0)
    image = base64.b64encode(buf.getvalue()).decode('utf-8')
    
    return render_template("plot.html", image=image, ulogin=session.get("user"))