"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import Flask,render_template,send_file
from flask import request
from PiWebFlask import app
import pyodbc
from io import BytesIO
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt1
import pandas as pd
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.dates import DateFormatter
import matplotlib.dates as mdates


@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""
    return render_template(
        'index.html',
        title='Home Page',
        year=datetime.now().year,
    )

@app.route('/DVLine/')
def DVLine():

    #plt.style.use('ggplot')
    
    fig,ax=plt.subplots(figsize=(12, 8))
    conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=DELL-PC;'
                      'Database=Pytest;'
                      'Trusted_Connection=yes;')
    df=pd.read_sql("select * from tblPointValue",conn) 
    
    time=df['DT']
    value=df['Value']
    
    
    # line graph single line
    #plt.plot(time,value,color='blue')
    
    #bar graph single bar using matplt
    #plt.bar(time,value,align='center',alpha=0.5)
    #multiple line
    #df.groupby(['DT','PointName']).count()['Value'].unstack().plot(ax=ax) 
    df.set_index('DT', inplace=True)
    df.groupby('PointName')['Value'].plot(legend=True)
    #plt.xlabel=("Date")
    #plt.ylabel("Value")
    plt.title("Consumption")
       
    #ax.xaxis.set_major_locator(mdates.DayLocator(interval=1))
    #ax.xaxis.set_major_locator(mdates.WeekdayLocator(interval=2))
    #ax.xaxis.set_major_locator(mdates.date_ticker_factory()
    ax.xaxis.set_major_formatter(DateFormatter("%d-%m"))
    canvas=FigureCanvas(fig)
    img=BytesIO()
    fig.savefig(img)
    img.seek(0)
    return send_file(img,mimetype='image/png')
    #cur = conn.cursor()  
    #curr.execute("select * from tblEmployees")  
    #rows = cur.fetchall()

      

@app.route('/contact')
def contact():
    """Renders the contact page."""

    return render_template(
        'contact.html',
        title='Contact',
        year=datetime.now().year,
        message='Your contact page.'
    )

@app.route('/about')
def about():
    """Renders the about page."""
    conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=DELL-PC;'
                      'Database=Pytest;'
                      'Trusted_Connection=yes;')
        
    cur = conn.cursor()  
    cur.execute("select * from tblEmployees")  
    rows = cur.fetchall() 
    return render_template(
        'about.html',
        title='About',
        year=datetime.now().year,
        message='Your application description page.'
        )
#code for Add page
 
@app.route("/AddDB")  
def AddDB():  
    return render_template("adddb.html")  

@app.route('/AddDBRecords',methods = ['POST'])  
def AddDBRecords():
    msg = "msg"  
    if request.method == "POST":
        try:
            name = request.form["name"]  
            email = request.form["email"]  
            address = request.form["address"] 
            conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=DELL-PC;'
                      'Database=Pytest;'
                      'Trusted_Connection=yes;')

            cur = conn.cursor()  
            cur.execute("INSERT into tblEmployees (name, email, address) values (?,?,?)",(name,email,address))  
            conn.commit()  
            msg = "Employee successfully Added"  
        except:
            msg = "We can not add the employee to the list"
            conn.rollback()  
        finally:  
            return render_template("success.html",msg = msg)  
            conn.close()  

#code for add page ends here
#code for View records
@app.route("/View")  
def View():
    try:
        conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=DELL-PC;'
                      'Database=Pytest;'
                      'Trusted_Connection=yes;')
        
        cur = conn.cursor()  
        cur.execute("select * from tblEmployees")  
        rows = cur.fetchall()  
        return render_template("View.html",rows = rows)
    except:
        msg = "We can not select employee to the list"
        conn.rollback()
    finally:
        #return render_template("success.html",msg = msg)  
        conn.close() 
#code for add page ends here
