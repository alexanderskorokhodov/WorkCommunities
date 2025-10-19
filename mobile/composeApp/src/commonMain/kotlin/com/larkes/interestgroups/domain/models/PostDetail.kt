package com.larkes.interestgroups.domain.models

data class PostDetail(
    val id: String,
    val image: String,
    val title: String,
    val text: String,
    val date: String?,
    val format: String?,
    val registration: String?
)