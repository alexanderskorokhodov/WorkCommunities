package com.larkes.interestgroups.ui.screen.webinar_screen

import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.Image
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.Button
import androidx.compose.material3.ButtonDefaults
import androidx.compose.material3.CircularProgressIndicator
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.navigation.NavController
import coil3.compose.AsyncImage
import com.larkes.interestgroups.ui.screen.components.PrimaryButton
import com.larkes.interestgroups.ui.theme.Theme
import com.larkes.interestgroups.ui.theme.getInterTightFont
import com.larkes.interestgroups.utils.Constants
import interestgroups.composeapp.generated.resources.Res
import interestgroups.composeapp.generated.resources.arrow_left
import interestgroups.composeapp.generated.resources.bonus
import interestgroups.composeapp.generated.resources.calendar
import interestgroups.composeapp.generated.resources.coin
import interestgroups.composeapp.generated.resources.link
import interestgroups.composeapp.generated.resources.message
import kotlinx.coroutines.delay
import org.jetbrains.compose.resources.painterResource

@Composable
fun WebinarScreen(navController: NavController){

    var showDialog by remember { mutableStateOf(false) }
    var checked by remember { mutableStateOf(false) }

    // Диалог появляется автоматически при заходе на экран
    LaunchedEffect(Unit) {
        delay(1000)
        showDialog = true
    }

    Box(){
        Column(
            modifier = Modifier.padding(horizontal = 20.dp)
        ) {
            Spacer(modifier = Modifier.height(60.dp))

            Image(
                painter = painterResource(Res.drawable.arrow_left),
                contentDescription = null,
                modifier = Modifier
                    .height(19.dp)
                    .width(10.dp)
                    .clickable{
                        navController.popBackStack()
                    },
                contentScale = ContentScale.Crop
            )
            Spacer(modifier = Modifier.height(14.dp))
            LazyColumn(
                modifier = Modifier.fillMaxWidth()
            ) {
                item {
                    AsyncImage(
                        "${Constants.SERVER_URL}/media/45389f36a4ad45568109de7f40701464",
                        contentDescription = "",
                        modifier = Modifier.fillMaxWidth().height(300.dp).clip(RoundedCornerShape(20.dp)),
                        contentScale = ContentScale.Crop,
                        onError = { error ->
                        },
                    )
                    Spacer(modifier = Modifier.height(14.dp))
                    Row(
                        modifier = Modifier
                            .background(Color(0xFFFFFDB6), shape = RoundedCornerShape(10.dp))
                            .padding(horizontal = 10.dp, vertical = 6.dp),
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        Image(
                            painter = painterResource(Res.drawable.coin),
                            contentDescription = null,
                            modifier = Modifier.size(18.dp)
                        )
                        Spacer(modifier = Modifier.width(6.dp))
                        Text(
                            text = "5 баллов начислено",
                            fontFamily = getInterTightFont(),
                            fontWeight = FontWeight.Medium,
                            fontSize = 14.sp,
                            color = Color(0xffE0A100)
                        )
                    }
                }
                item {
                    Spacer(modifier = Modifier.height(14.dp))
                    Text(
                        text = "Онлайн-воркшоп от R-Farm \n" +
                                "с Василием Игнатьевым",
                        fontFamily = getInterTightFont(),
                        fontSize = 24.sp,
                        fontWeight = FontWeight.Normal,
                        color = Color.Black
                    )
                    Spacer(modifier = Modifier.height(10.dp))
                    Text(
                        text = "Уже в эту пятницу приглашаем на встречу с Василием Игнатьевым, экспертом R-Farm по биотехнологическим инновациям.\n" +
                                "\n" +
                                "Разберём реальные кейсы из индустрии, поговорим о карьере в фарме и разложим по полочкам, как молодым специалистам попасть в проекты R-Farm.",
                        fontFamily = getInterTightFont(),
                        fontSize = 16.sp,
                        fontWeight = FontWeight.Normal,
                        color = Color.Black
                    )
                    Spacer(modifier = Modifier.height(14.dp))
                }
                item {
                    Row {
                        Image(
                            painter = painterResource(Res.drawable.calendar),
                            contentDescription = null,
                            modifier = Modifier.width(18.dp).height(20.dp),
                            contentScale = ContentScale.Crop
                        )
                        Spacer(modifier = Modifier.width(9.dp))
                        Text(
                            text = "14 октября, 17:00 (онлайн)",
                            fontFamily = getInterTightFont(),
                            fontSize = 16.sp,
                            fontWeight = FontWeight.Normal,
                            color = Color.Black
                        )
                    }

                    Spacer(modifier = Modifier.height(10.dp))
                }
                item {
                    Row {
                        Image(
                            painter = painterResource(Res.drawable.message),
                            contentDescription = null,
                            modifier = Modifier.width(18.dp).height(18.dp),
                            contentScale = ContentScale.Crop
                        )
                        Spacer(modifier = Modifier.width(9.dp))
                        Text(
                            text = "Формат: открытая сессия + ответы на вопросы",
                            fontFamily = getInterTightFont(),
                            fontSize = 16.sp,
                            fontWeight = FontWeight.Normal,
                            color = Color.Black
                        )
                    }
                    Spacer(modifier = Modifier.height(10.dp))
                }
                item {
                    Row {
                        Image(
                            painter = painterResource(Res.drawable.link),
                            contentDescription = null,
                            modifier = Modifier.width(18.dp).height(18.dp),
                            contentScale = ContentScale.Crop
                        )
                        Spacer(modifier = Modifier.width(9.dp))
                        Text(
                            text = "Регистрация: в сообществе R-Farm BioTech Club",
                            fontFamily = getInterTightFont(),
                            fontSize = 16.sp,
                            fontWeight = FontWeight.Normal,
                            color = Color.Black
                        )
                    }
                    Spacer(modifier = Modifier.height(10.dp))
                }
                item {
                    if(checked){
                        Spacer(modifier = Modifier.height(20.dp))
                        Button(
                            onClick = {
                            },
                            contentPadding = PaddingValues(0.dp),
                            colors = ButtonDefaults.buttonColors(
                                containerColor = Color.White
                            ),
                            border = BorderStroke(1.dp, color = Color(0xff2AABEE)),
                            shape = RoundedCornerShape(20.dp),
                            modifier = Modifier.fillMaxWidth().height(55.dp)
                        ){
                            Text(
                                text = "Просмотрено",
                                style = Theme.fonts.titleMedium,
                                modifier = Modifier.fillMaxWidth().padding(vertical = 13.dp),
                                textAlign = TextAlign.Center,
                                fontSize = 24.sp,
                                color = Color.Black
                            )
                        }
                    }
                }
            }
        }
        if (showDialog) {
            BonusDialog(
                title = "5 баллов начислилось!",
                subtitle = "За просмотр вебинара",
                onDismiss = {
                    checked = true
                    showDialog = false
                }
            )
        }
    }
}