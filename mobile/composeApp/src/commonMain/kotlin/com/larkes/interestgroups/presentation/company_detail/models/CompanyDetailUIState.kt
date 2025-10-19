package com.larkes.interestgroups.presentation.company_detail.models

import com.larkes.interestgroups.domain.models.Community
import com.larkes.interestgroups.domain.models.CompanyDetail

data class CompanyDetailUIState(
    val company: CompanyDetail? = null,
    val communities: List<Community>? = null,
    val isCompanyLoading: Boolean = true,
    val isCommunityLoading: Boolean = true
)