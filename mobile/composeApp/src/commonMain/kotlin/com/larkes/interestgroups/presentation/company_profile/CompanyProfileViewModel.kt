package com.larkes.interestgroups.presentation.company_profile

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.larkes.interestgroups.domain.repository.CompanyRepository
import com.larkes.interestgroups.presentation.login.models.CompanyUIState
import com.larkes.interestgroups.utils.Constants
import com.larkes.interestgroups.utils.Resource
import kotlinx.coroutines.delay
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.launchIn
import kotlinx.coroutines.flow.onEach
import kotlinx.coroutines.launch

class CompanyProfileViewModel(
    private val companyRepository: CompanyRepository
): ViewModel() {

    private val _uiState = MutableStateFlow(CompanyUIState())
    val uiState: StateFlow<CompanyUIState> = _uiState

    init {

        viewModelScope.launch {
            companyRepository.fetchCompanyInfo().onEach { res ->
                when(res){
                    is Resource.Success  -> {
                        res.data?.let { company ->
                            println("svsdvsdv ${Constants.SERVER_URL}/media/${company.logo_media_id}")
                            _uiState.value = uiState.value.copy(
                                image = "${Constants.SERVER_URL}/media/${company.logo_media_id}",
                                companyName = company.name,
                                description = company.description ?: "",
                                specialities = listOf("Биотех", "Хим инженерия")
                            )
                        }
                    }
                    is Resource.Error -> {}
                }
            }.launchIn(viewModelScope)
        }


    }

}