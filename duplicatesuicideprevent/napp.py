from flask import Flask, render_template
import yagmail

app = Flask(__name__)

def send_test_notification(sender_email, sender_password, recipient_email, subject, contents):
    yag = yagmail.SMTP(sender_email, sender_password)
    yag.send(
        to=recipient_email,
        subject=subject,
        contents=contents
    )
    yag.close()
@app.route('/')
def index():
    return render_template('noti.html')

@app.route('/send-test-notification', methods=['GET'])
def send_test_notification_route():
    # Send test notification email
    sender_email = '2k21cse152@kiot.ac.in'
    sender_password = 'kiot1234@'
    recipient_email = '2k21cse092@kiot.ac.in'
    subject = 'Test Notification'
    contents = 'You can now take the test. Good luck!'
    send_test_notification(sender_email, sender_password, recipient_email, subject, contents)
    return 'Test notification email sent successfully!'

if __name__ == '__main__':
    app.run(debug=True)
