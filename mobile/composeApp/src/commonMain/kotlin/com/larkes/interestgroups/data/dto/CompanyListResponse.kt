package com.larkes.interestgroups.data.dto

import kotlinx.serialization.Serializable

typealias CompanyListResponse = List<CompanyDto>

@Serializable
data class CompanyDto(
    val id: String,
    val name: String,
    val description: String?,
    val logo_media_id: String,
    val skills: List<CategoryDto>
)