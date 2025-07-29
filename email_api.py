from flask import Flask, request, jsonify
import smtplib
from email.message import EmailMessage
import os

app = Flask(__name__)

# Email configuration
EMAIL_ADDRESS = "madhur.ahlawat17@gmail.com"
EMAIL_PASSWORD = "qnwu rreg yoqh fzme"  # App password, not your real Gmail password
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

def send_email_function(recipient):
    """Function to send email with resume attachment"""
    try:
        msg = EmailMessage()
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = recipient
        msg['Subject'] = EMAIL_SUBJECT
        msg.set_content(EMAIL_BODY)

        # Attach resume if it exists
        if os.path.exists(RESUME_PATH):
            with open(RESUME_PATH, 'rb') as f:
                msg.add_attachment(
                    f.read(),
                    maintype='application',
                    subtype='pdf',
                    filename=RESUME_PATH
                )

        # Connect to Gmail SMTP server and send
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(msg)

        print(f"✅ Email sent to {recipient}")
        return True

    except Exception as e:
        print(f"❌ Failed to send email to {recipient}: {e}")
        return False


@app.route('/send', methods=['GET'])
def send_email():
    emails_param = request.args.get('emails')  # Get 'emails' from query param
    if not emails_param:
        return jsonify({"error": "Missing 'emails' query parameter"}), 400

    # Split by comma, strip whitespace
    emails = [email.strip() for email in emails_param.split(',') if email.strip()]
    failed = []

    for email in emails:
        success = send_email_function(email)
        if not success:
            failed.append(email)

    return jsonify({
        "status": "Completed",
        "success": [e for e in emails if e not in failed],
        "failed": failed
    }), 200


if __name__ == '__main__':
    app.run(debug=True)