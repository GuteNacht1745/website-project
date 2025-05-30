from flask import Flask, render_template, url_for
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from werkzeug.utils import redirect
from wtforms import StringField, SubmitField, URLField, TimeField, SelectField
from wtforms.validators import DataRequired, URL
import csv
from dotenv import load_dotenv
import os

load_dotenv('secret.env')
SECRET_KEY = os.getenv('SECRET_KEY')

app = Flask(__name__)

app.config['SECRET_KEY'] = SECRET_KEY
Bootstrap5(app)


class CafeForm(FlaskForm):
    cafe = StringField('Cafe name', validators=[DataRequired()])
    location = URLField('Location on Google Map (URL)', validators = [DataRequired(), URL()])
    open = TimeField(label = 'Opening hours')
    close = TimeField(label = 'Closing hours')
    coffee_rating = SelectField(label = 'Coffee rating', choices = [(i , i * '☕️') for i in range(1,6)], coerce = int)
    wifi_rating = SelectField(label = 'Wifi strength rating', choices = [(i, i * '💪') for i in range(1,6)], coerce = int)
    power_outlet_rating = SelectField(label = 'Power socket availability', choices = [(i , i * '🔌') for i in range(1,6)], coerce = int)
    submit = SubmitField('Submit')

# ---------------------------------------------------------------------------


# all Flask routes below
@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add', methods = ['GET', 'POST'])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        new_coffee = [form.cafe.data,
                      form.location.data,
                      form.open.data.strftime("%I:%M%p"),
                      form.close.data.strftime("%I:%M%p"),
                      form.coffee_rating.data * '☕',
                      form.wifi_rating.data * '💪',
                      form.power_outlet_rating.data * '🔌']
        with open('cafe-data.csv', mode='a', newline = '', encoding = 'utf-8') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(new_coffee)

        return redirect(url_for('cafes'))
    return render_template('add.html', form=form)


@app.route('/cafes')
def cafes():
    with open('cafe-data.csv', newline='', encoding='utf-8') as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = [row for row in csv_data]
    return render_template('cafes.html', cafes=list_of_rows)


if __name__ == '__main__':
    app.run()
