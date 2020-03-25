from flask import Flask, request, render_template
from datetime import date
import pymysql
from wtforms import Form, StringField, TextAreaField, PasswordField, validators, IntegerField, SelectField
app = Flask(__name__, template_folder='/Users/tomabraham/PycharmProjects/firstProject/EVHoops/template')

@app.route('/')
def index():
    return "<h2>The official web page of Tom Abraham</h2>"

@app.route('/bacon', methods = ["GET", "POST"])
def bacon():
    if request.method == "POST":
        return "You are using POST"
    else:
        return "You are probably using GET"

@app.route('/Early Life')
def early_life():
    return "<h2>Early Life of Tom Abraham</h2>"

@app.route('/profile/<username>')
def profile(username):
    return "<h2>Welcome to your profile page " + username + "!</h2>"

@app.route('/post/<int:post_id>')
def post(post_id):
    return "<h2>Post ID is %s</h2>" %post_id


class RegisterForm(Form):
    first_name = StringField("First Name", [validators.Length(min=1, max=100)])
    last_name = StringField("Last Name", [validators.Length(min=1, max=100)])
    age = IntegerField("Age", [validators.required()])
    height = IntegerField("Height", [validators.required()])
    email = StringField("Email", [validators.Length(min=6, max=100)])
    favorite_position = SelectField(u'Favorite Position', choices=[('PG', 'Point Guard'), ('SG', 'Shooting Guard'), ('C', 'Center'), ('PF', 'Power Forward'), ('SF', 'Small Forward')])


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        age = request.form["age"]
        height = request.form["height"]
        email = request.form["email"]
        favorite_position = request.form["favorite_position"]

        # Open database connection
        db = pymysql.connect("localhost", "root", "Parath0du", "EVHoops")

        # prepare a cursor object using cursor() method
        cursor = db.cursor()

        # Auto incrementing the ID by selecting the max id in db and adding 1
        id_num = cursor.execute('''select max(idnew_table) from player_info''')
        records = cursor.fetchall()
        next_ID = records[0][0]

        if (next_ID == None):
            next_ID = 1
        else:
            next_ID = next_ID + 1

        # Prepare SQL query to INSERT a record into the database.
        today = date.today()
        print(today)
        sql = "INSERT INTO player_info(idnew_table, \
           first_name, last_name, age, height, email, favorite_position, create_date, update_date) \
           VALUES (%s, '%s', '%s', %s, %s, '%s', '%s', '%s', '%s')" % \
              (next_ID, first_name, last_name, age, height, email, favorite_position, today, today)
        print(sql)

        try:
            # Execute the SQL command
            cursor.execute(sql)
            # Commit your changes in the database
            db.commit()
        except:
            #Rollback in case there is any error
            return "DOESNT WORK"
            print(id_num)
            db.rollback()

        # disconnect from server
        db.close()
        return render_template('return_form.html', first_name=first_name, last_name=last_name, age=age, height=height, email=email, favorite_position=favorite_position)

    return render_template('register.html', form=form)

@app.route('/roster', methods=['GET', 'POST'])
def roster():
    # Open database connection
    db = pymysql.connect("localhost", "root", "Parath0du", "EVHoops")

    # prepare a cursor object using cursor() method
    cursor = db.cursor()

    cursor.execute("SELECT * FROM player_info")
    data = cursor.fetchall()

    for row in data:
        print(row)
    # disconnect from server
    db.close()

    return render_template("roster.html", data=data)

if __name__ == "__main__":
    app.run(debug=True)