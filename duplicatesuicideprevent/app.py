# users database for user name details
import yagmail
from flask import Flask, render_template, request, redirect, url_for, flash
from flask.sessions import SessionInterface, SessionMixin
from flask_sqlalchemy import SQLAlchemy
from flask import session
import csv
import random 
# import yagmail
# Add the send_test_notification function here
def send_test_notification(sender_email, sender_password, recipient_email, subject, contents):
    yag = yagmail.SMTP(sender_email, sender_password)
    yag.send(
        to=recipient_email,
        subject=subject,
        contents=contents
    )
    yag.close()
 
# from flask import Flask, render_template, request, redirect, url_for, flash, session
# from flask_sqlalchemy import SQLAlchemy
# import csv
# import random 
app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a random value
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/sprevent'  # Update with your database connection details
db = SQLAlchemy(app)
# 
# Route to send a test notification email    
# 
def select_random_row(csv_file):
    with open(csv_file, 'r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        rows = [row for row in reader]
        if rows:
            return random.choice(rows)
        else:
            return None

# Define User model
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    number = db.Column(db.String(20), nullable=False)
    parent_no = db.Column(db.String(50), nullable=False)
# 
    #newly updated column 
    friend_no = db.Column(db.String(50), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    gender = db.Column(db.String(50), nullable=False)
    age = db.Column(db.String(20), nullable=False)
    # 
# 
# Define PSSResult model
class PSSResult(db.Model):
    __tablename__ = 'prevent'
    id = db.Column(db.Integer, primary_key=True)
    q1 = db.Column(db.Integer, nullable=False)
    q2 = db.Column(db.Integer, nullable=False)
    q3 = db.Column(db.Integer, nullable=False)
    q4 = db.Column(db.Integer, nullable=False)
    q5 = db.Column(db.Integer, nullable=False)
    q6 = db.Column(db.Integer, nullable=False)
    q7 = db.Column(db.Integer, nullable=False)
    q8 = db.Column(db.Integer, nullable=False)
    q9 = db.Column(db.Integer, nullable=False)
    q10 = db.Column(db.Integer, nullable=False)
    total_value = db.Column(db.Integer, nullable=False)
    risk_level = db.Column(db.String(20), nullable=False)
# 
# Route to render the homepage
#
class PSSResult1(db.Model):
    __tablename__ = 'newtest'
    id = db.Column(db.Integer, primary_key=True)
    q1 = db.Column(db.Integer, nullable=False)
    q2 = db.Column(db.Integer, nullable=False)
    q3 = db.Column(db.Integer, nullable=False)
    q4 = db.Column(db.Integer, nullable=False)
    q5 = db.Column(db.Integer, nullable=False)
    q6 = db.Column(db.Integer, nullable=False)
    q7 = db.Column(db.Integer, nullable=False)
    q8 = db.Column(db.Integer, nullable=False)
    q9 = db.Column(db.Integer, nullable=False)
    q10 = db.Column(db.Integer, nullable=False)
    total_value = db.Column(db.Integer, nullable=False)
    risk_level = db.Column(db.String(20), nullable=False)

#  
@app.route('/')
def homepage():
    return render_template('homepage.html')

# Route to render the signinup page
@app.route('/signinup')
def signinup():
    return render_template('signinup.html')
# --------------------------------------------------------
@app.route('/signout')
def signout():
    # Clear the user authentication status
    session.pop('user_id', None)  # Use session instead of SessionMixin
    return redirect(url_for('homepage'))

# Route to render the PSS Test page
# Route to render the PSS Test page
@app.route('/pss-test')
def pss_test():
    # Check if the user is authenticated
    if 'user_id' not in session:
        flash('Please sign in to take the PSS test', 'error')
        return redirect(url_for('signinup'))

    return render_template('psstest.html')
# 
# 
@app.route('/pss1-test')
def pss1_test():
    # Check if the user is authenticated
    if 'user_id' not in session:
        flash('Please sign in to take the PSS test', 'error')
        return redirect(url_for('signinup'))

    return render_template('fivetest.html')
# 
# 
@app.route('/stressdata')
def stressdata():
    # Check if the user is authenticated
    if 'user_id' not in session:
        flash('Please sign in to view this page.', 'error')
        return redirect(url_for('signinup'))

    csv_file = 'D:\dact.csv'  # Update this path
    labels = ["TotalSteps", "TotalDistance", "SedentaryMinutes", "Calories", "heartrate", "MinutesAsleep", "stressscore"]

    random_row = select_random_row(csv_file)

    if random_row:
        data = {label: float(value) for label, value in zip(labels, random_row)}
        # data = {label: value for label, value in zip(labels, random_row)}
        return render_template('stressdata.html', data=data)
    else:
        flash('No data available.', 'error')
        return redirect(url_for('homepage'))


# -----------------------------------------------------------------------
# # Route to render the PSS Test page
# @app.route('/pss-test')
# def pss_test():
#     return render_template('psstest.html')

# Route to handle PSS Test form submission
@app.route('/submit-pss', methods=['POST'])
def submit_pss():
    if request.method == 'POST':
        # Extract form data
        q1 = int(request.form['q1'])
        q2 = int(request.form['q2'])
        q3 = int(request.form['q3'])
        q4 = int(request.form['q4'])
        q5 = int(request.form['q5'])
        q6 = int(request.form['q6'])
        q7 = int(request.form['q7'])
        q8 = int(request.form['q8'])
        q9 = int(request.form['q9'])
        q10 = int(request.form['q10'])

        # Calculate total value
        total_value = q1 + q2 + q3 + q4 + q5 + q6 + q7 + q8 + q9 + q10

        # Determine category
        if (total_value <= 13 and total_value>=0):
            risk_level = "normal"
        elif (total_value <= 26 and total_value>=14):
            risk_level = "Acute"
        else:
            risk_level = "chronic"

        # Create a new PSSResult objecthttp://127.0.0.1:5000
        new_result = PSSResult(
            q1=q1, q2=q2, q3=q3, q4=q4, q5=q5,
            q6=q6, q7=q7, q8=q8, q9=q9, q10=q10,
            total_value=total_value, risk_level=risk_level
        )

        # Add the new result to the database
        db.session.add(new_result)
        db.session.commit()

        flash('PSS Test submitted successfully!', 'success')
        # Redirect based on risk_level
        if risk_level == "normal":
            return redirect(url_for('normal'))
        elif risk_level == "Acute":
            return redirect(url_for('acute'))
        else:
            return redirect(url_for('chronic'))
        # Pass risk_level to the template
        # return render_template('pssresult.html', risk_level=risk_level)
# 
#
@app.route('/submit-pss1', methods=['POST'])
def submit_pss1():
    if request.method == 'POST':
        # Extract form data
        q1 = int(request.form['q1'])
        q2 = int(request.form['q2'])
        q3 = int(request.form['q3'])
        q4 = int(request.form['q4'])
        q5 = int(request.form['q5'])
        q6 = int(request.form['q6'])
        q7 = int(request.form['q7'])
        q8 = int(request.form['q8'])
        q9 = int(request.form['q9'])
        q10 = int(request.form['q10'])

        # Calculate total value
        total_value = q1 + q2 + q3 + q4 + q5 + q6 + q7 + q8 + q9 + q10

        # Determine category
        if (total_value <= 13 and total_value>=0):
            risk_level = "normal"
        elif (total_value <= 26 and total_value>=14):
            risk_level = "Acute"
        else:
            risk_level = "chronic"

        # Create a new PSSResult object
        new_result1 = PSSResult1(
            q1=q1, q2=q2, q3=q3, q4=q4, q5=q5,
            q6=q6, q7=q7, q8=q8, q9=q9, q10=q10,
            total_value=total_value, risk_level=risk_level
        )

        # Add the new result to the database
        db.session.add(new_result1)
        db.session.commit()

        flash('PSS Test submitted successfully!', 'success')
        # Redirect based on risk_level
        if risk_level == "normal":
            return redirect(url_for('normal'))
        elif risk_level == "Acute":
            return redirect(url_for('acute'))
        else:
            return redirect(url_for('chronic'))# 
# 
         
@app.route('/normal')
def normal():
    return render_template('normal.html')

# Route to render acute.html
# homepage contents
@app.route('/about')
def about():
    return render_template('about.html')
@app.route('/res')
def res():
    return render_template('res.html')
@app.route('/contact')
def contact():
    return render_template('contact.html')    
# homepage contents
@app.route('/acute')
def acute():
    return render_template('acute.html')
# Route to render chronic.html
@app.route('/chronic')
def chronic():
    return render_template('chronic.html')
# Route to handle user registration form submission
@app.route('/signup', methods=['POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        number = request.form['number']
        parent_no = request.form['parent_no']
        #newly updated column
        friend_no = request.form['friend_no']
        location = request.form['location']
        gender = request.form['gender']
        age = request.form['age']
        #newly updated column

        # Check if user already exists
        if User.query.filter_by(email=email).first():
            flash('Email already exists. Please use a different email.', 'error')
            return redirect(url_for('signinup'))

        # Create a new User object with plaintext password
        new_user = User(username=username, email=email, password=password, number=number, parent_no=parent_no,friend_no=friend_no,location=location,gender=gender,age=age)

        try:
            # Add the new user to the database
            db.session.add(new_user)
            db.session.commit()
            flash('Successfully signed up!', 'success')
            return redirect(url_for('signinup'))
        except Exception as e:
            db.session.rollback()
            flash(f"There was an issue signing up: {str(e)}", 'error')
            return redirect(url_for('signinup'))

# Route to handle user sign in form submission
'''@app.route('/signin', methods=['POST'])
def signin():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Authenticate user
        user = User.query.filter_by(email=email, password=password).first()

        if user:
            flash(f'Welcome, {user.username}!', 'success')
            return redirect(url_for('homepage'))
        else:
            flash('Invalid email or password', 'error')
            return redirect(url_for('signinup'))

if __name__ == '__main__':
    app.run(debug=True)
'''
# Route to handle user sign in form submission
@app.route('/signin', methods=['POST'])
def signin():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Authenticate user
        user = User.query.filter_by(email=email, password=password).first()

        if user:
            # Set user_id in session upon successful sign-in
            session['user_id'] = user.id
            flash(f'Welcome, {user.username}!', 'success')
            return redirect(url_for('homepage'))
        else:
            flash('Invalid email or password', 'error')
            return redirect(url_for('signinup'))
# notification program
'''@app.route('/send-test-notification', methods=['GET'])
def send_test_notification_route():
    # Send test notification email
    user_id = session['user_id']
    user = User.query.get(user_id)
    # recipient_email = user.email
    sender_email = '2k21cse152@kiot.ac.in'
    sender_password = 'kiot1234@'
    recipient_email = user.email
    subject = 'Test Notification for the mental distress '
    contents = 'You can take the test to analyse the mental health. Good luck!'
    # name=user.name;
    send_test_notification(sender_email, sender_password, recipient_email, subject, contents)
    return 'Test notification email sent successfully!' '''  
# 
# chronic notification
# @app.route('/send-test-notification', methods=['GET'])
# def send_test_notification_route():
#     # Send test notification email
#     user_id = session['user_id']
#     user = User.query.get(user_id)
#     # recipient_email = user.email
#     sender_email = '2k21cse152@kiot.ac.in'
#     sender_password = 'kiot1234@'
#     recipient_email = user.email
#     subject = 'Test Notification Nandhinik'
#     contents = 'You can now take the test. Good luck!'
#     # name=user.name;
#     send_test_notification(sender_email, sender_password, recipient_email, subject, contents)
#     return 'Test notification email sent successfully!'   

# chronic notification
@app.route('/send-chronic-notification', methods=['GET'])
def send_chronic_notification_route():
    # Send test notification email
    user_id = session['user_id']
    user = User.query.get(user_id)
    # recipient_email = user.email
    sender_email = '2k21cse152@kiot.ac.in'
    sender_password = 'kiot1234@'
    recipient_email = user.email
    subject = 'Test Notification from StressMonitoring System'
    contents = 'Chronic stress level!'
    # name=user.name;

    send_test_notification(sender_email, sender_password, recipient_email, subject, contents)
    return 'Test notification email sent successfully!'   

# stress notification
# @app.route('/send-stresslevel-notification', methods=['GET'])
'''@app.route('/send-stresslevel-notification', methods=['GET'])
def send_stresslevel_notification_route():
    try:
        user_id = session.get('user_id')
        if user_id is None:
            return 'User not logged in', 401

        user = User.query.get(user_id)
        if user is None:
            return 'User not found', 404

        sender_email = 'your_sender_email@example.com'
        sender_password = 'your_sender_password'
        recipient_email = user.email
        subject = 'Overcoming Stress: Your Guide to a Serene Mind'
        contents = 'Your personalized stress notification message'

        send_test_notification(sender_email, sender_password, recipient_email, subject, contents)
        return 'Stress notification sent successfully!'
    except Exception as e:
        return f'Error: {str(e)}', 500

@app.route('/send-cal-notification', methods=['GET'])
def send_cal_notification_route():
    # Send test notification email
    user_id = session['user_id']
    user = User.query.get(user_id)
    # recipient_email = user.email
    sender_email = '2k21cse152@kiot.ac.in'
    sender_password = 'kiot1234@'
    recipient_emails = user.email
    subject = 'Track your health!'
    contents = """Hi there,<br><br>
            It's important to keep track of your calorie intake for maintaining a healthy lifestyle. Here are some tips to help you manage your calories:<br><br>
            1. Keep a food diary to record what you eat throughout the day. This can help you become more aware of your eating habits and make healthier choices.<br>
            2. Pay attention to portion sizes. Use measuring cups or a food scale to accurately measure your food portions, especially for high-calorie foods.<br>
            3. Choose nutrient-dense foods that are rich in vitamins, minerals, and fiber, such as fruits, vegetables, whole grains, lean proteins, and healthy fats.<br>
            4. Be mindful of liquid calories from sugary beverages like soda, juice, and alcohol. Opt for water, herbal tea, or other low-calorie drinks instead.<br>
            5. Incorporate regular physical activity into your routine to help balance your calorie intake and expenditure.<br><br>
            Remember, maintaining a healthy weight is not just about counting calories, but also about making nutritious food choices and staying active.<br><br>
            Wishing you success on your health journey!
            """
    images = ['/static/cal.jpg']  # Add paths to your image files
    website = 'https://www.choosemyplate.gov/resources/MyPlatePlan'

    send_test_notification(sender_email, sender_password, recipient_emails, subject, contents, images, website)
# 
''' 
if __name__ == '__main__':
    app.run(debug=True)