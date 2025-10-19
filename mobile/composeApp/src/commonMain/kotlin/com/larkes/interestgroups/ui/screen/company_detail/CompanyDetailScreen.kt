package com.larkes.interestgroups.ui.screen.company_detail

import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.Image
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxHeight
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.heightIn
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.LazyRow
import androidx.compose.foundation.lazy.itemsIndexed
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.Button
import androidx.compose.material3.ButtonDefaults
import androidx.compose.material3.CircularProgressIndicator
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
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.navigation.NavController
import coil3.compose.AsyncImage
import com.larkes.interestgroups.presentation.company_detail.CompanyDetailViewModel
import com.larkes.interestgroups.ui.navigation.Screens
import com.larkes.interestgroups.ui.screen.components.CaruselItemExstened
import com.larkes.interestgroups.ui.screen.components.PrimaryButton
import com.larkes.interestgroups.ui.theme.Theme
import com.larkes.interestgroups.ui.theme.getInterTightFont
import interestgroups.composeapp.generated.resources.Res
import interestgroups.composeapp.generated.resources.arrow_left
import interestgroups.composeapp.generated.resources.lamp
import org.jetbrains.compose.resources.painterResource

@Composable
fun CompanyDetailScreen(
    navController: NavController,
    viewModel: CompanyDetailViewModel,
    id: String
) {

    val uiState by viewModel.companyDetailUIState.collectAsState()

    LaunchedEffect(id){
        viewModel.getCompany(id)
    }

    Column(
    ) {
        Spacer(modifier = Modifier.height(30.dp))
        Box(
            modifier = Modifier.fillMaxWidth(),
            contentAlignment = Alignment.Center
        ){
            if(uiState.company == null){
                CircularProgressIndicator()
            }
        }
        uiState.company?.let { company ->

            Box(modifier = Modifier.padding(start = 20.dp)) {
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
            }
            Spacer(modifier = Modifier.height(14.dp))
            LazyColumn(
                modifier = Modifier.fillMaxWidth()
            ) {
                item {
                    Text(
                        text = company.title,
                        fontSize = 32.sp,
                        fontWeight = FontWeight.Normal,
                        fontFamily = getInterTightFont(),
                        color = Color.Black,
                        modifier = Modifier.padding(start = 20.dp)
                    )
                    Spacer(modifier = Modifier.height(14.dp))
                    LazyRow(
                        modifier = Modifier.height(140.dp),
                        horizontalArrangement = Arrangement.spacedBy(10.dp)
                    ) {
                        item { Spacer(modifier = Modifier.width(14.dp)) }
                        itemsIndexed(company.images){index, item ->
                            AsyncImage(
                                item,
                                contentDescription = "",
                                modifier = Modifier.width(250.dp).fillMaxHeight().clip(RoundedCornerShape(20.dp)),
                                contentScale = ContentScale.Crop,
                                onError = { error ->
                                },
                            )
                        }
                    }
                }
                item {
                    Spacer(modifier = Modifier.height(20.dp))
                    Text(
                        text = "О компании",
                        fontSize = 24.sp,
                        fontWeight = FontWeight.Normal,
                        fontFamily = getInterTightFont(),
                        color = Color.Black,
                        modifier = Modifier.padding(start = 20.dp)
                    )
                    Spacer(modifier = Modifier.height(12.dp))
                    Text(
                        text = company.about,
                        fontSize = 16.sp,
                        fontWeight = FontWeight.Normal,
                        fontFamily = getInterTightFont(),
                        color = Color.Black,
                        modifier = Modifier.padding(start = 20.dp)
                    )
                    Spacer(modifier = Modifier.height(12.dp))
                    Text(
                        text = "больше",
                        style = Theme.fonts.headlineLarge,
                        modifier = Modifier.fillMaxWidth(),
                        textAlign = TextAlign.Center
                    )
                    Spacer(modifier = Modifier.height(20.dp))
                    Column(modifier = Modifier.padding(horizontal = 20.dp)) {
                        Row(
                            modifier = Modifier
                                .fillMaxWidth()
                                .border(BorderStroke(1.dp, Theme.colors.formBorderColor), RoundedCornerShape(22.dp))
                                .clip(RoundedCornerShape(22.dp))
                                .padding(vertical = 10.dp, horizontal = 13.dp)
                        ) {
                            Image(
                                painter = painterResource(Res.drawable.lamp),
                                contentDescription = null,
                                modifier = Modifier.size(32.dp),
                                contentScale = ContentScale.Crop
                            )
                            Text(
                                text = company.highlight,
                                fontSize = 14.sp,
                                fontWeight = FontWeight.Normal,
                                fontFamily = getInterTightFont(),
                                color = Color.Black
                            )
                        }
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
                            modifier = Modifier.fillMaxWidth().height(46.dp)
                        ){
                            Text(
                                text = "Вы подписаны на компанию",
                                style = Theme.fonts.titleMedium,
                                modifier = Modifier.fillMaxWidth().padding(vertical = 13.dp),
                                textAlign = TextAlign.Center,
                                fontSize = 18.sp,
                                color = Color.Black
                            )
                        }
                    }
                }
                item {
                    Spacer(modifier = Modifier.height(20.dp))
                    Text(
                        text = "Cообщества",
                        fontSize = 24.sp,
                        fontWeight = FontWeight.Normal,
                        fontFamily = getInterTightFont(),
                        color = Color.Black,
                        modifier = Modifier.padding(horizontal = 20.dp)
                    )
                    Spacer(modifier = Modifier.height(12.dp))
                }
                item {
                    if(uiState.isCommunityLoading){
                        Box(
                            modifier = Modifier.fillMaxWidth(),
                            contentAlignment = Alignment.Center
                        ){
                            CircularProgressIndicator()
                        }
                    }
                    uiState.communities?.let { communities ->
                       LazyRow(
                           modifier = Modifier.heightIn(min = 280.dp),
                           horizontalArrangement = Arrangement.spacedBy(10.dp)
                       ) {
                           item { Spacer(modifier = Modifier.width(14.dp)) }
                           itemsIndexed(communities){index, item ->
                               CaruselItemExstened(
                                   image = item.image,
                                   title = item.title,
                                   rightTopText = if(item.isNew) "New" else null,
                                   bottomText = listOf("От компании", "Стажировки"),
                                   subtitle = "Разработка систем на чипе, нейросети, IoT",
                                   participants = 125
                               ){
                                navController.navigate(Screens.CommunityDetailScreen(item.id))
                               }
                           }
                       }
                     }
                    Spacer(modifier = Modifier.height(40.dp))
                }
            }
        }
    }

}