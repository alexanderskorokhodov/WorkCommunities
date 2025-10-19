package com.larkes.interestgroups.presentation.main.models

import com.larkes.interestgroups.domain.models.Community
import com.larkes.interestgroups.domain.models.Company
import com.larkes.interestgroups.domain.models.Event
import com.larkes.interestgroups.domain.models.Post

data class MainUIState(
    val companies: List<Company> = listOf(),
    val isCompaniesLoading: Boolean = false,
    val posts: List<Post> = listOf(),
    val isPostLoading: Boolean = false,
    val communities: List<Community> = listOf(),
    val isCommunitiesLoading: Boolean = false,
    val events: List<Event> = listOf(),
    val isEventsLoading: Boolean = false,
)