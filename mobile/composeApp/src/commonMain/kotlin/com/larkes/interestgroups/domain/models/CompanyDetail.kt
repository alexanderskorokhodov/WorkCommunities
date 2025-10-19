package com.larkes.interestgroups.domain.models

data class CompanyDetail(
    val logo: String,
    val title: String,
    val images: List<String>,
    val about: String,
    val highlight: String,
)