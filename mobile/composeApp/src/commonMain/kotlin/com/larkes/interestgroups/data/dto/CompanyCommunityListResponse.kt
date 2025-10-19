package com.larkes.interestgroups.data.dto

import kotlinx.serialization.Serializable

typealias CompanyCommunityListResponse = List<CompanyCommunityItemDto>

@Serializable
data class CompanyCommunityItemDto(
    val id: String,
    val name: String,
    val company_id: String,
    val description: String,
    val telegram_url: String?,
    val tags: List<String>,
    val is_archived: Boolean,
    val logo_media_id: String,
    val members_count: Int?
)