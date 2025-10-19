package com.larkes.interestgroups.data.dto

import kotlinx.serialization.Serializable


@Serializable
data class CompanyRegRequest(
    val email: String,
    val password: String,
    val name: String
)