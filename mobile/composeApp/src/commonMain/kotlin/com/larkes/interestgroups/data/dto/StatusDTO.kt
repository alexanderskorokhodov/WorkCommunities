package com.larkes.interestgroups.data.dto

import kotlinx.serialization.Serializable

typealias StatusListResponse = List<StatusDTO>

@Serializable
data class StatusDTO(
    val id: String,
    val title: String
)