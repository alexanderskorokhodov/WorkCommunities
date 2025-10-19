package com.larkes.interestgroups.data.repository

import com.larkes.interestgroups.data.dto.PostDto
import com.larkes.interestgroups.data.dto.PostListResponse
import com.larkes.interestgroups.data.dto.ProjectListResponse
import com.larkes.interestgroups.domain.repository.PostsRepository
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
import kotlinx.coroutines.flow.catch
import kotlinx.coroutines.flow.flow
import kotlinx.serialization.json.Json

class PostsRepositoryImpl(
    private val settings: Settings,
    private val ktorClient: HttpClient
): PostsRepository {

    private val session = settings.getStringOrNull("session")
    override fun getPosts(): Flow<Resource<PostListResponse>> = flow{

        try {
            val res = ktorClient.get("/content/posts") {
                parameter("limit", 2)
                parameter("offest", 0)
                header("Authorization", "Bearer $session")
                contentType(ContentType.Application.Json)
            }
            val json = Json {
                ignoreUnknownKeys = true
                coerceInputValues = true
                explicitNulls = false
            }
            println("NETWORK_LOG posts ${res.bodyAsText()}")
            val posts = json.decodeFromString<PostListResponse>(res.bodyAsText())
            emit(Resource.Success(posts))
        }catch (e: Exception){
            println("NETWORK_LOG posts ${e.message.toString()}")
        }
    }.catch { e ->
       // emit(Resource.Error(e.message.toString()))
    }

    override fun getPost(id: String): Flow<Resource<PostDto>> = flow{
        try {
            val json = Json {
                ignoreUnknownKeys = true
                coerceInputValues = true
                explicitNulls = false
            }
            val res = ktorClient.get("/content/posts/${id}") {
                header("Authorization", "Bearer $session")
                contentType(ContentType.Application.Json)
            }
            println("sdcsdvsd ${res.bodyAsText()}")
            val post = res.body<PostDto>()

            emit(Resource.Success(post))
        }catch (e: Exception){
            emit(Resource.Error(e.message.toString()))
        }
    }

}