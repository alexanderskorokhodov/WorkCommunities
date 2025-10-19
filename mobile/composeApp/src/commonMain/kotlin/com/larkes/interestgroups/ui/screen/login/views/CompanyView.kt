package com.larkes.interestgroups.ui.screen.login.views

import androidx.compose.foundation.Image
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.larkes.interestgroups.presentation.login.models.CompanyUIState
import com.larkes.interestgroups.presentation.login.models.LoginUIEvent
import com.larkes.interestgroups.ui.screen.components.PrimaryButton
import com.larkes.interestgroups.ui.screen.components.StandartDropdown
import com.larkes.interestgroups.ui.screen.components.StandartTextField
import com.larkes.interestgroups.ui.theme.Theme
import interestgroups.composeapp.generated.resources.Res
import interestgroups.composeapp.generated.resources.ThirdLanding
import interestgroups.composeapp.generated.resources.Upload
import interestgroups.composeapp.generated.resources.arrow_left
import kotlinx.coroutines.flow.StateFlow
import org.jetbrains.compose.resources.painterResource

@Composable
fun CompanyView(
    uiState: StateFlow<CompanyUIState>,
    onEvent: (LoginUIEvent) -> Unit
){

    val state by uiState.collectAsState()

    LazyColumn(horizontalAlignment = Alignment.CenterHorizontally) {
        item {
            Spacer(modifier = Modifier.height(60.dp))
            Box(modifier = Modifier.fillMaxWidth().padding(start = 20.dp)) {
                Image(
                    painter = painterResource(Res.drawable.arrow_left),
                    contentDescription = null,
                    modifier = Modifier
                        .height(19.dp)
                        .width(10.dp)
                        .clickable {

                        },
                    contentScale = ContentScale.Crop
                )
            }
            Text(
                text = "Заполните даннные о компании",
                style = Theme.fonts.titleLarge,
                textAlign = TextAlign.Center,
                modifier = Modifier.fillMaxWidth(),
                lineHeight = 50.sp
            )
        }
        item {
            Box(modifier = Modifier.fillMaxWidth(), contentAlignment = Alignment.Center){
                Image(
                    painter = painterResource(Res.drawable.ThirdLanding),
                    contentDescription = null,
                    modifier = Modifier.fillMaxWidth(),
                    contentScale = ContentScale.Crop
                )
                Column(
                    horizontalAlignment = Alignment.CenterHorizontally
                ) {
                    Text(
                        text = "Логотип",
                        style = Theme.fonts.headlineMedium
                    )
                    Spacer(modifier = Modifier.height(6.dp))
                    Image(
                        painter = painterResource(Res.drawable.Upload),
                        contentDescription = null,
                        modifier = Modifier.size(81.dp),
                        contentScale = ContentScale.Crop
                    )
                }
            }
        }
        item {
            Column(
                modifier = Modifier.padding(horizontal = 20.dp)
            ) {
                Spacer(modifier = Modifier.height(12.dp))
                StandartTextField(
                    value = state.companyName,
                    hint = "AO...",
                    onValueChange = {
                        onEvent(LoginUIEvent.CompanyNameEntered(it))
                    },
                    label = "Название компании *",
                    modifier = Modifier.height(55.dp)
                )
                Spacer(modifier = Modifier.height(12.dp))
                StandartTextField(
                    value = state.description,
                    hint = "Подробный текст",
                    onValueChange = {
                        onEvent(LoginUIEvent.CompanyDescriptionEntered(it))
                    },
                    label = "Описание деятельности",
                    modifier = Modifier.height(55.dp)
                )
                Spacer(modifier = Modifier.height(12.dp))
                StandartDropdown(
                    values = state.specialities,
                    options = listOf("Хим. инженерия", "ХимТех", "Робототехника", "Инженерия"),
                    hint = "Специализация",
                    label = "Специализация",
                    onValueChange = {
                        onEvent(LoginUIEvent.CompanySpecialAdded(it))
                    },
                    textColor = Color(0xff7F1484),
                    textBackgroundColor = Color(0xffF0DBF7)
                )
            }
        }
        item {
            Column(
                modifier = Modifier.padding(horizontal = 20.dp)
            ) {
                Spacer(modifier = Modifier.height(32.dp))
                PrimaryButton(
                    isPrimary = state.isAvailable,
                    text = "Готово"
                ){
                    onEvent(LoginUIEvent.CompanyDoneClicked)
                }
                Spacer(modifier = Modifier.height(30.dp))
            }
        }
    }
}