package com.larkes.interestgroups.domain.models

data class Company(
    val id: String,
    val image: String,
    val logo: String,
    val highlight: List<String>,
    val title: String
)