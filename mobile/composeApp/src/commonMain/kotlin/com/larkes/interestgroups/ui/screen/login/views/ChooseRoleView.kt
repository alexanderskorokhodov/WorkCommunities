package com.larkes.interestgroups.ui.screen.login.views

import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.Image
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.Button
import androidx.compose.material3.ButtonDefaults
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import com.larkes.interestgroups.presentation.login.models.LoginUIEvent
import com.larkes.interestgroups.ui.screen.components.RoleButton
import com.larkes.interestgroups.ui.theme.Theme
import interestgroups.composeapp.generated.resources.Company
import interestgroups.composeapp.generated.resources.FirstLandingVector
import interestgroups.composeapp.generated.resources.Res
import interestgroups.composeapp.generated.resources.Specialist
import org.jetbrains.compose.resources.painterResource

@Composable
fun ChooseRoleView(onEvent:(LoginUIEvent) -> Unit) {

    Box(modifier = Modifier.padding(top = 60.dp, bottom = 20.dp)){
        Image(
            painter = painterResource(Res.drawable.FirstLandingVector),
            contentDescription = null,
            modifier = Modifier.fillMaxWidth(),
            contentScale = ContentScale.Crop
        )
        Column(
            modifier = Modifier.padding(horizontal = 20.dp).fillMaxSize(),
            verticalArrangement = Arrangement.SpaceBetween,
            horizontalAlignment = Alignment.CenterHorizontally
        ) {
           Column(
               horizontalAlignment = Alignment.CenterHorizontally
           ) {
               Text(
                   text = Theme.strings.CHOOSE_ROLE_TITLE,
                   style = Theme.fonts.titleLarge,
                   textAlign = TextAlign.Center
               )
               Spacer(modifier = Modifier.height(49.dp))
               RoleButton(
                   image = Res.drawable.Company,
                   text = "Компания"
               ){
                   onEvent(LoginUIEvent.CompanyClicked)
               }
               Spacer(modifier = Modifier.height(20.dp))
               RoleButton(
                   image = Res.drawable.Specialist,
                   text = "Специалист"
               ){
                   onEvent(LoginUIEvent.SpecialistButtonClicked)
               }
           }
        }
    }

}