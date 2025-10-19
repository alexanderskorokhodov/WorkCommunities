package com.larkes.interestgroups.presentation.company_detail

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.larkes.interestgroups.domain.models.Community
import com.larkes.interestgroups.domain.models.CompanyDetail
import com.larkes.interestgroups.domain.repository.CompanyRepository
import com.larkes.interestgroups.presentation.company_detail.models.CompanyDetailUIState
import com.larkes.interestgroups.utils.Constants.SERVER_URL
import com.larkes.interestgroups.utils.Resource
import kotlinx.coroutines.delay
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.launchIn
import kotlinx.coroutines.flow.onEach
import kotlinx.coroutines.launch

class CompanyDetailViewModel(
    private val companyRepository: CompanyRepository
): ViewModel() {

    private val _companyDetailUIState = MutableStateFlow(CompanyDetailUIState())
    val companyDetailUIState: StateFlow<CompanyDetailUIState> = _companyDetailUIState

    fun getCompany(id: String){
        viewModelScope.launch {
            companyRepository.fetchCompanyInfo(id).onEach {res ->
                when(res){
                    is Resource.Success -> {
                        res.data?.let { company ->
                            _companyDetailUIState.value = CompanyDetailUIState(
                                isCompanyLoading = false,
                                isCommunityLoading = false,
                                company = CompanyDetail(
                                    title = company.name,
                                    logo = "$SERVER_URL/media/${company.logo_media_id}",
                                    images = listOf("$SERVER_URL/media/${company.logo_media_id}", "https://news.store.rambler.ru/img/ce010f79b112d272835d8ec93cf9f3f9?img-format=auto&img-1-resize=height:400,fit:max&img-2-filter=sharpen", "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRlGkXn8yV9XelzZDdTjD8098a6ttnmoUUbEQ&s"),
                                    about = company.description,
                                    highlight = "Здесь ты можешь начать путь в high-tech: присоединиться к сообществу, участвовать в проектах и получить первый опыт."
                                ),
                                communities = company.communities.map {
                                    Community(
                                        id = it.id,
                                        image = "$SERVER_URL/media/${it.logo_media_id}",
                                        logo = "Лого",
                                        highlight = it.tags,
                                        title = it.name,
                                        isNew = false
                                    )
                                }
                            )
                        }
                    }
                    is Resource.Error -> {

                    }
                }
            }.launchIn(viewModelScope)
        }
    }
    init {

    }

}