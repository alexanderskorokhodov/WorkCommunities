package com.larkes.interestgroups.data.dto

import kotlinx.serialization.Serializable


typealias PostListResponse = List<PostDto>

@Serializable
data class PostDto(
    val id: String,
    val community_id: String,
    val title: String,
    val body: String?,
    val media: List<MediaDto> = emptyList(),
    val tags: List<String> = emptyList(),
    val skills: List<CategoryDto> = emptyList(),
    val cost: Int?,
    val participant_payout: Int?
)

@Serializable
data class CategoryDto(
    val id: String,
    val title: String,
    val sphere_id: String,
    val sphere: SphereCatDto?
)

@Serializable
data class SphereCatDto(
    val id: String,
    val title: String,
    val background_color: String,
    val text_color: String
)

@Serializable
data class MediaDto(
    val id: String,
    val kind: String,
    val mime: String,
    val ext: String,
    val size: Long,
    val url: String
)
