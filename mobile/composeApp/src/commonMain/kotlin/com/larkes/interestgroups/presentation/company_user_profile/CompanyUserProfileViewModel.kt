package com.larkes.interestgroups.presentation.company_user_profile

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.larkes.interestgroups.data.dto.UserProfileDto
import com.larkes.interestgroups.domain.repository.AuthRepository
import com.larkes.interestgroups.utils.Resource
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.launchIn
import kotlinx.coroutines.flow.onEach

class CompanyUserProfileViewModel(
    private val authRepository: AuthRepository
): ViewModel() {

    val _userData = MutableStateFlow<UserProfileDto?>(null)

    fun fetchProfile(id: String){
        authRepository.fetchViewProfile(id).onEach { res ->
            when(res){
                is Resource.Success -> {
                    res.data?.let {
                        _userData.value = it
                    }
                }
                is Resource.Error -> {}
            }
        }.launchIn(viewModelScope)
    }


}