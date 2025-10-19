package com.larkes.interestgroups.data.dto

import kotlinx.serialization.Serializable

typealias EventListResponse = List<EventDto>

@Serializable
data class EventDto(
    val id: String,
    val community_id: String,
    val title: String,
    val event_date: String, // переименовано с starts_at на event_date
    val city: String?,
    val location: String?,
    val description: String?,
    val registration: String?,
    val format: String?,
    val media_id: String,
    val tags: List<String> = emptyList(),
    val skills: List<CategoryDto> = emptyList(),
    val cost: Int?,
    val participant_payout: Int?
)
