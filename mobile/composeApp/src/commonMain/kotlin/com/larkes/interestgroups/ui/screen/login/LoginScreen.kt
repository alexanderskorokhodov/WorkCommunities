package com.larkes.interestgroups.ui.screen.login

import androidx.compose.foundation.Image
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.unit.dp
import androidx.navigation.NavController
import com.larkes.interestgroups.presentation.login.LoginViewModel
import com.larkes.interestgroups.presentation.login.models.LoginUIAction
import com.larkes.interestgroups.presentation.login.models.LoginUIEvent

import com.larkes.interestgroups.ui.navigation.Screens
import com.larkes.interestgroups.ui.screen.login.views.AboutMeView
import com.larkes.interestgroups.ui.screen.login.views.ChooseRoleView
import com.larkes.interestgroups.ui.screen.login.views.CompanyView
import com.larkes.interestgroups.ui.screen.login.views.CreateProfileView
import com.larkes.interestgroups.ui.screen.login.views.EnterCodeView
import interestgroups.composeapp.generated.resources.FirstLandingVector
import interestgroups.composeapp.generated.resources.Res
import org.jetbrains.compose.resources.painterResource

@Composable
fun LoginScreen(navController: NavController, viewModel: LoginViewModel){
    val uiAction by viewModel.uiAction.collectAsState()

    when(uiAction){
        LoginUIAction.OpenCompany -> {
            CompanyView(
                viewModel.companyUIState
            ) {
                viewModel.onEvent(it)
            }
        }
        LoginUIAction.OpenChoseRole -> {
            ChooseRoleView {
                viewModel.onEvent(it)
            }
        }
        LoginUIAction.OpenCreateProfile -> {
            CreateProfileView(viewModel.createProfileUIState) {
                viewModel.onEvent(it)
            }
        }
        LoginUIAction.OpenCode -> {
            EnterCodeView(viewModel.enterCodeUIState) {
                viewModel.onEvent(it)
            }
        }
        LoginUIAction.OpenAboutNe -> {
            AboutMeView(viewModel.aboutMeUIState){
                viewModel.onEvent(it)
            }
        }
        LoginUIAction.OpenMain -> {
            navController.navigate(Screens.MainScreen)
        }
        LoginUIAction.OpenCompanyProfile -> {
            navController.navigate(Screens.CompanyProfileScreen)
        }
    }

}