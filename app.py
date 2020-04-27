import os

from flask import Flask, render_template, flash, session, url_for, redirect
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Regexp, DataRequired, Length

app = Flask(__name__)
Bootstrap(app)
app.config['SECRET_KEY'] = "Don't tell anybody"
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = \
    'sqlite:///' + os.path.join(basedir, 'db/soen287.db')
app.config['SQLAlCHEMY_TRACK_MODIFICATIONS'] = False
app.config['USE_SESSION_FOR_NEXT'] = True
db = SQLAlchemy(app)


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    submit = SubmitField('Submit')
    forget = SubmitField('Forget password')


class RecoverForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired()])
    phone = StringField("PhoneNumber", validators=[DataRequired(), Length(10,10), Regexp('^[0-9]*$')])
    password = PasswordField('New Password', validators=[InputRequired()])
    submit = SubmitField('Submit')


class User(db.Model):
    __tablename__ = 'users'
    username = db.Column(db.String(16), primary_key=True, nullable=True)
    password = db.Column(db.String(32), nullable=True)
    phone = db.Column(db.String(10), nullable=True)


@app.route('/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.submit.data:
            user = User.query.filter_by(username=form.username.data).first()
            if user:
                if user.password == form.password.data:
                    flash("Log in successfully")
                    session['username'] = user.username
                    return render_template("base.html", username=session['username'])
                else:
                    return redirect("/")
            else:
                render_template("login.html", form=form)
        if form.forget.data:
            form = RecoverForm()
            render_template("forget.html", form=form)
    return render_template("login.html", form=form)


@app.route('/forget')
def recover():
    form = RecoverForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if user.phone == form.phone.data:
                user.password = form.password.data
                db.session.commit()
                form = LoginForm
                return render_template("login.html", form=form)
    return render_template('forget.html', form=form)


@app.route('/base')
def base():
    return render_template('base.html', username=session.get('username'))


@app.route('/general')
def general():
    return render_template('general.html', username=session.get('username'))


@app.route('/curr')
def curr():
    with open(basedir + "/data/curr.csv") as lines:
        return render_template('curr.html', lines=lines, username=session.get('username'))


@app.route('/degree')
def degree():
    return render_template('degree.html', username=session.get('username'))


@app.route('/desc')
def desc():
    return render_template('desc.html', username=session.get('username'));


@app.route('/pre')
def pre():
    return render_template('pre.html', username=session.get('username'));


if __name__ == '__main__':
    app.run(debug=True)
