from flask import Flask,render_template,request,redirect,url_for

'''
It creates an instance of the Flask class
Which will be your WSGI application'''

app = Flask(__name__)

#HTML integration

@app.route("/")
def welcome():
    return "<html><H1>Welcome Rajib!</H1></html>"

@app.route("/index")
def index():
    return render_template('index.html')

#HTTP Verb GET and POST

@app.route('/form',methods=['GET','POST'])
def form():
    if request.method=='POST':
        name=request.form['name']
        return f'Hello {name}!'
    
    return render_template('form.html')


## Variable Rule

@app.route('/success/<int:score>')

def success(score):
    res=''
    if score>=50:
        res="PASS"
    else:
        res="FAIL"

    return render_template('result.html',results=res)    

##For condition
@app.route('/successres/<int:score>')

def successres(score):
    res=''
    if score>=50:
        res="PASS"
    else:
        res="FAIL"
    
    exp={"score":score,"res":res}

    return render_template('result1.html',results=exp) 
    

##if condition

@app.route('/successif/<int:score>')

def successif(score):
    

    return render_template('result.html',results=score) 

##Dynamic url Creation




#entry point of a code in python
if __name__ =="__main__":
    app.run(debug=True)

