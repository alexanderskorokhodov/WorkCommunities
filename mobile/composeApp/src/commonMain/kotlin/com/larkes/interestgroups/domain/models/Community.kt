package com.larkes.interestgroups.domain.models

data class Community(
    val id: String,
    val image: String,
    val logo: String,
    val highlight: List<String>,
    val title: String,
    val isNew: Boolean,
    val subtitle: String? = null,
    val participents: Int? = null
)