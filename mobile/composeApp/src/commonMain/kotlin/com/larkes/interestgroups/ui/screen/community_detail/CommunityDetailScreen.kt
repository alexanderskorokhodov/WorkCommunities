package com.larkes.interestgroups.ui.screen.community_detail

import androidx.compose.foundation.Image
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.itemsIndexed
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.Card
import androidx.compose.material3.CardDefaults
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
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
import com.larkes.interestgroups.presentation.community_detail.CommunityDetailViewModel
import com.larkes.interestgroups.ui.navigation.Screens
import com.larkes.interestgroups.ui.screen.components.PrimaryButton
import com.larkes.interestgroups.ui.theme.Theme
import com.larkes.interestgroups.ui.theme.getInterTightFont
import com.larkes.interestgroups.utils.Constants
import interestgroups.composeapp.generated.resources.Res
import interestgroups.composeapp.generated.resources.arrow_left
import interestgroups.composeapp.generated.resources.coin
import interestgroups.composeapp.generated.resources.settings
import org.jetbrains.compose.resources.painterResource

@Composable
fun CommunityDetailScreen(
    viewModel: CommunityDetailViewModel,
    navController: NavController,
    id: String
){

    val uiState by viewModel.community.collectAsState()

    LaunchedEffect(Unit){
        viewModel.getCommunity(id)
    }

    uiState?.let { community ->
        LazyColumn(
            modifier = Modifier.padding(horizontal = 20.dp)
        ) {
            item {
                Spacer(modifier = Modifier.height(30.dp))
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.SpaceBetween
                ) {
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
                    Image(
                        painter = painterResource(Res.drawable.settings),
                        contentDescription = null,
                        modifier = Modifier
                            .size(27.dp)
                            .clickable{

                            },
                        contentScale = ContentScale.Crop
                    )
                }
            }
            item {
                Spacer(modifier = Modifier.height(12.dp))
                Text(
                    text = community.name,
                    fontFamily = getInterTightFont(),
                    fontWeight = FontWeight.Normal,
                    fontSize = 32.sp,
                    color = Color.Black
                )
                Spacer(modifier = Modifier.height(4.dp))
                Text(
                    text = "\uD83E\uDDD1\uD83C\uDFFB\uFE0F 140 участников",
                    fontFamily = getInterTightFont(),
                    fontWeight = FontWeight.Normal,
                    fontSize = 16.sp,
                    color = Color.Black
                )
                Spacer(modifier = Modifier.height(4.dp))
                Text(
                    text = community.description,
                    style = Theme.fonts.headlineLarge
                )
                Spacer(modifier = Modifier.height(20.dp))
                PrimaryButton(
                    text = "Общий чат",
                    isPrimary = true
                ){
                    viewModel.subscribe()
                }
            }
            item {
                Spacer(modifier = Modifier.height(20.dp))
                Text(
                    text = "\uD83D\uDCBC Keйсы(${community.cases.size})"
                )
            }
            itemsIndexed(community.cases) {index, item ->
                Card(
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(horizontal = 20.dp, vertical = 10.dp),
                    shape = RoundedCornerShape(16.dp),
                    colors = CardDefaults.cardColors(
                        containerColor = Color(0xFFF6F6F6)
                    ),
                    elevation = CardDefaults.cardElevation(defaultElevation = 0.dp)
                ) {
                    Row(
                        modifier = Modifier
                            .fillMaxWidth()
                            .padding(horizontal = 16.dp, vertical = 14.dp),
                        horizontalArrangement = Arrangement.SpaceBetween,
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        Column(
                            modifier = Modifier.weight(1f)
                        ) {
                            Text(
                                text = item.title,
                                fontFamily = getInterTightFont(),
                                fontWeight = FontWeight.SemiBold,
                                fontSize = 18.sp,
                                color = Color.Black
                            )

                            Spacer(modifier = Modifier.height(10.dp))

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
                                    text = "Начислено 30 баллов",
                                    fontFamily = getInterTightFont(),
                                    fontWeight = FontWeight.Medium,
                                    fontSize = 14.sp,
                                    color = Color.Black
                                )
                            }
                        }

                        Spacer(modifier = Modifier.width(10.dp))

                        Text(
                            text = "12.12",
                            color = Color(0xFF2AABEE),
                            fontWeight = FontWeight.Medium,
                            fontFamily = getInterTightFont(),
                            fontSize = 14.sp
                        )
                    }
                }
            }
            item {
                Spacer(modifier = Modifier.height(20.dp))
                Column(
                    modifier = Modifier.clickable{
                        navController.navigate(Screens.WebinarScreen)
                    }
                ) {
                    AsyncImage(
                        "${Constants.SERVER_URL}/media/45389f36a4ad45568109de7f40701464",
                        contentDescription = "",
                        modifier = Modifier.fillMaxWidth().height(300.dp).clip(RoundedCornerShape(20.dp)),
                        contentScale = ContentScale.Crop,
                        onError = { error ->
                        },
                    )
                    Spacer(modifier = Modifier.height(5.dp))
                    Text(
                        text = "Онлайн-воркшоп от Микрон\n" +
                                "с Гришаевым Леонидом",
                        fontFamily = getInterTightFont(),
                        fontSize = 24.sp,
                        color = Color.Black,
                        fontWeight = FontWeight.Normal
                    )
                }
                Spacer(modifier = Modifier.height(20.dp))
                Column(
                    modifier = Modifier.clickable{
                        navController.navigate(Screens.WebinarScreen)
                    }
                ) {
                    AsyncImage(
                        "${Constants.SERVER_URL}/media/759c01e031744dca9d6436a8d24accb8",
                        contentDescription = "",
                        modifier = Modifier.fillMaxWidth().height(300.dp).clip(RoundedCornerShape(20.dp)),
                        contentScale = ContentScale.Crop,
                        onError = { error ->
                        },
                    )
                    Spacer(modifier = Modifier.height(5.dp))
                    Text(
                        text = "Аналитическое мышление и аккуратность — ошибки в 0.1 мм решают всё.",
                        fontFamily = getInterTightFont(),
                        fontSize = 24.sp,
                        color = Color.Black,
                        fontWeight = FontWeight.Normal
                    )
                }
            }
        }
    }

}