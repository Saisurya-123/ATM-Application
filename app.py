from flask import Flask,request,redirect,url_for,render_template,make_response,jsonify
from datetime import datetime
app=Flask(__name__)
users={}
statements={}
@app.route('/')
def home():
    return render_template('index.html')
@app.route('/userregistration',methods=['GET','POST'])
def userregistration():
    if request.method=='POST':
        print(request.form)
        username=request.form['username'] #ambica
        password=request.form['password'] #123
        pin_no=request.form['pin_no']
        if username not in users:
            users[username]={'password':password,'pin_no':pin_no,'Amount':0}
            statements[username]={'deposit':[],'withdraw':[]}
            return redirect(url_for('login'))
        else:
            return 'username already existed'

    return render_template('register.html')
@app.route('/login',methods=['GET','POST'])
def login():
    if request.method=='POST':
        login_username=request.form['username'] #anusha
        login_password=request.form['password'] #123
        if login_username in users:
            if login_password==users[login_username]['password']:
                resp=make_response(redirect(url_for('dashboard')))
                resp.set_cookie('userid',login_username)
                return resp
            else:
                return 'password wrong'
        else:
            return 'email not found'
    return render_template('login.html')
@app.route('/dashboard')
def dashboard():
    if request.cookies.get('userid'):
        user=request.cookies.get('userid')
        return render_template('dashboard.html',user=user)
    else:
        return 'pls login to access dashboard'
@app.route('/deposit',methods=['GET','PUT'])
def deposit():
    if request.cookies.get('userid'):
        username=request.cookies.get('userid')
        if request.method=='PUT':
            amount=int(request.get_json('amount')['amount']) #{'amount':'200'}
            if amount<=0:
                return jsonify({'message':'amount should positive value'})
            elif amount>0 and amount < 50000:
                users[username]['Amount']=users[username]['Amount']+amount #updating amount for users dict
                dep_time=datetime.now() # generate cuurent time
                statements[username]['deposit'].append((amount,dep_time))
                return jsonify({'message':f"Amount deposited {users[username]['Amount']}"})
            elif amount > 50000:
                return jsonify({'message':'Amount exceeded > 50000'})
            else:
                return jsonify({'message':'invalid amount value'})
            
        return render_template('deposit.html')
    else:
        return 'pls login to deposit'
@app.route('/withdrawal',methods=['GET','PUT'])
def withdrawal():
    if request.cookies.get('userid'):
        username=request.cookies.get('userid')
        balance_amount=users[username]['Amount']
        if request.method=='PUT':
            amount=int(request.get_json('amount')['amount']) #{'amount':200}
            if amount<=0:
                return jsonify({'message':'amount should positive value'})
            elif amount>0 and amount <= balance_amount:
                users[username]['Amount']=users[username]['Amount']-amount # updating users dict by sub amount
                wid_time=datetime.now() # generating current time
                statements[username]['withdraw'].append((amount,wid_time))
                return jsonify({'message':f"Amount withdrawal successfully {amount}"})
            elif amount > balance_amount:
                return jsonify({'message':f'Amount exceeded  than balance amount{balance_amount}'})
            else:
                return jsonify({'message':'invalid amount value'})
        return render_template('withdraw.html')
    else:
        return redirect(url_for('login'))
@app.route('/balance')
def balance():
    if request.cookies.get('userid'):
        username=request.cookies.get('userid')
        bal_amount=users[username]['Amount']
        return render_template('balance.html',bal_amount=bal_amount)
    else:
        return redirect(url_for('login')) 
@app.route('/user_statements')
def user_statements():
    if request.cookies.get('userid'):
        username=request.cookies.get('userid')
        user_statementdata=statements[username]
        return render_template('statements.html',user_statementdata=user_statementdata,username=username)
    else:
        return redirect(url_for('login'))
app.run(debug=True,use_reloader=True)