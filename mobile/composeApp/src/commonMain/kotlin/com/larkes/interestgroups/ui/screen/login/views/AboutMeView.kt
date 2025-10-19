package com.larkes.interestgroups.ui.screen.login.views

import androidx.compose.animation.AnimatedVisibility
import androidx.compose.animation.core.tween
import androidx.compose.animation.fadeIn
import androidx.compose.animation.fadeOut
import androidx.compose.animation.slideInVertically
import androidx.compose.animation.slideOutVertically
import androidx.compose.foundation.Image
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.sizeIn
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
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import com.larkes.interestgroups.presentation.login.models.AboutMeUIState
import com.larkes.interestgroups.presentation.login.models.LoginUIEvent
import com.larkes.interestgroups.ui.screen.components.StandartDropdown
import com.larkes.interestgroups.ui.screen.components.StandartTextField
import com.larkes.interestgroups.ui.screen.components.PrimaryButton
import com.larkes.interestgroups.ui.theme.Theme
import interestgroups.composeapp.generated.resources.Res
import interestgroups.composeapp.generated.resources.SecondLanding
import kotlinx.coroutines.flow.StateFlow
import org.jetbrains.compose.resources.painterResource

@Composable
fun AboutMeView(
    uiState: StateFlow<AboutMeUIState>,
    onEvent:(LoginUIEvent) -> Unit
){
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
        Box(modifier = Modifier.padding(top = 60.dp, bottom = 20.dp)) {
            Image(
                painter = painterResource(Res.drawable.SecondLanding),
                contentDescription = null,
                modifier = Modifier.fillMaxWidth(),
                contentScale = ContentScale.Crop
            )
            Column(
                modifier = Modifier.padding(horizontal = 20.dp).fillMaxSize(),
                horizontalAlignment = Alignment.CenterHorizontally
            ) {
                Spacer(modifier = Modifier.height(20.dp))
                Text(
                    text = "Создай свой профиль",
                    style = Theme.fonts.titleLarge,
                    textAlign = TextAlign.Center
                )
                Spacer(modifier = Modifier.height(10.dp))
                Text(
                    text = "Для персональных подборок и компаний, которые заинтересованы \n" +
                            "в твоём опыте",
                    style = Theme.fonts.headlineLarge,
                    textAlign = TextAlign.Center
                )
                Spacer(modifier = Modifier.height(20.dp))
                StandartTextField(
                    value = state.name,
                    onValueChange = {
                        onEvent(LoginUIEvent.NameEntered(it))
                    },
                    hint = "Имя Фамилия",
                    modifier = Modifier.fillMaxWidth().height(55.dp)
                )
                Spacer(modifier = Modifier.height(10.dp))
                state.skillsOptions?.let {
                    StandartDropdown(
                        modifier = Modifier.sizeIn(minHeight = 55.dp),
                        values = state.skills,
                        options = it.map { it.title },
                        hint = "Hавыки",
                        onValueChange = {
                            onEvent(LoginUIEvent.SkillClicked(it))
                        },
                        textColor = Color(0xff308414),
                        textBackgroundColor = Color(0xff45D90C)
                    )
                }
                state.statuesOptions?.let {
                    Spacer(modifier = Modifier.height(10.dp))
                    StandartDropdown(
                        modifier = Modifier.sizeIn(minHeight = 55.dp),
                        values = state.status,
                        options = it.map {item -> item.title },
                        hint = "Статус",
                        onValueChange = {
                            onEvent(LoginUIEvent.StatusClicked(it))
                        },
                        textColor = Color(0xff7F1484),
                        textBackgroundColor = Color(0xffF0DBF7)
                    )
                }

                Spacer(modifier = Modifier.height(10.dp))
                StandartTextField(
                    value = state.aboutMe,
                    onValueChange = {
                        onEvent(LoginUIEvent.AboutMeEntered(it))
                    },
                    hint = "О себе",
                    modifier = Modifier.fillMaxWidth().sizeIn(55.dp),
                    singleLine = false
                )
                Spacer(modifier = Modifier.height(10.dp))
                StandartTextField(
                    value = state.portfolio,
                    onValueChange = {
                        onEvent(LoginUIEvent.ProfileEntered(it))
                    },
                    hint = "Портфолио",
                    modifier = Modifier.fillMaxWidth().sizeIn(55.dp)
                )
                Spacer(modifier = Modifier.height(55.dp))
                PrimaryButton(
                    isPrimary = state.isClickAvailable,
                    text = "Готово"
                ){
                    onEvent(LoginUIEvent.AboutMeDoneClicked)
                }
                Spacer(modifier = Modifier.height(10.dp))
                PrimaryButton(
                    text = "Пропустить"
                ){
                    onEvent(LoginUIEvent.AboutMeDoneClicked)
                }
            }
        }
    }
}