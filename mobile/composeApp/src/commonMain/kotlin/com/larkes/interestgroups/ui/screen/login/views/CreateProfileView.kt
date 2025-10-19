package com.larkes.interestgroups.ui.screen.login.views

import androidx.compose.animation.AnimatedVisibility
import androidx.compose.animation.core.tween
import androidx.compose.animation.fadeIn
import androidx.compose.animation.fadeOut
import androidx.compose.animation.slideInVertically
import androidx.compose.animation.slideOutVertically
import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.Image
import androidx.compose.foundation.border
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
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.Button
import androidx.compose.material3.ButtonDefaults
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import com.larkes.interestgroups.presentation.login.models.CreateProfileUIState
import com.larkes.interestgroups.presentation.login.models.LoginUIEvent
import com.larkes.interestgroups.ui.screen.components.NumberTextField
import com.larkes.interestgroups.ui.screen.components.PrimaryButton
import com.larkes.interestgroups.ui.theme.Theme
import interestgroups.composeapp.generated.resources.Apple
import interestgroups.composeapp.generated.resources.FirstLandingVector
import interestgroups.composeapp.generated.resources.Res
import interestgroups.composeapp.generated.resources.SecondLanding
import interestgroups.composeapp.generated.resources.TG
import interestgroups.composeapp.generated.resources.VK
import kotlinx.coroutines.flow.StateFlow
import org.jetbrains.compose.resources.painterResource

@Composable
fun CreateProfileView(uiState: StateFlow<CreateProfileUIState>, onEvent:(LoginUIEvent) -> Unit){

    val state by uiState.collectAsState()
    var visible by remember { mutableStateOf(false) }

    LaunchedEffect(Unit) {
        visible = true
    }

    AnimatedVisibility(
        visible = visible,
        enter = fadeIn(animationSpec = tween(600)) + slideInVertically(
            initialOffsetY = { it / 2 },
            animationSpec = tween(600)
        ),
        exit = fadeOut() + slideOutVertically()
    ) {
        Box(modifier = Modifier.padding(top = 60.dp, bottom = 20.dp)){
            Image(
                painter = painterResource(Res.drawable.SecondLanding),
                contentDescription = null,
                modifier = Modifier.fillMaxWidth(),
                contentScale = ContentScale.Crop
            )
            Column(
                modifier = Modifier.padding(horizontal = 20.dp).fillMaxSize(),
                verticalArrangement = Arrangement.SpaceBetween,
                horizontalAlignment = Alignment.CenterHorizontally
            ) {
                Spacer(modifier = Modifier.height(10.dp))
                Column(
                    horizontalAlignment = Alignment.CenterHorizontally
                ) {
                    Text(
                        text = "Создай свой профиль",
                        style = Theme.fonts.titleLarge,
                        textAlign = TextAlign.Center
                    )
                    Spacer(modifier = Modifier.height(10.dp))
                    Text(
                        text = "Мы вышлем код на твой номер, чтобы подтвердить его",
                        style = Theme.fonts.headlineLarge,
                        textAlign = TextAlign.Center
                    )
                    Spacer(modifier = Modifier.height(43.dp))
                    NumberTextField(
                        value = state.number,
                        hint = "Номер телефона",
                        onValueChange = {
                            onEvent(LoginUIEvent.NumberEntered(it))
                        },
                        modifier = Modifier.height(52.dp)
                    )
                    if(state.error.isNotEmpty()){
                        Spacer(modifier = Modifier.height(10.dp))
                        Text(
                            state.error,
                            style = Theme.fonts.headlineMedium.copy(Color.Red)
                        )
                    }
                }
                Column(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalAlignment = Alignment.CenterHorizontally
                ) {
                    Text(
                        text = "Или регистрация через",
                        style = Theme.fonts.headlineLarge,
                        textAlign = TextAlign.Center
                    )
                    Spacer(modifier = Modifier.height(28.dp))
                    Row(horizontalArrangement = Arrangement.spacedBy(20.dp)) {
                        listOf(Res.drawable.Apple, Res.drawable.TG, Res.drawable.VK).map {
                            Button(
                                modifier = Modifier,
                                onClick = {},
                                contentPadding = PaddingValues(24.dp),
                                shape = RoundedCornerShape(30.dp),
                                border = BorderStroke(1.dp, Theme.colors.formBorderColor),
                                colors = ButtonDefaults.buttonColors(containerColor = Color.White)
                            ){
                                Image(
                                    painter = painterResource(it),
                                    contentDescription = null,
                                    modifier = Modifier.size(32.dp),
                                    contentScale = ContentScale.Crop
                                )
                            }
                        }
                    }
                    Spacer(modifier = Modifier.height(60.dp))
                    PrimaryButton(
                        text = "Продолжить"
                    ){
                        onEvent(LoginUIEvent.ContinueNumberClicked)
                    }
                    Spacer(modifier = Modifier.height(30.dp))
                }
            }
        }
    }
}