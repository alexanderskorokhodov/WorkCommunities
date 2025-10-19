package com.larkes.interestgroups.presentation.company_community_detail

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.larkes.interestgroups.data.dto.CommunityWithDetailsDto
import com.larkes.interestgroups.domain.repository.CommunitiesRepository
import com.larkes.interestgroups.domain.repository.CompanyRepository
import com.larkes.interestgroups.utils.Resource
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.launchIn
import kotlinx.coroutines.flow.onEach
import kotlinx.coroutines.launch

class CompanyCommunityDetailViewModel(
    private val communityRepository: CommunitiesRepository
): ViewModel() {

    val _community = MutableStateFlow<CommunityWithDetailsDto?>(null)

    fun getCommunity(id: String){
        viewModelScope.launch {
            communityRepository.fetchCommunity(id).onEach { res ->
                when(res){
                    is Resource.Success -> {
                        res.data?.let {
                            _community.value = it
                        }
                    }
                    is Resource.Error -> {

                    }
                }
            }.launchIn(this)
        }
    }

}