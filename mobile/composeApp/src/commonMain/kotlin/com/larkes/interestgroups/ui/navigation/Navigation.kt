package com.larkes.interestgroups.ui.navigation

import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.BottomAppBar
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.geometry.Rect
import androidx.compose.ui.unit.dp
import androidx.navigation.NavController
import androidx.navigation.compose.NavHost
import androidx.navigation.NavHostController
import androidx.navigation.compose.composable
import androidx.navigation.toRoute
import com.larkes.interestgroups.presentation.community_detail.CommunityDetailViewModel
import com.larkes.interestgroups.presentation.company_communities.CompanyCommunitiesViewModel
import com.larkes.interestgroups.presentation.company_community_detail.CompanyCommunityDetailViewModel
import com.larkes.interestgroups.presentation.company_detail.CompanyDetailViewModel
import com.larkes.interestgroups.presentation.company_profile.CompanyProfileViewModel
import com.larkes.interestgroups.presentation.company_user_profile.CompanyUserProfileViewModel
import com.larkes.interestgroups.presentation.login.LoginViewModel
import com.larkes.interestgroups.presentation.main.MainViewModel
import com.larkes.interestgroups.presentation.post_detail.PostDetailViewModel
import com.larkes.interestgroups.ui.screen.community_detail.CommunityDetailScreen
import com.larkes.interestgroups.ui.screen.company_communities.CompanyCommunitiesScreen
import com.larkes.interestgroups.ui.screen.company_community_detail.CompanyCommunityDetailScreen
import com.larkes.interestgroups.ui.screen.company_detail.CompanyDetailScreen
import com.larkes.interestgroups.ui.screen.company_profile.CompanyProfileScreen
import com.larkes.interestgroups.ui.screen.company_user_profile.CompanyUserProfileScreen
import com.larkes.interestgroups.ui.screen.login.LoginScreen
import com.larkes.interestgroups.ui.screen.main.MainScreen
import com.larkes.interestgroups.ui.screen.post_detail.PostDetailScreen
import com.larkes.interestgroups.ui.screen.profile.ProfileScreen
import com.larkes.interestgroups.ui.screen.webinar_screen.WebinarScreen
import com.russhwolf.settings.Settings
import interestgroups.composeapp.generated.resources.Res
import interestgroups.composeapp.generated.resources.calendar
import interestgroups.composeapp.generated.resources.home
import interestgroups.composeapp.generated.resources.key
import interestgroups.composeapp.generated.resources.people
import interestgroups.composeapp.generated.resources.profile
import interestgroups.composeapp.generated.resources.union
import org.koin.compose.viewmodel.koinViewModel

@Composable
fun Navigation(navController: NavHostController) {

    Box(){
        Column() {
            NavHost(navController, Screens.LoginScreen){
                composable<Screens.LoginScreen> {
                    val viewModel: LoginViewModel = koinViewModel()
                    LoginScreen(navController, viewModel)
                }
                composable<Screens.MainScreen> {
                    val viewModel: MainViewModel = koinViewModel()
                    MainScreen(navController,viewModel)
                }
                composable<Screens.CompanyDetailScreen> {entry ->
                    val id: Screens.CompanyDetailScreen = entry.toRoute<Screens.CompanyDetailScreen>()
                    val viewModel: CompanyDetailViewModel = koinViewModel()
                    CompanyDetailScreen(
                        navController = navController,
                        viewModel = viewModel,
                        id = id.id
                    )
                }
                composable<Screens.PostDetailScreen> {entry ->
                    val id: Screens.PostDetailScreen = entry.toRoute<Screens.PostDetailScreen>()
                    val viewModel: PostDetailViewModel = koinViewModel()
                    PostDetailScreen(navController, viewModel, id = id.id)
                }
                composable<Screens.ProfileScreen> {
                    ProfileScreen(navController)
                }
                composable<Screens.CompanyProfileScreen> {
                    val viewModel: CompanyProfileViewModel = koinViewModel()
                    CompanyProfileScreen(viewModel, navController)
                }
                composable<Screens.CompanyPostsScreen> {

                }
                composable<Screens.CompanyCommunitiesScreen> {

                }
                composable<Screens.CompanyVacanciesScreen> {

                }
                composable<Screens.CommunityDetailScreen> {entry ->
                    val id: Screens.CommunityDetailScreen = entry.toRoute<Screens.CommunityDetailScreen>()
                    val viewModel: CommunityDetailViewModel = koinViewModel()
                    CommunityDetailScreen( viewModel,navController, id.id)
                }
                composable<Screens.CompanyCommunitiesScreen> {
                    val viewModel: CompanyCommunitiesViewModel = koinViewModel()
                    CompanyCommunitiesScreen(viewModel, navController)
                }
                composable<Screens.CompanyCommunitiesDetailsScreen> {entry ->
                    val id: Screens.CompanyCommunitiesDetailsScreen = entry.toRoute<Screens.CompanyCommunitiesDetailsScreen>()
                    val viewModel: CompanyCommunityDetailViewModel = koinViewModel()
                    CompanyCommunityDetailScreen(navController, viewModel,id.id)
                }
                composable<Screens.CompanyUserProfileScreen> {entry ->
                    val viewModel: CompanyUserProfileViewModel = koinViewModel()
                    val id: Screens.CompanyUserProfileScreen = entry.toRoute<Screens.CompanyUserProfileScreen>()
                    CompanyUserProfileScreen(navController,viewModel,id.id)
                }
                composable<Screens.WebinarScreen> {
                    WebinarScreen(navController)
                }
            }
        }
        Box(modifier = Modifier.fillMaxSize(), contentAlignment = Alignment.BottomCenter) {
            if(Settings().getString("role","") == "Specialist"){
                BottomNavBar(
                    items = listOf(
                        BottomNavItem(Res.drawable.union, "Главная", Screens.MainScreen),
                        BottomNavItem(Res.drawable.people, "Сообщества", Screens.MainScreen),
                        BottomNavItem(Res.drawable.home, "Компании", Screens.MainScreen),
                        BottomNavItem(Res.drawable.calendar, "События", Screens.MainScreen),
                        BottomNavItem(Res.drawable.profile, "Профиль", Screens.ProfileScreen),

                    ),
                    navController = navController
                ){
                    navController.navigate(it.route)
                }
            }else{
                BottomNavBar(
                    items = listOf(
                        BottomNavItem(Res.drawable.union, "Посты", Screens.CompanyPostsScreen),
                        BottomNavItem(Res.drawable.people, "Вакансии", Screens.CompanyVacanciesScreen),
                        BottomNavItem(Res.drawable.key, "Сообщения", Screens.CompanyCommunitiesScreen),
                        BottomNavItem(Res.drawable.profile, "Профиль", Screens.CompanyProfileScreen)
                    ),
                    navController = navController
                ){
                    navController.navigate(it.route)
                }
            }
        }
    }


}