package com.larkes.interestgroups.domain.repository

import com.larkes.interestgroups.data.dto.PostDto
import com.larkes.interestgroups.data.dto.PostListResponse
import com.larkes.interestgroups.domain.models.Post
import com.larkes.interestgroups.utils.Resource
import kotlinx.coroutines.flow.Flow

interface PostsRepository {
    fun getPosts(): Flow<Resource<PostListResponse>>
    fun getPost(id: String): Flow<Resource<PostDto>>
}