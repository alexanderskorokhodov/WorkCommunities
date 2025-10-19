package com.larkes.interestgroups.data.repository

import androidx.compose.ui.text.font.FontVariation
import com.larkes.interestgroups.data.dto.AuthResponse
import com.larkes.interestgroups.data.dto.CodeRequest
import com.larkes.interestgroups.data.dto.CompanyRegRequest
import com.larkes.interestgroups.data.dto.CompanyWithCommunitiesDto
import com.larkes.interestgroups.data.dto.GroupDto
import com.larkes.interestgroups.data.dto.GroupListResponse
import com.larkes.interestgroups.data.dto.NumberRequest
import com.larkes.interestgroups.data.dto.StatusListResponse
import com.larkes.interestgroups.data.dto.UserProfileDto
import com.larkes.interestgroups.domain.models.UpdateUserProfileRequest
import com.larkes.interestgroups.domain.repository.AuthRepository
import com.larkes.interestgroups.presentation.login.models.RoleType
import com.larkes.interestgroups.utils.Resource
import com.russhwolf.settings.Settings
import io.ktor.client.HttpClient
import io.ktor.client.call.body
import io.ktor.client.request.get
import io.ktor.client.request.header
import io.ktor.client.request.patch
import io.ktor.client.request.post
import io.ktor.client.request.setBody
import io.ktor.client.statement.bodyAsText
import io.ktor.http.ContentType
import io.ktor.http.contentType
import kotlinx.coroutines.CoroutineExceptionHandler
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.callbackFlow
import kotlinx.coroutines.flow.flow
import kotlinx.coroutines.withContext
import kotlinx.serialization.json.Json

class AuthRepositoryImpl(
    private val ktorClient: HttpClient,
    private val settigs: Settings
): AuthRepository {

    private val session = "session"
    private val role = "role"
    override fun sendNumber(number: NumberRequest, isCompany: Boolean): Flow<Resource<Unit>> = flow {
        try {
            ktorClient.post(if(isCompany) "/auth/company/otp/request" else "/auth/otp/request") {
                setBody(number)
                contentType(ContentType.Application.Json)
            }
            emit(Resource.Success(Unit))
        }catch (e: Exception){
            emit(Resource.Error(e.message.toString()))
        }
    }

    override fun sendCode(code: CodeRequest, isCompany: Boolean): Flow<Resource<Unit>> = callbackFlow {

        try {
            val res = ktorClient.post(if(isCompany) "/auth/company/otp/verify" else "/auth/otp/verify") {
                setBody(code)
                contentType(ContentType.Application.Json)
            }
            println("NETWORK_LOG ${code} ${res.bodyAsText()}")
            val body = res.body<AuthResponse>()
            settigs.putString(session, body.access_token)
            trySend(Resource.Success(Unit))
            channel.close()
        }catch (e: Exception){
            trySend(Resource.Error(e.message.toString()))
            channel.close()
        }

    }

    override fun companySignIn(request: CompanyRegRequest): Flow<Resource<Unit>> = flow {
        try {
            val res = ktorClient.post("/auth/company/signup") {
                setBody(request)
                contentType(ContentType.Application.Json)
            }
            val body = res.body<AuthResponse>()
            settigs.putString(session, body.access_token)
            emit(Resource.Success(Unit))
        }catch (e: Exception){
            emit(Resource.Error(e.message.toString()))
        }
    }


    override fun createProfile(updateUserProfileRequest: UpdateUserProfileRequest): Flow<Resource<Unit>>  = flow{
        try {
            val session = settigs.getString(session, "")
            println("NETWORK_LOG session $session")
            println("NETWORK_LOG session $updateUserProfileRequest")
            ktorClient.patch("/profiles/me") {
                contentType(ContentType.Application.Json)
                header("Authorization", "Bearer $session")
                setBody(updateUserProfileRequest)
            }
            emit(Resource.Success(Unit))
        }catch (e: Exception){
            println("NETWORK_LOG  ${e.message}")
            emit(Resource.Error(e.message.toString()))
        }
    }

    override fun checkUserAuth(): Pair<Boolean, RoleType>{

        val role = settigs.getStringOrNull(role)
        var totalRole:RoleType = RoleType.Specialist
        if(role == "Specialist"){
            totalRole = RoleType.Specialist
        }else{
            totalRole = RoleType.Company
        }

        return Pair(settigs.getStringOrNull(session) != null,  totalRole)
    }

    override fun fetchSkills(): Flow<Resource<GroupListResponse>> = flow {
        try {
            val res = ktorClient.get("/reference/skills") {
                contentType(ContentType.Application.Json)
            }

            emit(Resource.Success(res.body<GroupListResponse>()))
        }catch (e: Exception){
            emit(Resource.Error(e.message.toString()))
        }
    }

    override fun fetchStatuses(): Flow<Resource<StatusListResponse>> = flow {
        try {
            val res = ktorClient.get("/reference/statuses") {
                contentType(ContentType.Application.Json)
            }

            emit(Resource.Success(res.body<StatusListResponse>()))
        }catch (e: Exception){
            emit(Resource.Error(e.message.toString()))
        }
    }

    override fun cleanSession() {
        settigs.putString(session, "")
    }

    override fun fetchViewProfile(id: String): Flow<Resource<UserProfileDto>> = flow{
        try {
            val json = Json {
                ignoreUnknownKeys = true
                coerceInputValues = true
                explicitNulls = false
            }

            val res = ktorClient.get("/users/${id}") {
                contentType(ContentType.Application.Json)
            }
            emit(Resource.Success(json.decodeFromString(UserProfileDto.serializer(), res.bodyAsText())))
        }catch (e: Exception){
            emit(Resource.Error(e.message.toString()))
        }
    }
}