from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime 
import smtplib 

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///homework.db'

db=SQLAlchemy(app)

#create a database model
class Notes_Data(db.Model):
    #__setup_table__='friends'
    id = db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(200), nullable = False)
    subject =db.Column(db.String(200) )
    chapter=db.Column(db.String(100))
    link=db.Column(db.String(300))
    hw =db.Column(db.String(200))
    date_created = db.Column(db.DateTime, default=datetime.now())
    

    #function to return data
    def __repr__(self):
        return '<Name %r>' % self.id
 
#db.create_all()

email_id='notdefinedareyou@gmail.com'

@app.route('/')
def index():
    hw_data=Notes_Data.query.order_by(Notes_Data.date_created)
    return render_template('index.html', time=(datetime.now().strftime("%B %d, %y ")), data = hw_data)

@app.route('/subjects')
def subjects():
    return render_template('subjects.html')

@app.route('/notes/<sub>' , methods=['GET','POSTS'])
def view(sub):
    print(sub)
    data=Notes_Data.query.filter_by(subject=(str(sub)))
    #data=Notes_Data.query.order_by(Notes_Data.date_created)
    return render_template('view.html' ,friend = data )



@app.route('/update/<int:id>',methods=['POST','GET'])
def update(id):
    friend_to_update= Notes_Data.query.get_or_404(id)
    if request.method == 'POST':
        friend_to_update.chapter= request.form['chapter']
        friend_to_update.link = request.form['link']
        try :
            db.session.commit()
            return redirect('/subjects')

        except:
            return 'Sorry , an error occured !'
    else:
        return render_template('update.html',editing_data=friend_to_update )
    
     

@app.route('/updates/<int:id>', methods=['POST','GET'])
def updates(id):
    friend_to_update= Notes_Data.query.get_or_404(id)
    if request.method == 'POST':
        friend_to_update.hw= request.form['name']
        
        try :
            db.session.commit()
            return redirect('/index')

        except:
            return 'Sorry , an error occured !'
    else:
        return render_template('updates.html',editing_data=friend_to_update, friend=Notes_Data.query.order_by(Notes_Data.date_created))
    
@app.route('/delete/<int:id>')
def delete(id):
    friend_to_delete= Notes_Data.query.get_or_404(id)    
    try :
        db.session.delete((friend_to_delete))
        db.session.commit()
        return redirect('/')
    except:
        return 'Error is there Boss'


@app.route('/homework',methods=['POST','GET'])
def homework():
    
    hw_name = request.form.get('name')
    if not hw_name:
        return render_template('index.html',all_fields_needed_msg='Enter valid Input')


    print(hw_name)
        
    new_friend= Notes_Data(name=f'Homework {hw_name}',hw=str(hw_name))

        #push into database
    try :
        db.session.add(new_friend)
        db.session.commit()
        return redirect('/') 
    except:
        return 'Error'
    


@app.route('/upload')
def upload():
    return render_template('upload.html')

@app.route('/form', methods =['POST',"GET"])
def form():
    name= request.form.get('person_name')
    link=request.form.get('entered_link')
    subject= request.form.get('subject')
    chapter_name=request.form.get('chapter_name')
    email_entered=request.form.get('enter_email')

    print(name , link, subject )

    if not name or not link or not email_entered or (subject==''):
        error_statement='All Fields Required'
        return render_template('upload.html', all_fields_msg=error_statement,name=name,
        email=email_entered, link=link)

    try:
        datas=Notes_Data(name=name,subject=subject,chapter=chapter_name , link=link)
        db.session.add(datas)
        db.session.commit()
    except Exception as e:
        return 'Error'
    
    return redirect('/subjects')

@app.route('/support')
def support():
    return render_template('support.html')

app.run(debug=True)