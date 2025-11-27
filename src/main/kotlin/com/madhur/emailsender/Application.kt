package com.madhur.emailsender

import org.springframework.boot.autoconfigure.SpringBootApplication
import org.springframework.boot.runApplication

@SpringBootApplication
class Application

fun main(args: Array<String>) {
    println("\n" + "=".repeat(80))
    println("ENVIRONMENT VARIABLES:")
    println("=".repeat(80))
    println("recipient_email = ${System.getenv("recipient_email") ?: "Not set"}")
    println("sender_email = ${System.getenv("sender_email") ?: "Not set"}")
    val maskedPassword = if (System.getenv("gmail_app_password") != null) "*".repeat(20) else "None"
    println("gmail_app_password = $maskedPassword")
    println("=".repeat(80))
    println("\nStarting Spring Boot server...\n")
    
    runApplication<Application>(*args)
}

