package com.larkes.interestgroups.ui.screen.company_user_profile

import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.Image
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.shape.RoundedCornerShape
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
import com.larkes.interestgroups.presentation.company_user_profile.CompanyUserProfileViewModel
import com.larkes.interestgroups.ui.theme.Theme
import com.larkes.interestgroups.ui.theme.getInterTightFont
import com.larkes.interestgroups.utils.Constants
import interestgroups.composeapp.generated.resources.PDF
import interestgroups.composeapp.generated.resources.Res
import interestgroups.composeapp.generated.resources.TG
import interestgroups.composeapp.generated.resources.VK
import interestgroups.composeapp.generated.resources.arrow_left
import interestgroups.composeapp.generated.resources.coin
import interestgroups.composeapp.generated.resources.settings
import org.jetbrains.compose.resources.painterResource

@Composable
fun CompanyUserProfileScreen(
    navController: NavController,
    viewModel: CompanyUserProfileViewModel,
    id: String
){

    val user by viewModel._userData.collectAsState()

    LaunchedEffect(id){
        viewModel.fetchProfile(id)
    }

    user?.let { res ->
        LazyColumn(
            horizontalAlignment = Alignment.CenterHorizontally
        ) {
            item {
                Box(
                    modifier = Modifier
                        .padding(horizontal = 20.dp)
                        .padding(top = 50.dp)
                ){
                    Column(
                        modifier = Modifier.fillMaxWidth(),
                        horizontalAlignment = Alignment.CenterHorizontally
                    ) {
                        println("sdsdvsdv ${Constants.SERVER_URL}/media/${res.avatar_media_id}")
                        AsyncImage(
                            "${Constants.SERVER_URL}/media/${res.avatar_media_id}",
                            contentDescription = "",
                            modifier = Modifier.size(130.dp).clip(RoundedCornerShape(100)),
                            contentScale = ContentScale.Crop,
                            onError = { error ->
                            },
                        )
                        Spacer(modifier = Modifier.height(12.dp))
                        Text(
                            text = res.full_name,
                            fontFamily = getInterTightFont(),
                            fontSize = 32.sp,
                            color = Color.Black,
                            fontWeight = FontWeight.Normal
                        )
                        Spacer(modifier = Modifier.height(12.dp))
                        Box(modifier = Modifier.fillMaxWidth(), contentAlignment = Alignment.Center){
                            Text(
                                text = "20 лет г. Москва",
                                style = Theme.fonts.headlineLarge
                            )
                        }
                    }
                    Image(
                        painter = painterResource(Res.drawable.settings),
                        contentDescription = null,
                        modifier = Modifier.size(26.dp).align(Alignment.TopEnd),
                        contentScale = ContentScale.Crop
                    )
                    Image(
                        painter = painterResource(Res.drawable.arrow_left),
                        contentDescription = null,
                        modifier = Modifier.height(19.dp).width(10.dp)
                            .align(Alignment.TopStart)
                            .clickable{
                                navController.popBackStack()
                            },
                        contentScale = ContentScale.Crop
                    )
                }
                Spacer(modifier = Modifier.height(12.dp))
                Row(horizontalArrangement = Arrangement.spacedBy(4.dp)) {
                    res.skills.map {
                        Text(
                            text = it.title,
                            color = Color(0xff308414),
                            fontWeight = FontWeight.Normal,
                            fontSize = 14.sp,
                            fontFamily = getInterTightFont(),
                            modifier = Modifier.clip(
                                RoundedCornerShape(9.dp)
                            ).background(Color(0xffE5F7DB)).padding(horizontal = 10.dp, vertical = 2.dp)
                        )
                    }

                    Spacer(modifier = Modifier.width(5.dp))
                    Row(
                        modifier = Modifier
                            .clip(RoundedCornerShape(9.dp))
                            .background(Color(0xffFFFDB6))
                            .padding(horizontal = 10.dp, vertical = 2.dp)
                    ) {
                        Image(
                            painter = painterResource(Res.drawable.coin),
                            contentDescription = null,
                            modifier = Modifier.size(14.dp),
                            contentScale = ContentScale.Crop
                        )
                        Spacer(modifier = Modifier.width(4.dp))
                        Text(
                            text = "125",
                            color = Color(0xffE0A100),
                            fontWeight = FontWeight.Normal,
                            fontSize = 14.sp,
                            fontFamily = getInterTightFont()
                        )
                    }
                }
                Spacer(modifier = Modifier.height(20.dp))
                Row (horizontalArrangement = Arrangement.spacedBy(20.dp)){
                    listOf(Pair(Res.drawable.VK, Modifier.size(32.dp)), Pair(Res.drawable.PDF, Modifier.size(50.dp)),
                        Pair(Res.drawable.TG, Modifier.size(32.dp))).map {
                        Box(modifier = Modifier
                            .size(80.dp)
                            .border(BorderStroke(1.dp, Color(0xffD8D8D8)), RoundedCornerShape(30.dp))
                            .clip(RoundedCornerShape(30.dp)),
                            contentAlignment = Alignment.Center
                        ){
                            Image(
                                painter = painterResource(it.first),
                                modifier = it.second,
                                contentDescription = null,
                                contentScale = ContentScale.Crop
                            )
                        }
                    }
                }
                Spacer(modifier = Modifier.height(20.dp))
                Text(
                    text = "О себе",
                    style = Theme.fonts.headlineMedium,
                    modifier = Modifier.fillMaxWidth().padding(start = 20.dp)
                )
                Spacer(modifier = Modifier.height(6.dp))
                Text(
                    text = res.description,
                    style = Theme.fonts.headlineMedium,
                    color = Color.Black,
                    modifier = Modifier.padding(horizontal = 20.dp)
                )
            }
        }
    }

}