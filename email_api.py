from flask import Flask, request, jsonify
import smtplib
from email.message import EmailMessage
import os

app = Flask(__name__)

# --- Email and App Configuration (All variables at the top) ---
# It's highly recommended to use environment variables for sensitive data
# Example: os.environ.get('EMAIL_ADDRESS')
# export EMAIL_ADDRESS='your_email@gmail.com'
# export EMAIL_PASSWORD='your_app_password'

EMAIL_ADDRESS = "madhur.ahlawat17@gmail.com"
EMAIL_PASSWORD = "ghat dpaz iyps nztm"

RESUME_PATH = "Madhur_Ahlawat.pdf"

# --- Job Application Email Details ---
EMAIL_SUBJECT_JOB_APP = "Android Developer with 5 yr exp (exBharatPe, PVR Cinemas, OICL)"
EMAIL_BODY_JOB_APP = """\
Total experience: 5.7 years
Relevant experience: Same
Primary skills: Java/Kotlin, MVVM, Coroutines, Flows, Jetpack Compose, Dagger/Hilt
Notice period: Immediate Joiner
LWD (If applicable): 23rd July
Current location: Gurugram
Preferred location: Any
Are you open to work from Office 5 days a week: Yes
Current CTC: 13 LPA
Offer in hand: No, Just started looking for job.
Expected CTC: 15 LPA
Current company: BharatPe (payroll Sunday Labs)
Updated resume: Attached
Reason for change: Sunday Labs contract over with BharatPe client
"""

# --- Investor Pitch Email Details ---
EMAIL_SUBJECT_INVESTOR = "Seeking Angel Investment to become leading FinTech software solution provider"
EMAIL_BODY_INVESTOR = """\
I am an experienced Software Engineer (Android) with 6 years of professional tech-savvy experience and over 15 years of expertise working across Windows, Linux, macOS, and a wide range of devices. Technology has been my passion throughout, and now I am building a FinTech-focused software company.

I have worked with leading clients such as Physics Wallah, PVR Cinemas(Conduent) and FinTech giants like PhonePe and Stashfin.

My expertise covers the end-to-end FinTech ecosystem software, including:

Websites & Portals
Comprehensive web platforms providing access to all services and administrative functions

Corporate Website
Official corporate website showcasing products and services. Features responsive design, SEO optimization, and comprehensive product information.

Money Services Portal
Consumer-facing money services portal for payments and accounts. Provides account management, transaction history, and service access.

Extended Product Website
Extended product website highlighting comprehensive offerings. Features detailed product comparisons, pricing, and integration guides.

Lending Website
Website dedicated to the P2P lending details. Includes investment calculators, risk assessments, and portfolio tools.

Credit and BNPL Web Portal
PostPe product portal offering credit and BNPL services. Features credit applications, account management, and payment tracking.

Merchant Dashboard
Merchant portal to view settlements, transactions, and reports. Provides comprehensive analytics, financial insights, and business tools.

Loan Dashboard
Loan tracking dashboard for repayments, approvals, and balances. Features automated notifications, payment scheduling, and account management.

Bank Portal
Bank portal for transaction and settlement tracking. Includes real-time reporting, compliance monitoring, and automated reconciliation.

Devices & POS
Advanced payment devices and point-of-sale solutions for seamless merchant experiences

Swipe API
APIs enabling Swipe device transactions. Supports multiple card types, EMV compliance, and real-time processing with comprehensive error handling.

Swipe V2
Upgraded card swipe POS device with faster processing. Features enhanced security, contactless payments, and improved user interface.

Swipe CRM Backend
Backend system managing swipe device customers and merchants. Includes device provisioning, support ticketing, and performance monitoring.

Swipe Switch
Service for transaction routing on swipe devices. Handles intelligent routing, failover mechanisms, and cost optimization.

Smart Speaker V2
Smart audio speaker confirming payments with real-time voice alerts. Features multi-language support, customizable alerts, and voice recognition.

POS Terminal Series
POS terminal devices supporting card and QR transactions. Includes receipt printing, inventory management, and comprehensive reporting.

Internal Tools
Comprehensive suite of internal tools for operations, customer service, and business management

CRM Backend Java
Backend infrastructure for customer relationship management. Handles customer data, interaction tracking, and automated workflows.

CRM Frontend React
React-based frontend for CRM dashboards and agents. Features real-time updates, customizable workflows, and comprehensive reporting.

Call Centre
Internal tool to manage merchant and customer queries efficiently. Includes ticket routing, knowledge base, and performance analytics.

Insurance Hub
Central hub for insurance-related documentation and services. Features policy management, claims processing, and partner integrations.

Inventory Management
Tracks and manages device and product inventory. Includes automated reordering, warehouse management, and supply chain optimization.

App Review Bot
Automated system for reviewing and testing app releases. Features automated testing, performance monitoring, and quality assurance.

DevOps Self-Service
Self-service infrastructure automation tool for engineers. Includes deployment pipelines, monitoring setup, and resource provisioning.

Infrastructure as Code
Infrastructure-as-Code templates for scaling cloud infrastructure. Features automated deployments, cost optimization, and security compliance.

Data, AI & Fraud
Advanced artificial intelligence and machine learning systems for fraud detection and business intelligence

ML Server
Central ML server hosting production-ready models. Features model versioning, A/B testing, and real-time inference capabilities.

AI Falcon
ML/AI pipeline for rapid deployment of fraud detection models. Includes automated model training, validation, and deployment workflows.

Vision AI
Computer vision service for document/KYC validation. Features OCR, document verification, and identity authentication capabilities.

Image Deduplication
AI system detecting duplicate or fraudulent images. Uses advanced computer vision algorithms for similarity detection and fraud prevention.

Fraud Risk Management
Fraud risk management system detecting anomalies and fraud patterns. Features real-time scoring, rule engines, and machine learning models.

Credit Score Engine
Proprietary engine for calculating merchant and consumer credit scores. Uses alternative data sources and advanced analytics for accurate scoring.

Lending Analytics
Lending analytics platform for loan decision intelligence. Provides risk assessment, portfolio analysis, and predictive modeling.

Data Science Platform
General-purpose data science experimentation module. Features model development, data exploration, and collaborative research environment.

Additional Platform Components
Comprehensive suite of supporting services, utilities, and infrastructure components that power the entire ecosystem

API Gateway Services

Business Intelligence

Mobile SDKs

Integration Services

Development Tools

Reporting Tools

Marketing Automation

Banking Integrations

Search Services

Dashboard Services

Security Scanning

Workflow Engines

Design Systems

Push Notifications

Audit Logging

Performance Analytics

Form Builders

Real-time Analytics

Build Tools

Monitoring Tools

Security & Authentication

Web Services

Database Services

Analytics Platforms

Compliance Systems

Performance Monitoring

Communication APIs

Card Processing

Package Management

Automation Bots

Configuration Management

Documentation Tools

Metrics Collection

Link Management

File Management

System Utilities

Encryption Services

A/B Testing

Event Processing

Deployment Services

Data Visualization

I have developed the complete software and infrastructure required to serve a FinTech company including every layer of financial services, merchant solutions through mobile apps, web services and portals, POS devices, Internal business tools, AI-powered fraud prevention, and scalable infrastructure delivering seamless, secure, and innovative experiences for businesses and their customers.

My vision is to become a leading FinTech software solution provider, empowering both startups and enterprises with innovative financial technology. To scale and progress towards becoming a FinTech software provider, I am seeking initial seed funding, I would be happy to connect for a call for a more detailed discussion.

Thanks
Madhur Ahlawat
Linkedin: https://www.linkedin.com/in/madhur-ahlawat/
Phone & WhatsApp: +91-9958417372
"""

def send_email(recipient, subject, body, attachment_path=None):
    try:
        msg = EmailMessage()
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = recipient
        msg['Subject'] = subject
        msg.set_content(body)

        if attachment_path and os.path.exists(attachment_path):
            with open(attachment_path, 'rb') as f:
                msg.add_attachment(
                    f.read(),
                    maintype='application',
                    subtype='pdf',
                    filename=os.path.basename(attachment_path)
                )

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(msg)
            print(f"✅ Email sent to {recipient} with subject: '{subject}'")
        return True

    except Exception as e:
        print(f"❌ Failed to send email to {recipient}: {e}")
        return False

# --- Flask Routes ---

@app.route('/')
def home():
    return "Email sender service is up and running!"

@app.route('/send', methods=['GET'])
def send_job_application_emails():
    """Route to send job application emails with a resume attachment."""
    emails_param = request.args.get('emails')
    if not emails_param:
        return jsonify({"error": "Missing 'emails' query parameter"}), 400

    emails = [e.strip() for e in emails_param.split(',') if e.strip()]
    failed = []

    for email in emails:
        # Use the reusable send_email function with job application details
        success = send_email(
            recipient=email,
            subject=EMAIL_SUBJECT_JOB_APP,
            body=EMAIL_BODY_JOB_APP,
            attachment_path=RESUME_PATH
        )
        if not success:
            failed.append(email)

    return jsonify({
        "status": "Completed",
        "success": [e for e in emails if e not in failed],
        "failed": failed
    }), 200

@app.route('/sendToInvestor', methods=['GET'])
def send_investor_pitch_emails():
    emails_param = request.args.get('emails')
    if not emails_param:
        return jsonify({"error": "Missing 'emails' query parameter"}), 400

    emails = [e.strip() for e in emails_param.split(',') if e.strip()]
    failed = []

    for email in emails:
        # Use the reusable send_email function with investor pitch details
        success = send_email(
            recipient=email,
            subject=EMAIL_SUBJECT_INVESTOR,
            body=EMAIL_BODY_INVESTOR,
            attachment_path=None # Explicitly set to None
        )
        if not success:
            failed.append(email)

    return jsonify({
        "status": "Completed",
        "success": [e for e in emails if e not in failed],
        "failed": failed
    }), 200

if __name__ == '__main__':
    app.run(debug=True)