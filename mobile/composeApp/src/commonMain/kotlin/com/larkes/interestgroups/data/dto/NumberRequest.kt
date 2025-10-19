package com.larkes.interestgroups.data.dto

import kotlinx.serialization.Serializable

@Serializable
data class NumberRequest(
    val phone: String
)