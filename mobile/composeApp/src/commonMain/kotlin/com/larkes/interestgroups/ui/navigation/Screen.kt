package com.larkes.interestgroups.ui.navigation

import kotlinx.serialization.Serializable


@Serializable
sealed class Screens{
    @Serializable
    data object LoginScreen: Screens()
    @Serializable
    data object MainScreen: Screens()
    @Serializable
    data class PostDetailScreen(val id: String): Screens()
    @Serializable
    data class CompanyDetailScreen(val id: String): Screens()
    @Serializable
    data object ProfileScreen: Screens()
    @Serializable
    data object CompanyProfileScreen: Screens()
    @Serializable
    data object CompanyPostsScreen: Screens()
    @Serializable
    data object CompanyVacanciesScreen: Screens()
    @Serializable
    data object CompanyCommunitiesScreen: Screens()
    @Serializable
    data class CommunityDetailScreen(val id: String): Screens()

    @Serializable
    data class CompanyCommunitiesDetailsScreen(val id: String): Screens()

    @Serializable
    data class CompanyUserProfileScreen(val id: String): Screens()
    @Serializable
    data object WebinarScreen: Screens()
}

