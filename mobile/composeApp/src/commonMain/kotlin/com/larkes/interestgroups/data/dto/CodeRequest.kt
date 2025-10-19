package com.larkes.interestgroups.data.dto

import kotlinx.serialization.Serializable

@Serializable
data class CodeRequest(
    val phone: String,
    val code: String
)