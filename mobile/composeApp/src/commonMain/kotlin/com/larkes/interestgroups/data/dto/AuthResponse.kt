package com.larkes.interestgroups.data.dto

import kotlinx.serialization.Serializable

@Serializable
data class AuthResponse(
    val access_token: String,
    val token_type: String
)