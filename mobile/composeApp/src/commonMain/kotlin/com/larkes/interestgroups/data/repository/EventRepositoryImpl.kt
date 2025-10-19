package com.larkes.interestgroups.data.repository

import com.larkes.interestgroups.data.dto.EventListResponse
import com.larkes.interestgroups.data.dto.PostListResponse
import com.larkes.interestgroups.domain.repository.EventRepository
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

class EventRepositoryImpl(
    private val settings: Settings,
    private val ktorClient: HttpClient
): EventRepository {

    private val session = settings.getStringOrNull("session")

    override fun fetchEvents(): Flow<Resource<EventListResponse>> = flow{
        try {
            val res = ktorClient.get("/events/upcoming") {
                parameter("offset", 0)
                parameter("limit", 20)
                header("Authorization", "Bearer $session")
                contentType(ContentType.Application.Json)
            }
            println("NETWORK_LOG events ${res.bodyAsText()}")
            emit(Resource.Success(res.body<EventListResponse>()))
        }catch (e: Exception){
            emit(Resource.Error(e.message.toString()))
        }

    }
}
