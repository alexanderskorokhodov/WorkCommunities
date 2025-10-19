package com.larkes.interestgroups.presentation.community_detail

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.larkes.interestgroups.data.dto.CommunityDto
import com.larkes.interestgroups.data.dto.CommunityWithDetailsDto
import com.larkes.interestgroups.data.dto.GroupDto
import com.larkes.interestgroups.data.dto.ProjectDto
import com.larkes.interestgroups.domain.repository.CommunitiesRepository
import com.larkes.interestgroups.utils.Resource
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.launchIn
import kotlinx.coroutines.flow.merge
import kotlinx.coroutines.flow.onEach

class CommunityDetailViewModel(
    private val communitiesRepository: CommunitiesRepository
): ViewModel() {

    val community = MutableStateFlow<CommunityWithDetailsDto?>(null)

    init {
    }

    fun subscribe(){
        community.value?.let {
            communitiesRepository.communitySubscribe(it.id).onEach {res ->
                when(res){
                    is Resource.Success -> {
                        res.data?.let {

                        }
                    }
                    is Resource.Error -> {

                    }
                }
            }.launchIn(viewModelScope)
        }
    }

    fun getCommunity(id: String){
        communitiesRepository.fetchCommunity(id).onEach { res ->

            when(res){
                is Resource.Success -> {
                    res.data?.let {
                        community.value = it
                    }
                }
                is Resource.Error -> {

                }
            }
        }.launchIn(viewModelScope)
    }

}