package com.larkes.interestgroups.domain.repository

import com.larkes.interestgroups.data.dto.CommunityWithDetailsDto
import com.larkes.interestgroups.data.dto.GroupDto
import com.larkes.interestgroups.data.dto.ProjectDto
import com.larkes.interestgroups.data.dto.ProjectListResponse
import com.larkes.interestgroups.utils.Resource
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.flow

interface CommunitiesRepository {

    fun fetchRecommentedCommunities(): Flow<Resource<ProjectListResponse>>
    fun fetchCommunity(id: String): Flow<Resource<CommunityWithDetailsDto>>
    fun communitySubscribe(id: String): Flow<Resource<Unit>>

}