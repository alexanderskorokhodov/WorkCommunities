package com.larkes.interestgroups.ui.screen.company_profile

import androidx.compose.foundation.Image
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.heightIn
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.navigation.NavController
import coil3.compose.AsyncImage
import com.larkes.interestgroups.presentation.company_profile.CompanyProfileViewModel
import com.larkes.interestgroups.presentation.login.models.LoginUIEvent
import com.larkes.interestgroups.ui.screen.components.StandartDropdown
import com.larkes.interestgroups.ui.screen.components.StandartTextField
import com.larkes.interestgroups.ui.theme.getInterTightFont
import interestgroups.composeapp.generated.resources.Res
import interestgroups.composeapp.generated.resources.settings
import org.jetbrains.compose.resources.painterResource

@Composable
fun CompanyProfileScreen(
    viewModel: CompanyProfileViewModel,
    navController: NavController
){
    val uiState by viewModel.uiState.collectAsState()

    Box(
        modifier = Modifier
            .padding(horizontal = 20.dp)
            .padding(top = 50.dp)
    ){
        Column(
            modifier = Modifier.fillMaxWidth(),
            horizontalAlignment = Alignment.CenterHorizontally
        ) {
            uiState.image?.let {
                AsyncImage(
                    it,
                    contentDescription = "",
                    modifier = Modifier.size(130.dp).clip(RoundedCornerShape(100)),
                    contentScale = ContentScale.Crop,
                    onError = { error ->
                    },
                )
            }
            Spacer(modifier = Modifier.height(12.dp))
            Text(
                text = uiState.companyName,
                fontFamily = getInterTightFont(),
                fontSize = 32.sp,
                color = Color.Black,
                fontWeight = FontWeight.Normal
            )
            Spacer(modifier = Modifier.height(12.dp))
            StandartTextField(
                value = uiState.description,
                onValueChange = {

                },
                hint = "",
                modifier = Modifier.heightIn(min = 55.dp),
                label = "Описание"
            )
            Spacer(modifier = Modifier.height(12.dp))
            StandartDropdown(
                values = uiState.specialities,
                options = listOf("Хим. инженерия", "ХимТех", "Робототехника", "Инженерия"),
                hint = "Специализация",
                label = "Специализация",
                onValueChange = {
                },
                textColor = Color(0xff7F1484),
                textBackgroundColor = Color(0xffF0DBF7)
            )
        }
        Image(
            painter = painterResource(Res.drawable.settings),
            contentDescription = null,
            modifier = Modifier.size(26.dp).align(Alignment.TopEnd),
            contentScale = ContentScale.Crop
        )
    }
}