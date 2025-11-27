package com.madhur.emailsender.model

data class EmailResponse(
    val status: String,
    val success: List<String>? = null,
    val failed: List<String>? = null,
    val message: String? = null,
    val error: String? = null
)

data class OnlineResponse(
    val status: String,
    val success: String,
    val failed: Boolean
)

data class ContactUsResponse(
    val status: String,
    val message: String
)

