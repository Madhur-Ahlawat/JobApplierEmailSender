# Job Applier Email Sender - Kotlin

A Spring Boot application for sending job application emails and investor pitch emails.

## Prerequisites

- Java 17 or higher
- Gradle 8.5 or higher (or use the included Gradle wrapper)

## Environment Variables

Set the following environment variables before running:

```bash
export recipient_email=your_recipient@email.com
export sender_email=your_sender@gmail.com
export gmail_app_password=your_16_digit_app_password
```

## Building

```bash
./gradlew build
```

## Running

```bash
./gradlew bootRun
```

Or build and run the JAR:

```bash
./gradlew bootJar
java -jar build/libs/JobApplierEmailSender-1.0.0.jar
```

## API Endpoints

### Health Check
- `GET /` - Returns "Email sender service is up and running!"
- `GET /isOnline` - Returns JSON status

### Email Endpoints
- `GET /sendJobApplicationEmails?emails=email1@example.com,email2@example.com` - Send job application emails with resume attachment
- `GET /sendInvestorPitchEmails?emails=email1@example.com,email2@example.com` - Send investor pitch emails
- `GET /getFailedEmails` - Get list of bounced/failed email addresses
- `GET /contactUs?full_name=...&country_code=...&phone_number=...&email_address=...&contactus_message=...` - Contact form submission

## Deployment on Render

The application is configured for deployment on Render.com. See `render.yaml` for configuration.

## Project Structure

```
src/main/kotlin/com/madhur/emailsender/
├── Application.kt                 # Main application entry point
├── config/
│   └── EmailConfig.kt             # Email configuration
├── controller/
│   └── EmailController.kt         # REST API endpoints
├── model/
│   ├── ApiResponse.kt             # Response data classes
│   └── EmailTemplates.kt          # Email templates
└── service/
    ├── EmailService.kt            # Email sending service
    └── FailedEmailService.kt      # Bounced email detection service
```

