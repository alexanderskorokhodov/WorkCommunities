package com.larkes.interestgroups.data.dto

import kotlinx.serialization.Serializable

@Serializable
data class UserProfileDto(
    val id: String,
    val role: String,
    val phone: String?,
    val full_name: String,
    val portfolio_url: String?,
    val description: String,
    val skills: List<CategoryDto>,
    val statuses: List<UserStatusDto>,
    val avatar_media_id: String?,
    val created_at: String, // или используйте Instant/kotlinx.datetime.Instant
    val communities: List<CommunityShortDto>
)

@kotlinx.serialization.Serializable
data class UserStatusDto(
    val id: String,
    val title: String
)

@kotlinx.serialization.Serializable
data class CommunityShortDto(
    val id: String,
    val name: String,
    val company_id: String,
    val description: String,
    val telegram_url: String?,
    val tags: List<String>,
    val is_archived: Boolean,
    val logo_media_id: String
)