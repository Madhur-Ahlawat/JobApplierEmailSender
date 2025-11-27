package com.madhur.emailsender.controller

import com.madhur.emailsender.config.EmailConfig
import com.madhur.emailsender.model.ContactUsResponse
import com.madhur.emailsender.model.EmailResponse
import com.madhur.emailsender.model.EmailTemplates
import com.madhur.emailsender.model.OnlineResponse
import com.madhur.emailsender.service.EmailService
import com.madhur.emailsender.service.FailedEmailService
import org.springframework.http.HttpStatus
import org.springframework.http.MediaType
import org.springframework.http.ResponseEntity
import org.springframework.web.bind.annotation.GetMapping
import org.springframework.web.bind.annotation.RequestParam
import org.springframework.web.bind.annotation.RestController

@RestController
class EmailController(
    private val emailService: EmailService,
    private val failedEmailService: FailedEmailService,
    private val emailConfig: EmailConfig
) {
    
    @GetMapping("/")
    fun home(): String {
        return "Email sender service is up and running!"
    }
    
    @GetMapping("/isOnline")
    fun isOnline(): ResponseEntity<OnlineResponse> {
        return ResponseEntity.ok(
            OnlineResponse(
                status = "Completed",
                success = "Server is running!",
                failed = false
            )
        )
    }
    
    @GetMapping("/sendJobApplicationEmails")
    fun sendJobApplicationEmails(@RequestParam emails: String?): ResponseEntity<EmailResponse> {
        if (emails.isNullOrBlank()) {
            return ResponseEntity.badRequest().body(
                EmailResponse(
                    status = "Error",
                    error = "Missing 'emails' query parameter"
                )
            )
        }
        
        val emailList = emails.split(",").map { it.trim() }.filter { it.isNotBlank() }
        val failed = mutableListOf<String>()
        
        for (email in emailList) {
            val success = emailService.sendEmail(
                recipient = email,
                subject = EmailTemplates.EMAIL_SUBJECT_JOB_APP,
                body = EmailTemplates.EMAIL_BODY_JOB_APP,
                attachmentPath = emailConfig.resumePath
            )
            if (!success) {
                failed.add(email)
            }
        }
        
        return ResponseEntity.ok(
            EmailResponse(
                status = "Completed",
                success = emailList.filter { it !in failed },
                failed = failed
            )
        )
    }
    
    @GetMapping("/getFailedEmails", produces = [MediaType.TEXT_PLAIN_VALUE])
    fun getFailedEmails(): ResponseEntity<String> {
        val bouncedList = failedEmailService.getFailedEmails()
        
        return if (bouncedList.isNotEmpty()) {
            val commaSeparatedList = bouncedList.joinToString(",")
            println("\n--- Comma-Separated List of Failed Emails ---")
            ResponseEntity.ok(commaSeparatedList)
        } else {
            ResponseEntity.status(HttpStatus.NOT_FOUND)
                .body("Could not find or extract any failed email addresses.")
        }
    }
    
    @GetMapping("/sendInvestorPitchEmails")
    fun sendInvestorPitchEmails(@RequestParam emails: String?): ResponseEntity<EmailResponse> {
        if (emails.isNullOrBlank()) {
            return ResponseEntity.badRequest().body(
                EmailResponse(
                    status = "Error",
                    error = "Missing 'emails' query parameter"
                )
            )
        }
        
        val emailList = emails.split(",").map { it.trim() }.filter { it.isNotBlank() }
        val failed = mutableListOf<String>()
        
        for (email in emailList) {
            val success = emailService.sendEmail(
                recipient = email,
                subject = EmailTemplates.EMAIL_SUBJECT_INVESTOR,
                body = EmailTemplates.EMAIL_BODY_INVESTOR,
                attachmentPath = null
            )
            if (!success) {
                failed.add(email)
            }
        }
        
        return ResponseEntity.ok(
            EmailResponse(
                status = "Completed",
                success = emailList.filter { it !in failed },
                failed = failed
            )
        )
    }
    
    @GetMapping("/contactUs")
    fun contactUs(
        @RequestParam("full_name") fullName: String?,
        @RequestParam("country_code") countryCode: String?,
        @RequestParam("phone_number") phoneNumber: String?,
        @RequestParam("email_address") emailAddress: String?,
        @RequestParam("contactus_message") contactUsMessage: String?
    ): ResponseEntity<ContactUsResponse> {
        
        // Validate required parameters
        if (fullName.isNullOrBlank()) {
            return ResponseEntity.badRequest().body(
                ContactUsResponse(status = "error", message = "Missing 'full_name' query parameter")
            )
        }
        if (countryCode.isNullOrBlank()) {
            return ResponseEntity.badRequest().body(
                ContactUsResponse(status = "error", message = "Missing 'country_code' query parameter")
            )
        }
        if (phoneNumber.isNullOrBlank()) {
            return ResponseEntity.badRequest().body(
                ContactUsResponse(status = "error", message = "Missing 'phone_number' query parameter")
            )
        }
        if (emailAddress.isNullOrBlank()) {
            return ResponseEntity.badRequest().body(
                ContactUsResponse(status = "error", message = "Missing 'email_address' query parameter")
            )
        }
        if (contactUsMessage.isNullOrBlank()) {
            return ResponseEntity.badRequest().body(
                ContactUsResponse(status = "error", message = "Missing 'contactus_message' query parameter")
            )
        }
        
        // Format email body for recipient
        val recipient = emailConfig.recipientEmail
        val subject = "$fullName contacted you!"
        val body = """
            |Contact Form Submission
            |
            |Name: $fullName
            |Country Code: $countryCode
            |Phone Number: $phoneNumber
            |Email: $emailAddress
            |
            |Message:
            |$contactUsMessage
        """.trimMargin()
        
        // Send email to recipient
        val successRecipient = emailService.sendEmail(
            recipient = recipient,
            subject = subject,
            body = body,
            attachmentPath = null
        )
        
        // Format confirmation email body for submitter
        val confirmationSubject = "Thank you for contacting us!"
        val confirmationBody = """
            |Dear $fullName,
            |
            |Thank you for reaching out to us. We have received your message and will get back to you soon!
            |
            |Here's a copy of your submission:
            |
            |Name: $fullName
            |Country Code: $countryCode
            |Phone Number: $phoneNumber
            |Email: $emailAddress
            |
            |Message:
            |$contactUsMessage
            |
            |Best regards,
            |Rythm Audio Team
        """.trimMargin()
        
        // Send confirmation email to submitter
        val successSubmitter = emailService.sendEmail(
            recipient = emailAddress,
            subject = confirmationSubject,
            body = confirmationBody,
            attachmentPath = null
        )
        
        // Return response based on both email results
        return when {
            successRecipient && successSubmitter -> {
                ResponseEntity.ok(
                    ContactUsResponse(
                        status = "success",
                        message = "Emails sent successfully to $recipient and $emailAddress"
                    )
                )
            }
            successRecipient -> {
                ResponseEntity.status(207).body(
                    ContactUsResponse(
                        status = "partial_success",
                        message = "Email sent to $recipient, but failed to send confirmation to $emailAddress"
                    )
                )
            }
            successSubmitter -> {
                ResponseEntity.status(207).body(
                    ContactUsResponse(
                        status = "partial_success",
                        message = "Confirmation sent to $emailAddress, but failed to send email to $recipient"
                    )
                )
            }
            else -> {
                ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(
                    ContactUsResponse(
                        status = "error",
                        message = "Failed to send emails"
                    )
                )
            }
        }
    }
}

