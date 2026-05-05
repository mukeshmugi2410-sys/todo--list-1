from flask import Flask,request,redirect,render_template
from flask_sqlalchemy import SQLAlchemy

app=Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"]= "mysql+pymysql://flask:flask123@localhost/demo"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS" ]=False
db=SQLAlchemy(app)

class Pro(db.Model):
    __tablename__="demoproject"
    ID=db.Column(db.Integer, primary_key=True)
    NAME = db.Column(db.String(50))
    AGE = db.Column(db.Integer)

with app.app_context():
     db.create_all()
     
@app.route('/')
def index():
    users= Pro.query.all()
    return render_template("to-do.html",users=users)

@app.route("/add", methods=['POST'])
def add():
    name=request.form.get("name")
    age=request.form.get("age")

    new_user = Pro(NAME=name,AGE=age)
    db.session.add(new_user)
    db.session.commit()
    
    return redirect('/')
@app.route("/update/<int:id>",methods=['POST','GET'])
def update(id):

    users=Pro.query.get_or_404(id)

    if request.method=="POST":
        users.NAME=request.form.get("name")
        users.AGE=request.form.get("age")

        
        db.session.commit()
        return redirect('/')
    return render_template("update.html", users=users)

@app.route("/delete/<int:id>")
def delete(id):

    users=Pro.query.get_or_404(id)
    db.session.delete(users)
    db.session.commit()
    return redirect("/")

if __name__=="__main__":
    app.run(debug=True)