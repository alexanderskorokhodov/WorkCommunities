package com.larkes.interestgroups.presentation.company_profile.models

data class CompanyProfileUIState(
    val name: String = "",
    val description: String = "",
    val highlight: List<String> = listOf()
)