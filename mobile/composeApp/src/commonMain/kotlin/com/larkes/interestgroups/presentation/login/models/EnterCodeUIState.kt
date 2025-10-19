package com.larkes.interestgroups.presentation.login.models

data class EnterCodeUIState(
    val number: String = "",
    val code: String = "",
    val isLoading: Boolean = false,
    val error: String = "",
    val repeatTime: Int = 40
)