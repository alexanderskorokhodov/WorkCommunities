package com.larkes.interestgroups.presentation.post_detail

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.larkes.interestgroups.domain.models.PostDetail
import com.larkes.interestgroups.domain.repository.PostsRepository
import com.larkes.interestgroups.presentation.post_detail.models.PostDetailUIState
import com.larkes.interestgroups.utils.Constants.SERVER_URL
import com.larkes.interestgroups.utils.Resource
import kotlinx.coroutines.delay
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.launchIn
import kotlinx.coroutines.flow.onEach
import kotlinx.coroutines.launch

class PostDetailViewModel(
    private val postsRepository: PostsRepository
): ViewModel() {

    private val _uiState = MutableStateFlow(PostDetailUIState())
    val uiState: StateFlow<PostDetailUIState> = _uiState

    fun getPost(id: String){

        viewModelScope.launch {
            postsRepository.getPost(id).onEach { res ->
                when(res) {
                    is Resource.Error -> {

                    }
                    is Resource.Success -> {
                        res.data?.let { post ->
                            _uiState.value = _uiState.value.copy(
                                isLoading = false,
                                post = PostDetail(
                                    id = id,
                                    image = "$SERVER_URL/media/${post.media.getOrNull(0)?.id}",
                                    title = post.title,
                                    text = post.body ?: "null",
                                    date = "14 октября, 17:00",
                                    format = "открытая сессия + ответы на вопросы",
                                    registration = "в сообществе ${post.title}"
                                )
                            )
                        }
                    }
                }
            }.launchIn(viewModelScope)
        }

    }


}