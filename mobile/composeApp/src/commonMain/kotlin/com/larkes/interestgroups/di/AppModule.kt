package com.larkes.interestgroups.di

import com.larkes.interestgroups.data.network.HttpEngineFactory
import com.larkes.interestgroups.data.repository.AuthRepositoryImpl
import com.larkes.interestgroups.data.repository.CommunitiesRepositoryImpl
import com.larkes.interestgroups.data.repository.CompanyRepositoryImpl
import com.larkes.interestgroups.data.repository.EventRepositoryImpl
import com.larkes.interestgroups.data.repository.PostsRepositoryImpl
import com.larkes.interestgroups.domain.repository.AuthRepository
import com.larkes.interestgroups.domain.repository.CommunitiesRepository
import com.larkes.interestgroups.domain.repository.CompanyRepository
import com.larkes.interestgroups.domain.repository.EventRepository
import com.larkes.interestgroups.domain.repository.PostsRepository
import com.larkes.interestgroups.presentation.community_detail.CommunityDetailViewModel
import com.larkes.interestgroups.presentation.company_communities.CompanyCommunitiesViewModel
import com.larkes.interestgroups.presentation.company_community_detail.CompanyCommunityDetailViewModel
import com.larkes.interestgroups.presentation.company_detail.CompanyDetailViewModel
import com.larkes.interestgroups.presentation.company_profile.CompanyProfileViewModel
import com.larkes.interestgroups.presentation.company_user_profile.CompanyUserProfileViewModel
import com.larkes.interestgroups.presentation.login.LoginViewModel
import com.larkes.interestgroups.presentation.main.MainViewModel
import com.larkes.interestgroups.presentation.post_detail.PostDetailViewModel
import com.larkes.interestgroups.utils.Constants.SERVER_URL
import com.russhwolf.settings.Settings
import io.ktor.client.HttpClient
import io.ktor.client.plugins.HttpTimeout
import io.ktor.client.plugins.contentnegotiation.ContentNegotiation
import io.ktor.client.plugins.defaultRequest
import io.ktor.client.plugins.logging.Logger
import io.ktor.client.plugins.logging.Logging
import io.ktor.serialization.kotlinx.json.json
import kotlinx.serialization.json.Json
import org.koin.dsl.module

val appModule = module {

    factory {
        HttpClient(HttpEngineFactory().createEngine()) {
            install(ContentNegotiation) {
                json(Json {
                    prettyPrint = true
                    isLenient = true
                    ignoreUnknownKeys = true
                })
            }
            defaultRequest {
                url(SERVER_URL)
            }

            install(Logging){
                logger = object : Logger{
                    override fun log(message: String) {
                        println("NETWORK_LOG $message")
                    }

                }
            }

            install(HttpTimeout) {
                connectTimeoutMillis = 159000
                requestTimeoutMillis = 500000
            }
        }
    }

    factory {
        Settings()
    }

    factory<AuthRepository> { AuthRepositoryImpl(get(), get()) }

    factory<AuthRepository> {
        AuthRepositoryImpl(get(), get())
    }

    factory<CommunitiesRepository> {
        CommunitiesRepositoryImpl(get(), get())
    }

    factory<PostsRepository> {
        PostsRepositoryImpl(get(), get())
    }
    factory<CompanyRepository> {
        CompanyRepositoryImpl(get(), get())
    }
    factory<EventRepository> {
        EventRepositoryImpl(get(), get())
    }

    factory { CommunityDetailViewModel(get()) }
    factory { CompanyDetailViewModel(get()) }
    factory { PostDetailViewModel(get()) }

    factory { CompanyCommunitiesViewModel(get()) }
    factory { CompanyProfileViewModel(get()) }
    factory { CompanyCommunityDetailViewModel(get()) }
    factory { MainViewModel(get(), get(), get(), get()) }

    factory { CompanyUserProfileViewModel(get()) }
    factory { LoginViewModel(get()) }
}