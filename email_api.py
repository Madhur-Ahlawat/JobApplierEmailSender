from flask import Flask, request, jsonify
import smtplib
from email.message import EmailMessage

app = Flask(__name__)

# Your email config
EMAIL_ADDRESS = "madhur.ahlawat17@gmail.com"
EMAIL_PASSWORD = "qnwu rreg yoqh fzme"
RESUME_PATH = "Madhur_Ahlawat.pdf"
EMAIL_SUBJECT = "Android Developer with 5 yr exp (exBharatPe, PVR Cinemas, OICL)"
EMAIL_BODY = """\
Total experience: 5.7 years
Relevant experience: Same
Primary skills(top3): Java/Kotlin, MVVM, Jetpack Compose, Dagger/Hilt
Notice period: Immediate Joiner
LWD (If applicable): 18th July
Current location: Gurugram
Preferred location: Any
Are you open to work from Office 5 days a week: (Yes/No) Yes
Current CTC: 13 LPA
Offer in hand: 1st round at Samsung is clear, waiting for panel to get available
Expected CTC: As per company norms
Current company: BharatPe (payroll Sunday Labs)
Updated resume: Attached
Reason for change: Sunday Labs contract over with BharatPe client
"""

@app.route('/send', methods=['GET'])
def send_email():
    emails_param = request.args.get('emails')  # Get 'emails' from query param
    if not emails_param:
        return jsonify({"error": "Missing 'emails' query parameter"}), 400

    # Split by comma, strip whitespace
    emails = [email.strip() for email in emails_param.split(',') if email.strip()]

    for email in emails:
        # Call your email sending logic here
        print(f"Sending email to: {email}")
        # send_email_function(email)

    return jsonify({"status": "Emails sent", "recipients": emails}), 200

if __name__ == '__main__':
    app.run()