package com.larkes.interestgroups.domain.models

data class Event(
    val image: String,
    val date: String,
    val highlight: List<String>,
    val title: String
)