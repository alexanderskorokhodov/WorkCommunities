package com.larkes.interestgroups.data.dto

import kotlinx.serialization.Serializable

typealias GroupListResponse = List<GroupDto>

@Serializable
data class GroupDto(
    val id: String,
    val title: String,
    val sphere: SphereDto
)

@Serializable
data class SphereDto(
    val id: String,
    val title: String,
    val background_color: String,
    val text_color: String
)