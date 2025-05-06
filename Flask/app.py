from flask import Flask,render_template,request
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



    


#entry point of a code in python
if __name__ =="__main__":
    app.run(debug=True)

