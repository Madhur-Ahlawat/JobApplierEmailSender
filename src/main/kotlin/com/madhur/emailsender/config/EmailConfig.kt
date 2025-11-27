package com.madhur.emailsender.config

import org.springframework.beans.factory.annotation.Value
import org.springframework.context.annotation.Configuration

@Configuration
class EmailConfig {
    
    @Value("\${email.recipient:madhur.aws17@gmail.com}")
    lateinit var recipientEmail: String
    
    @Value("\${email.sender:#{systemEnvironment['sender_email'] ?: ''}}")
    lateinit var senderEmail: String
    
    @Value("\${email.password:vymz jmda rbuj dyho}")
    lateinit var gmailAppPassword: String
    
    @Value("\${email.imap.server:imap.gmail.com}")
    lateinit var imapServer: String
    
    @Value("\${email.resume.path:assets/Madhur_Ahlawat_Android.docx}")
    lateinit var resumePath: String
}

