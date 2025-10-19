package com.larkes.interestgroups.presentation.company_communities

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.larkes.interestgroups.data.dto.CompanyCommunityItemDto
import com.larkes.interestgroups.domain.repository.CompanyRepository
import com.larkes.interestgroups.utils.Resource
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.launchIn
import kotlinx.coroutines.flow.onEach


class CompanyCommunitiesViewModel(
    private val companyRepository: CompanyRepository
): ViewModel(){

    val _communities = MutableStateFlow<List<CompanyCommunityItemDto>>(listOf())
    val _isLoading = MutableStateFlow(true)

    init {

        companyRepository.fetchCompanyCommunities().onEach { res ->
            when(res){
                is Resource.Success -> {
                    res.data?.let { communities ->
                        _communities.value = communities
                    }
                    _isLoading.value = false
                }
                is Resource.Error -> {

                }
            }
        }.launchIn(viewModelScope)

    }


}