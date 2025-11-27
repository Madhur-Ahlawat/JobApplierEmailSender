package com.madhur.emailsender.service

import com.madhur.emailsender.config.EmailConfig
import jakarta.activation.DataHandler
import jakarta.activation.FileDataSource
import jakarta.mail.*
import jakarta.mail.internet.InternetAddress
import jakarta.mail.internet.MimeBodyPart
import jakarta.mail.internet.MimeMessage
import jakarta.mail.internet.MimeMultipart
import org.springframework.stereotype.Service
import java.io.File
import java.util.*

@Service
class EmailService(private val emailConfig: EmailConfig) {
    
    fun sendEmail(
        recipient: String,
        subject: String,
        body: String,
        attachmentPath: String? = null
    ): Boolean {
        return try {
            val properties = Properties().apply {
                put("mail.smtp.auth", "true")
                put("mail.smtp.starttls.enable", "true")
                put("mail.smtp.ssl.enable", "true")
                put("mail.smtp.host", "smtp.gmail.com")
                put("mail.smtp.port", "465")
                put("mail.smtp.socketFactory.port", "465")
                put("mail.smtp.socketFactory.class", "javax.net.ssl.SSLSocketFactory")
            }
            
            val session = Session.getInstance(properties, object : Authenticator() {
                override fun getPasswordAuthentication(): PasswordAuthentication {
                    return PasswordAuthentication(emailConfig.senderEmail, emailConfig.gmailAppPassword)
                }
            })
            
            val message = MimeMessage(session).apply {
                setFrom(InternetAddress(emailConfig.senderEmail))
                setRecipients(Message.RecipientType.TO, InternetAddress.parse(recipient))
                setSubject(subject)
            }
            
            if (attachmentPath != null) {
                val file = File(attachmentPath)
                if (file.exists()) {
                    val multipart = MimeMultipart()
                    
                    // Text body part
                    val textPart = MimeBodyPart().apply {
                        setText(body)
                    }
                    multipart.addBodyPart(textPart)
                    
                    // Attachment part
                    val attachmentPart = MimeBodyPart().apply {
                        dataHandler = DataHandler(FileDataSource(file))
                        fileName = file.name
                    }
                    multipart.addBodyPart(attachmentPart)
                    
                    message.setContent(multipart)
                } else {
                    println(" Failed to attach file!")
                    message.setText(body)
                }
            } else {
                message.setText(body)
            }
            
            Transport.send(message)
            println(" Email sent to $recipient with subject: '$subject'")
            true
        } catch (e: Exception) {
            println(" Failed to send email to $recipient: ${e.message}")
            false
        }
    }
}

