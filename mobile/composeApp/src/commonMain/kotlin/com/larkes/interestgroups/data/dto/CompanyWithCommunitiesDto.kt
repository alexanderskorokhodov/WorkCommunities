package com.larkes.interestgroups.data.dto

import kotlinx.serialization.Serializable

@kotlinx.serialization.Serializable
data class CompanyWithCommunitiesDto(
    val id: String,
    val name: String,
    val description: String,
    val logo_media_id: String,
    val skills: List<CategoryDto>,
    val communities: List<CommunityDto>
)

@Serializable
data class CommunityDto(
    val id: String,
    val name: String,
    val company_id: String,
    val description: String,
    val telegram_url: String?,
    val tags: List<String>,
    val is_archived: Boolean,
    val logo_media_id: String
)