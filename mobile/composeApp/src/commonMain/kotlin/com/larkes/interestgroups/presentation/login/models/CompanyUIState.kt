package com.larkes.interestgroups.presentation.login.models

data class CompanyUIState(
    val companyName: String = "",
    val description: String = "",
    val specialities: List<String> = listOf(),
    val isAvailable: Boolean = false,
    val isLoading: Boolean = true,
    val image: String? = null
)