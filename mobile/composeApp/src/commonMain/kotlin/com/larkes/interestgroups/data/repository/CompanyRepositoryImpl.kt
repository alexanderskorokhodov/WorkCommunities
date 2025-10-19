package com.larkes.interestgroups.data.repository

import com.larkes.interestgroups.data.dto.CommunityWithDetailsDto
import com.larkes.interestgroups.data.dto.CompanyCommunityItemDto
import com.larkes.interestgroups.data.dto.CompanyCommunityListResponse
import com.larkes.interestgroups.data.dto.CompanyDto
import com.larkes.interestgroups.data.dto.CompanyInfoDto
import com.larkes.interestgroups.data.dto.CompanyListResponse
import com.larkes.interestgroups.data.dto.CompanyWithCommunitiesDto
import com.larkes.interestgroups.data.dto.PostListResponse
import com.larkes.interestgroups.data.dto.ProjectDto
import com.larkes.interestgroups.domain.repository.CompanyRepository
import com.larkes.interestgroups.utils.Resource
import com.russhwolf.settings.Settings
import io.ktor.client.HttpClient
import io.ktor.client.call.body
import io.ktor.client.request.get
import io.ktor.client.request.header
import io.ktor.client.request.parameter
import io.ktor.client.statement.bodyAsText
import io.ktor.http.ContentType
import io.ktor.http.contentType
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.flow
import kotlinx.serialization.json.Json

class CompanyRepositoryImpl(
    private val settings: Settings,
    private val ktorClient: HttpClient
): CompanyRepository {

    private val session = settings.getStringOrNull("session")

    override fun fetchCompanies(): Flow<Resource<CompanyListResponse>> = flow{
        try {
            val res = ktorClient.get("/companies/") {
                header("Authorization", "Bearer $session")
                contentType(ContentType.Application.Json)
            }
            println("NETWORK_LOG company ${res.bodyAsText()}")
            emit(Resource.Success(res.body<CompanyListResponse>()))
        }catch (e: Exception){
            emit(Resource.Error(e.message.toString()))
        }
    }

    override fun fetchCompanyInfo(id: String): Flow<Resource<CompanyWithCommunitiesDto>> = flow {
        try {
            val res = ktorClient.get("/companies/${id}") {
                header("Authorization", "Bearer $session")
                contentType(ContentType.Application.Json)
            }
            emit(Resource.Success(res.body<CompanyWithCommunitiesDto>()))
        }catch (e: Exception){
            emit(Resource.Error(e.message.toString()))
        }
    }

    override fun fetchCompanyInfo(): Flow<Resource<CompanyWithCommunitiesDto>> = flow {
        try {
            val json = Json {
                ignoreUnknownKeys = true
                coerceInputValues = true
                explicitNulls = false
            }
            val res = ktorClient.get("/companies/me") {
                header("Authorization", "Bearer $session")
                contentType(ContentType.Application.Json)
            }
            println("NETWORK_RES ${res.bodyAsText()}")
            emit(Resource.Success(json.decodeFromString(CompanyWithCommunitiesDto.serializer(), res.bodyAsText())))
        }catch (e: Exception){
            emit(Resource.Error(e.message.toString()))
        }
    }

    override fun fetchCompanyCommunities(): Flow<Resource<CompanyCommunityListResponse>> = flow{
        try {
            val res = ktorClient.get("/communities/mine") {
                header("Authorization", "Bearer $session")
                contentType(ContentType.Application.Json)
            }
            println("NETWORK_LOG commob ${res.bodyAsText()}")
            emit(Resource.Success(res.body<CompanyCommunityListResponse>()))
        }catch (e: Exception){
            emit(Resource.Error(e.message.toString()))
        }
    }

}