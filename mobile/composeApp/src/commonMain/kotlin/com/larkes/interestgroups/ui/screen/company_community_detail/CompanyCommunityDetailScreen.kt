package com.larkes.interestgroups.ui.screen.company_community_detail

import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.Image
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Arrangement
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
import androidx.compose.foundation.lazy.itemsIndexed
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.Button
import androidx.compose.material3.ButtonColors
import androidx.compose.material3.ButtonDefaults
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.navigation.NavController
import com.larkes.interestgroups.presentation.company_community_detail.CompanyCommunityDetailViewModel
import com.larkes.interestgroups.ui.navigation.Screens
import com.larkes.interestgroups.ui.screen.components.CompanyKey
import com.larkes.interestgroups.ui.screen.components.CompanyParticipant
import com.larkes.interestgroups.ui.theme.Theme
import com.larkes.interestgroups.ui.theme.getInterTightFont
import interestgroups.composeapp.generated.resources.Res
import interestgroups.composeapp.generated.resources.arrow_left
import interestgroups.composeapp.generated.resources.pen
import interestgroups.composeapp.generated.resources.settings
import org.jetbrains.compose.resources.painterResource

@Composable
fun CompanyCommunityDetailScreen(
    navController: NavController,
    viewModel: CompanyCommunityDetailViewModel,
    id: String
){
    val community by viewModel._community.collectAsState()

    LaunchedEffect(Unit){
        viewModel.getCommunity(id)
    }

    Column(
        modifier = Modifier.padding(horizontal = 20.dp)
    ) {
        Spacer(modifier = Modifier.height(40.dp))
        Row(
            modifier = Modifier.fillMaxWidth(),
            horizontalArrangement = Arrangement.SpaceBetween,
            verticalAlignment = Alignment.CenterVertically
        ){
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
                    .size(26.dp)
                    .clickable{
                        navController.popBackStack()
                    },
                contentScale = ContentScale.Crop
            )
        }
        Spacer(modifier = Modifier.height(12.dp))
        community?.let { community ->
            LazyColumn(

            ) {
                item {
                    Row(
                        modifier = Modifier.fillMaxWidth(),
                        horizontalArrangement = Arrangement.SpaceBetween,
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        Text(
                            text = community.name,
                            style = Theme.fonts.titleLarge,
                            fontSize = 32.sp
                        )
                        Image(
                            painter = painterResource(Res.drawable.pen),
                            contentDescription = null,
                            modifier = Modifier.size(18.dp),
                            contentScale = ContentScale.Crop
                        )

                    }
                    Spacer(modifier = Modifier.height(4.dp))
                    Text(
                        text = community.description,
                        style = Theme.fonts.headlineLarge
                    )
                    Spacer(modifier = Modifier.height(20.dp))
                    Button(
                        onClick = {},
                        border = BorderStroke(1.dp, Color(0xff2AABEE)),
                        shape = RoundedCornerShape(16.dp),
                        contentPadding = PaddingValues(vertical = 4.dp),
                        colors = ButtonDefaults.buttonColors(containerColor = Color.White),
                        modifier = Modifier.fillMaxWidth()
                    ){
                        Text(
                            text = "Общий чат",
                            modifier = Modifier.padding(vertical = 9.dp),
                            fontSize = 18.sp,
                            color = Color.Black,
                            fontFamily = getInterTightFont(),
                            fontWeight = FontWeight.Normal
                        )
                    }
                    Spacer(modifier = Modifier.height(29.dp))
                }
                item {
                    Spacer(modifier = Modifier.height(22.dp))
                    Text(
                        text = "\uD83E\uDDD1\uD83C\uDFFB\uFE0F Участники(${community.members.size})",
                        fontSize = 24.sp,
                        fontWeight = FontWeight.Normal,
                        fontFamily = getInterTightFont(),
                        color = Color.Black
                    )
                    Spacer(modifier = Modifier.height(20.dp))
                }
                itemsIndexed(community.members.filter { (it.full_name ?: "").contains("Ксения").not() }){index, item ->
                    Box(modifier = Modifier.clickable{
                        navController.navigate(Screens.CompanyUserProfileScreen(item.id))
                    }){
                        CompanyParticipant(
                            text = item.full_name ?: "",
                            backColor = Color(0xffCDEEFF),
                            color = Color(0xff2AABEE),
                            participantKind = item.role,
                            coins = 320
                        )
                    }
                    Spacer(modifier = Modifier.height(18.dp))
                }
                item {
                    Spacer(modifier = Modifier.height(12.dp))
                    Text(
                        text = "смотреть все",
                        style = Theme.fonts.headlineLarge,
                        modifier = Modifier.fillMaxWidth(),
                        textAlign = TextAlign.Center
                    )
                    Spacer(modifier = Modifier.height(20.dp))
                }
                item {
                    Text(
                        text = "\uD83D\uDCBC Кейсы(${community.cases.size})",
                        fontSize = 24.sp,
                        fontWeight = FontWeight.Normal,
                        fontFamily = getInterTightFont(),
                        color = Color.Black
                    )
                    Spacer(modifier = Modifier.height(18.dp))
                }
                itemsIndexed(community.cases) {index, item ->
                    CompanyKey(
                        title = item.title,
                        solves = item.solutions_count,
                        date = item.date
                    )
                    Spacer(modifier = Modifier.height(10.dp))
                }
                item {
                    Spacer(modifier = Modifier.height(80.dp))
                }
            }
        }
    }

}