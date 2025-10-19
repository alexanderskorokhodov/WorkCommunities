package com.larkes.interestgroups.data.dto

import kotlinx.serialization.Serializable

@kotlinx.serialization.Serializable
data class CompanyInfoDto(
    val id: String,
    val name: String,
    val description: String?,
    val logo_media_id: String?,
    val tags: List<String> = emptyList(),
    val communities: List<CompanyCommunityDto> = emptyList(),
    val media: List<String> = emptyList()
)

@Serializable
data class CompanyCommunityDto(
    val id: String, // d=f8e489f5d37c4ef2883519c47cf70ef6
    val company_id: String, // company_id=4137b453b0b7474aa19b921b37b7f63b
    val name: String, // ИИ и встраиваемые системы
    val logo_media_id: String // e7ff650f958943d9b722416f4597ce58
)