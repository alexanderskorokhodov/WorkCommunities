package com.larkes.interestgroups

import com.larkes.interestgroups.data.dto.CodeRequest
import com.larkes.interestgroups.data.dto.NumberRequest
import com.larkes.interestgroups.data.network.HttpEngineFactory
import com.larkes.interestgroups.data.repository.AuthRepositoryImpl
import com.russhwolf.settings.Settings
import io.ktor.client.HttpClient
import io.ktor.client.plugins.HttpTimeout
import io.ktor.client.plugins.contentnegotiation.ContentNegotiation
import io.ktor.client.plugins.defaultRequest
import io.ktor.client.plugins.logging.Logger
import io.ktor.client.plugins.logging.Logging
import io.ktor.serialization.kotlinx.json.json
import kotlinx.coroutines.flow.launchIn
import kotlinx.coroutines.flow.onEach
import kotlinx.coroutines.runBlocking
import kotlinx.serialization.json.Json
import kotlin.test.Test

class TestAuth {

    private val auth = AuthRepositoryImpl( HttpClient(HttpEngineFactory().createEngine()) {
        install(ContentNegotiation) {
            json(Json {
                prettyPrint = true
                isLenient = true
                ignoreUnknownKeys = true
            })
        }
        install(Logging){
            logger = object : Logger{
                override fun log(message: String) {
                    println("NETWORK_LOG $message")
                }

            }
        }
        defaultRequest {
            url("https://ly1qte-91-197-99-176.ru.tuna.am")
        }

        install(HttpTimeout) {
            connectTimeoutMillis = 159000
            requestTimeoutMillis = 500000
        }
    }, Settings())

    @Test
    fun testNumber(){
        runBlocking {
            auth.sendNumber(NumberRequest("+742693840809259")).onEach {  }.launchIn(this)
        }
    }

    @Test
    fun testOtp(){
        runBlocking {
            auth.sendCode(CodeRequest(
                phone = "+742693840809259",
                code = "111111"))
        }
    }

}