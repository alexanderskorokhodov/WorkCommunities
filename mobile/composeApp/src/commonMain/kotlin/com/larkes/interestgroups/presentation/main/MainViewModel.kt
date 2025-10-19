package com.larkes.interestgroups.presentation.main

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.larkes.interestgroups.domain.models.Community
import com.larkes.interestgroups.domain.models.Company
import com.larkes.interestgroups.domain.models.Event
import com.larkes.interestgroups.domain.models.Post
import com.larkes.interestgroups.domain.repository.CommunitiesRepository
import com.larkes.interestgroups.domain.repository.CompanyRepository
import com.larkes.interestgroups.domain.repository.EventRepository
import com.larkes.interestgroups.domain.repository.PostsRepository
import com.larkes.interestgroups.presentation.main.models.MainUIState
import com.larkes.interestgroups.utils.Constants.SERVER_URL
import com.larkes.interestgroups.utils.Resource
import kotlinx.coroutines.delay
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.launchIn
import kotlinx.coroutines.flow.onEach
import kotlinx.coroutines.launch

class MainViewModel(
    private val communitiesRepository: CommunitiesRepository,
    private val postsRepository: PostsRepository,
    private val companyRepository: CompanyRepository,
    private val eventRepository: EventRepository
): ViewModel() {

    private val _uiState = MutableStateFlow(MainUIState())
    val uiState: StateFlow<MainUIState> = _uiState

    init {
        communitiesRepository.fetchRecommentedCommunities().onEach {res ->
            when(res){
                is Resource.Success -> {
                    res.data?.let {companies ->
                        _uiState.value = uiState.value.copy(
                            communities = companies.map {
                                println("NETWORK_LOG $SERVER_URL/media/${it.logo_media_id}")
                                Community(
                                    image = "$SERVER_URL/media/${it.logo_media_id}",
                                    highlight = it.tags,
                                    title = it.name,
                                    isNew = true,
                                    logo = "Лого",
                                    id = it.id
                                )
                            }
                        )
                    }
                }
                is Resource.Error -> {

                }
            }
        }.launchIn(viewModelScope)

        //"$SERVER_URL${it.media[0].url}"
        postsRepository.getPosts().onEach {res ->
            when(res){
                is Resource.Success -> {
                    res.data?.let {posts ->
                                _uiState.value = uiState.value.copy(
                            posts = posts.map {
                                Post(
                                    image = "$SERVER_URL/media/${it.media[0].id}",
                                    title = it.title,
                                    id = it.id
                                )
                            }
                        )
                    }
                }
                is Resource.Error -> {

                }
            }
        }.launchIn(viewModelScope)

        companyRepository.fetchCompanies().onEach {res ->
            when(res){
                is Resource.Success -> {
                    res.data?.let {companies ->
                        _uiState.value = uiState.value.copy(
                            companies = companies.map {
                                Company(
                                    image = "$SERVER_URL/media/${it.logo_media_id}",
                                    logo = "Лого",
                                    highlight =  it.skills.map { it.title },
                                    title = it.name,
                                    id = it.id
                                )
                            }
                        )
                    }
                }
                is Resource.Error -> {

                }
            }
        }.launchIn(viewModelScope)

        eventRepository.fetchEvents().onEach {res ->
            when(res){
                is Resource.Success -> {
                    res.data?.let {companies ->
                        _uiState.value = uiState.value.copy(
                            events = companies.map {
                                Event(
                                    image = "$SERVER_URL/media/${it.media_id}",
                                    highlight = it.skills.map {skill -> skill.title },
                                    date = it.event_date,
                                    title = it.title
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