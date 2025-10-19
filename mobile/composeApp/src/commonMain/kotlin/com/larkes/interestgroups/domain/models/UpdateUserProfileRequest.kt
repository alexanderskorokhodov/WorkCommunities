package com.larkes.interestgroups.domain.models

import kotlinx.serialization.Serializable

@Serializable
data class UpdateUserProfileRequest(
    val full_name: String? = null,
    val portfolio_url: String? = null,
    val description: String? = null,
    val skill_uids: List<String>? = null,
    val status_uids: List<String>? = null
)