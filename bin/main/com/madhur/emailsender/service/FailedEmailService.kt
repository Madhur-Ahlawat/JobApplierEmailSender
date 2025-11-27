package com.madhur.emailsender.service

import com.madhur.emailsender.config.EmailConfig
import org.springframework.stereotype.Service
import java.util.*
import javax.mail.Folder
import javax.mail.Session
import javax.mail.internet.MimeMultipart

@Service
class FailedEmailService(private val emailConfig: EmailConfig) {
    
    private val emailRegex = Regex("[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}")
    
    fun getFailedEmails(): List<String> {
        val failedEmails = mutableSetOf<String>()
        var store: javax.mail.Store? = null
        var inbox: javax.mail.Folder? = null
        
        try {
            val properties = Properties().apply {
                put("mail.store.protocol", "imaps")
                put("mail.imaps.host", emailConfig.imapServer)
                put("mail.imaps.port", "993")
                put("mail.imaps.ssl.enable", "true")
            }
            
            val session = Session.getInstance(properties)
            store = session.getStore("imaps")
            store.connect(emailConfig.imapServer, emailConfig.recipientEmail, emailConfig.gmailAppPassword)
            
            inbox = store.getFolder("INBOX")
            inbox.open(Folder.READ_ONLY)
            
            // Search for bounced emails from mailer-daemon
            val messages = inbox.messages
            
            println("Searching through ${messages.size} messages for bounced emails...")
            
            for (message in messages) {
                try {
                    val from = message.from?.firstOrNull()?.toString() ?: ""
                    
                    // Check if from mailer-daemon
                    if (from.contains("mailer-daemon", ignoreCase = true)) {
                        val body = getTextFromMessage(message)
                        
                        // Check if it contains "Address not found"
                        if (body.contains("Address not found", ignoreCase = true)) {
                            // Extract email address from body
                            val match = emailRegex.find(body)
                            if (match != null) {
                                failedEmails.add(match.value)
                            }
                        }
                    }
                } catch (e: Exception) {
                    // Continue processing other messages
                    continue
                }
            }
            
            println("Found ${failedEmails.size} bounced emails. Processing...")
            return failedEmails.toList()
            
        } catch (e: Exception) {
            println("An error occurred: ${e.message}")
            return emptyList()
        } finally {
            try {
                inbox?.close(false)
                store?.close()
                println("Connection closed.")
            } catch (e: Exception) {
                // Ignore close errors
            }
        }
    }
    
    private fun getTextFromMessage(message: javax.mail.Message): String {
        return try {
            when (val content = message.content) {
                is String -> content
                is MimeMultipart -> getTextFromMimeMultipart(content)
                else -> ""
            }
        } catch (e: Exception) {
            ""
        }
    }
    
    private fun getTextFromMimeMultipart(mimeMultipart: MimeMultipart): String {
        val result = StringBuilder()
        for (i in 0 until mimeMultipart.count) {
            val bodyPart = mimeMultipart.getBodyPart(i)
            if (bodyPart.isMimeType("text/plain")) {
                result.append(bodyPart.content.toString())
            } else if (bodyPart.content is MimeMultipart) {
                result.append(getTextFromMimeMultipart(bodyPart.content as MimeMultipart))
            }
        }
        return result.toString()
    }
}
