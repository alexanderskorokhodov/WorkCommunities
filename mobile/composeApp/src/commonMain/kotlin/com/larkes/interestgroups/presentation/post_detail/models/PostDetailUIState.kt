package com.larkes.interestgroups.presentation.post_detail.models

import com.larkes.interestgroups.domain.models.PostDetail

data class PostDetailUIState(
    val isLoading: Boolean = true,
    val post: PostDetail? = null
)