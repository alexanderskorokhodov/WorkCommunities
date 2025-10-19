package com.larkes.interestgroups.data.repository

import com.larkes.interestgroups.data.dto.CommunityWithDetailsDto
import com.larkes.interestgroups.data.dto.GroupDto
import com.larkes.interestgroups.data.dto.GroupListResponse
import com.larkes.interestgroups.data.dto.ProjectDto
import com.larkes.interestgroups.data.dto.ProjectListResponse
import com.larkes.interestgroups.domain.repository.CommunitiesRepository
import com.larkes.interestgroups.utils.Resource
import com.russhwolf.settings.Settings
import io.ktor.client.HttpClient
import io.ktor.client.call.body
import io.ktor.client.request.get
import io.ktor.client.request.header
import io.ktor.client.request.parameter
import io.ktor.client.request.post
import io.ktor.client.statement.bodyAsText
import io.ktor.http.ContentType
import io.ktor.http.contentType
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.flow

class CommunitiesRepositoryImpl(
    private val settings: Settings,
    private val ktorClient: HttpClient
): CommunitiesRepository {

    private val session = settings.getStringOrNull("session")

    override fun fetchRecommentedCommunities(): Flow<Resource<ProjectListResponse>> = flow {
        try {
            val res = ktorClient.get("/communities/") {
                parameter("offset", 0)
                parameter("limit", 5)
                header("Authorization", "Bearer $session")
                contentType(ContentType.Application.Json)
            }
            println("NETWORK_LOG comm ${res.bodyAsText()}")
            emit(Resource.Success(res.body<ProjectListResponse>()))
        }catch (e: Exception){
            emit(Resource.Error(e.message.toString()))
        }
    }

    override fun fetchCommunity(id: String): Flow<Resource<CommunityWithDetailsDto>> = flow {
        try {
            val res = ktorClient.get("/communities/$id") {
                header("Authorization", "Bearer $session")
                contentType(ContentType.Application.Json)
            }
            emit(Resource.Success(res.body<CommunityWithDetailsDto>()))
        }catch (e: Exception){
            emit(Resource.Error(e.message.toString()))
        }
    }

    override fun communitySubscribe(id: String): Flow<Resource<Unit>> = flow{
        try {
            session.let {
                val res = ktorClient.post("/communities/$id/follow") {
                    header("Authorization", "Bearer $session")
                    contentType(ContentType.Application.Json)
                }
                emit(Resource.Success(Unit))
            }
        }catch (e: Exception){
            emit(Resource.Error(e.message.toString()))
        }
    }
}