package com.madhur.emailsender.config

import org.springframework.beans.factory.annotation.Value
import org.springframework.context.annotation.Configuration

@Configuration
class EmailConfig {
    
    @Value("\${email.recipient:#{systemEnvironment['recipient_email'] ?: ''}}")
    lateinit var recipientEmail: String
    
    @Value("\${email.sender:#{systemEnvironment['sender_email'] ?: ''}}")
    lateinit var senderEmail: String
    
    @Value("\${email.password:#{systemEnvironment['gmail_app_password'] ?: ''}}")
    lateinit var gmailAppPassword: String
    
    @Value("\${email.imap.server:imap.gmail.com}")
    lateinit var imapServer: String
    
    @Value("\${email.resume.path:assets/Madhur_Ahlawat_Android_FinTech.docx}")
    lateinit var resumePath: String
}

