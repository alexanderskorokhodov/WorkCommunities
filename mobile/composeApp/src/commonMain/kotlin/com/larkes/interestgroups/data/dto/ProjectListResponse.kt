package com.larkes.interestgroups.data.dto

import kotlinx.serialization.Serializable


typealias ProjectListResponse = List<ProjectDto>

@Serializable
data class ProjectDto(
    val id: String,
    val name: String,
    val company_id: String,
    val description: String,
    val telegram_url: String?,
    val tags: List<String>,
    val is_archived: Boolean,
    val logo_media_id: String,
    val members_count: String?
)

@Serializable
data class CommunityWithDetailsDto(
    val id: String,
    val name: String,
    val company_id: String,
    val description: String,
    val telegram_url: String?,
    val tags: List<String>,
    val is_archived: Boolean,
    val logo_media_id: String,
    val members_count: Int?,
    val cases: List<CommunityCaseDto>,
    val members: List<CommunityMemberDto>
)

@Serializable
data class CommunityCaseDto(
    val id: String,
    val community_id: String,
    val title: String,
    val description: String,
    val date: String, // или используйте Instant/kotlinx.datetime.Instant
    val solutions_count: Int
)

@Serializable
data class CommunityMemberDto(
    val id: String,
    val role: String,
    val phone: String? = null,
    val full_name: String? = null,
    val avatar_media_id: String? = null,
    val created_at: String // или используйте Instant/kotlinx.datetime.Instant
)
