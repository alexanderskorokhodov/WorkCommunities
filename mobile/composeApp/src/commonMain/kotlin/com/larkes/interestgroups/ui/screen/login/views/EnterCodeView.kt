package com.larkes.interestgroups.ui.screen.login.views

import androidx.compose.foundation.Image
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.width
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import com.larkes.interestgroups.presentation.login.models.EnterCodeUIState
import com.larkes.interestgroups.presentation.login.models.LoginUIEvent
import com.larkes.interestgroups.ui.screen.components.OtpCodeInput
import com.larkes.interestgroups.ui.screen.components.PrimaryButton
import com.larkes.interestgroups.ui.theme.Theme
import interestgroups.composeapp.generated.resources.FirstLandingVector
import interestgroups.composeapp.generated.resources.Res
import interestgroups.composeapp.generated.resources.SecondLanding
import interestgroups.composeapp.generated.resources.arrow_left
import kotlinx.coroutines.flow.StateFlow
import org.jetbrains.compose.resources.painterResource

@Composable
fun EnterCodeView(
    uiState: StateFlow<EnterCodeUIState>,
    onEvent:(LoginUIEvent) -> Unit
){

    val state by uiState.collectAsState()
    Column(
        modifier = Modifier.fillMaxSize(),
        horizontalAlignment = Alignment.CenterHorizontally
    ) {
        Column(modifier = Modifier.padding(horizontal = 20.dp), horizontalAlignment = Alignment.CenterHorizontally) {
            Spacer(modifier = Modifier.height(60.dp))
            Box(modifier = Modifier.fillMaxWidth()){
                Image(
                    painter = painterResource(Res.drawable.arrow_left),
                    contentDescription = null,
                    modifier = Modifier
                        .height(19.dp)
                        .width(10.dp)
                        .clickable{

                        },
                    contentScale = ContentScale.Crop
                )
            }
            Spacer(modifier = Modifier.height(7.dp))
            Text(
                text = "Введи код",
                style = Theme.fonts.titleLarge,
                textAlign = TextAlign.Center
            )
            Spacer(modifier = Modifier.height(10.dp))
            Text(
                text = "Мы прислали код на твой номер +7${state.number}, введи его, чтобы войти в аккаунт",
                style = Theme.fonts.headlineLarge,
                textAlign = TextAlign.Center
            )
            Spacer(modifier = Modifier.height(28.dp))
            OtpCodeInput(
                length = 5,
                code = state.code
            ){
                onEvent(LoginUIEvent.SmsCodeEntered(it))
            }
            Spacer(modifier = Modifier.height(20.dp))
            Text(
                text = "Прислать код повторно через 00:${state.repeatTime}",
                style = Theme.fonts.headlineMedium,
                textAlign = TextAlign.Center
            )
        }
        Spacer(modifier = Modifier.height(60.dp))
        Image(
            painter = painterResource(Res.drawable.SecondLanding),
            contentDescription = null,
            modifier = Modifier.fillMaxWidth(),
            contentScale = ContentScale.Crop
        )
    }

}