package com.larkes.interestgroups.presentation.login.models

data class CreateProfileUIState(
    val number: String = "",
    val isLoading: Boolean = false,
    val error: String = ""
)