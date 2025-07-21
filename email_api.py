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

def send_email(to_email):
    try:
        msg = EmailMessage()
        msg["Subject"] = EMAIL_SUBJECT
        msg["From"] = EMAIL_ADDRESS
        msg["To"] = to_email
        msg.set_content(EMAIL_BODY)

        with open(RESUME_PATH, "rb") as f:
            file_data = f.read()
            file_name = RESUME_PATH.split("/")[-1]
            msg.add_attachment(file_data, maintype="application", subtype="octet-stream", filename=file_name)

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(msg)

        return True, f"Email successfully sent to {to_email}"

    except Exception as e:
        return False, str(e)

@app.route("/send")
def send_email_api():
    to_email = request.args.get("email")
    if not to_email:
        return jsonify({"error": "Email query parameter is required"}), 400

    success, message = send_email(to_email)
    return jsonify({"success": success, "message": message})

if __name__ == "__main__":
    app.run(debug=True)