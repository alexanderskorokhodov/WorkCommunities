package com.larkes.interestgroups.presentation.login.models

import com.larkes.interestgroups.data.dto.StatusDTO

data class AboutMeUIState(
    val name: String = "",
    val skills: List<String> = listOf(),
    val status: List<String> = listOf(),
    val aboutMe: String = "",
    val portfolio: String = "",
    val isClickAvailable: Boolean = false,
    val skillsOptions: List<SkillModel>? = null,
    val statuesOptions: List<StatusDTO>? = null
)