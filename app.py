from flask import Flask,render_template,request,flash,redirect,url_for,session
from flask_mysqldb import MySQL
from datetime import datetime
from werkzeug.security import generate_password_hash,check_password_hash
import matplotlib.pyplot as plt
import os
from datetime import datetime




app=Flask(__name__)
db=MySQL(app)

app.secret_key='my_key'

app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']=''
app.config['MYSQL_DB']='user_db'


@app.route("/")
def home():
    return render_template("login.html")

@app.route("/view")
def view():
    if 'user_id' not in session:
        flash('login required')
        redirect(url_for('login'))

    return render_template("index.html")


@app.route("/expenses")
def expenses():
    
    if 'user_id' not in session:
        flash('login required')
        redirect(url_for('login'))


    cur=db.connection.cursor()
    cur.execute('SELECT * from expenses where user_id=%s',(session['user_id'],))
    data=cur.fetchall()
    return render_template('expenses.html',data=data)


@app.route("/add",methods=["GET", "POST"])
def add():

    if 'user_id' not in session:
        flash('login required')
        redirect(url_for('login'))


    if request.method=='POST':
        amount=request.form.get('amount')
        category=request.form.get('category')
        note=request.form.get('note')
        date=datetime.now().strftime('%y-%m-%d %H-%m-%S')
        
        
        cur=db.connection.cursor()
        cur.execute('''INSERT INTO expenses (category,amount,note,date,user_id) VALUES (%s,%s,%s,%s,%s)
                                     ''',(category,amount,note,date,session['user_id']))
        flash("data added sucessfully")
        db.connection.commit()
    return render_template("add.html")

@app.route("/edit/<string:id>",methods=['POST','GET'])
def edit(id):
     if request.method=='POST':
        amount=request.form.get('amount')
        category=request.form.get('category')
        note=request.form.get('note')
        date=datetime.now().strftime('%y-%m-%d %H-%m-%S')
        cur=db.connection.cursor()

        cur.execute('''UPDATE expenses
                       SET category=%s,amount=%s,note=%s,date=%s
                       WHERE  id=%s and user_id=%s''',(category,amount,note,date,id,session['user_id']))
        
        db.connection.commit()
        flash("data added sucessfully")
     cur=db.connection.cursor()
     cur.execute('SELECT * from expenses where id=%s and user_id=%s',(id,session['user_id']))
     data=cur.fetchone()
     return render_template('edit.html',i=data)


@app.route("/delete/<string:id>")
def delete(id):
    cur=db.connection.cursor()
    cur.execute('DELETE FROM expenses WHERE id=%s and user_id=%s',(id,session['user_id']))
    db.connection.commit()
    render_template('expenses.html')
    flash("delete data successfully")
    return redirect(url_for('expenses'))


import bcrypt





@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['set_password'].strip().encode('utf-8')

        cur = db.connection.cursor()
        cur.execute("SELECT * FROM registration WHERE Email = %s", (email,))
        user = cur.fetchone()
        

        if user:
            flash('Email already registered')
            return redirect(url_for('register'))

        hashed_pw = bcrypt.hashpw(password, bcrypt.gensalt())
        cur.execute("INSERT INTO registration (Username, Email, Password) VALUES (%s, %s, %s)",
                    (username, email, hashed_pw.decode('utf-8')))
        db.connection.commit()
        cur.close()
        flash('Registration successful. Please log in.')
        return redirect(url_for('login'))
    
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password'].strip().encode('utf-8')

        cur = db.connection.cursor()
        cur.execute("SELECT * FROM registration WHERE Email = %s", (email,))
        user = cur.fetchone()

        if user and bcrypt.checkpw(password, user[3].encode('utf-8')):
            session['username'] = user[1]
            session['user_id'] = user[0]
            flash('Login successful')
            return redirect(url_for('view'))
        else:
            flash('Invalid email or password')
            return redirect(url_for('login'))

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()
    flash('logout successfully')
    return redirect(url_for('login'))



@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash('login required')
        return redirect(url_for('login'))

    cur = db.connection.cursor()

    # Total sum
    cur.execute('SELECT SUM(amount) FROM expenses WHERE user_id=%s', (session['user_id'],))
    sum_amount = cur.fetchone()[0] or 0

    # Category-wise totals
    cur.execute('''
        SELECT category, SUM(amount)
        FROM expenses
        WHERE user_id = %s
        GROUP BY category
    ''', (session['user_id'],))
    category_amount = cur.fetchall()

    # Average daily spend
    cur.execute('''
        SELECT DATE(date), SUM(amount)
        FROM expenses
        WHERE user_id = %s
        GROUP BY DATE(date)
    ''', (session['user_id'],))
    daily_expenses = cur.fetchall()
    avg_daily_expense = round(sum([row[1] for row in daily_expenses]) / len(daily_expenses), 2) if daily_expenses else 0

    # Generate static graph using Matplotlib
    if category_amount:
        categories = [row[0] for row in category_amount]
        amounts = [row[1] for row in category_amount]

        plt.figure(figsize=(8, 5))
        plt.bar(categories, amounts, color='skyblue')
        plt.title("Expenses by Category")
        plt.xlabel("Category")
        plt.ylabel("Amount (₹)")
        plt.tight_layout()

        chart_path = os.path.join("static", "charts", f"{session['user_id']}_chart.png")

        os.makedirs(os.path.dirname(chart_path), exist_ok=True)
        plt.savefig(chart_path)
        plt.close()

    else:
        chart_path = None

    #this month expenses
    now=datetime.now()
    year=now.year
    month=now.month
    cur.execute('''
                          select sum(amount),date from expenses
                          where user_id=%s and MONTH(date)=%s and YEAR(date)=%s''',([session['user_id'],month,year]))
    this_month_total=cur.fetchone()[0]  
    

    return render_template('dashboard.html',
                           sum_amount=sum_amount,
                           category_amount=category_amount,
                           avg_daily_expense=avg_daily_expense,
                           chart_path=chart_path,
                           this_month_total=this_month_total)



if __name__ == "__main__":
    app.run(debug=True)



    