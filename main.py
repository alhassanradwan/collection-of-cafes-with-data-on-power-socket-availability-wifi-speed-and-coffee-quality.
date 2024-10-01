from flask import Flask, render_template,redirect,url_for
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField , SelectField
from wtforms.validators import DataRequired,URL
import csv

'''
Red underlines? Install the required packages first: 
Open the Terminal in PyCharm (bottom left). 

On Windows type:
python -m pip install -r requirements.txt

On MacOS type:
pip3 install -r requirements.txt

This will install the packages from requirements.txt for this project.
'''

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)


class CafeForm(FlaskForm):
    cafe = StringField('Cafe name', validators=[DataRequired()])
    location=StringField('cafe loaction on google maps(URL)', validators=[DataRequired(),URL()])
    open=StringField('open cafe at 8:00 AM',validators=[DataRequired()])
    close=StringField('close cafe at 8:00 PM',validators=[DataRequired()])
    coffee_rating=SelectField('coffee rating',choices=["☕️", "☕☕", "☕☕☕", "☕☕☕☕", "☕☕☕☕☕"], validators=[DataRequired()])
    wifi_rating=SelectField('wifi rating',choices=["✘", "💪", "💪💪", "💪💪💪", "💪💪💪💪", "💪💪💪💪💪"] ,validators=[DataRequired()])
    power_rating = SelectField("Power Socket Availability", choices=["✘", "🔌", "🔌🔌", "🔌🔌🔌", "🔌🔌🔌🔌", "🔌🔌🔌🔌🔌"], validators=[DataRequired()])
    submit = SubmitField('Submit')


# all Flask routes below
@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add')
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        with open("cafe-data.txt",mode="a",encoding="utf-8") as csv_file:
            csv_file.writer(f"\n{form.cafe.data},"
                            f"\n{form.location.data},"
                            f"\n{form.open.data},"
                            f"\n{form.close.data},"
                            f"\n{form.coffee_rating.data},"
                            f"\n{form.wifi_rating.data},"
                            f"\n{form.power_rating.data}")
            return redirect(url_for('cafes'))
    
    return render_template('add.html', form=form)
# 1. Form Validation (if form.validate_on_submit():)
# This line checks whether the form has been submitted (via a POST request) and whether the form data passes all the validation rules you defined in the CafeForm class.
# validate_on_submit() is a Flask-WTF method that returns True if the form is submitted and passes validation.
# 2. Opening the CSV File (with open("cafe-data.csv", mode="a", encoding='utf-8') as csv_file:)
# This line opens a file named cafe-data.csv in append mode (mode="a"). The append mode means the file is opened, and new data is added to the end without erasing the previous content.

@app.route('/cafes')
def cafes():
    with open('cafe-data.csv', newline='', encoding='utf-8') as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)
    return render_template('cafes.html', cafes=list_of_rows)


if __name__ == '__main__':
    app.run(debug=True, port=5002)
