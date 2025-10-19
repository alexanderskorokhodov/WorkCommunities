package com.larkes.interestgroups.ui.screen.main

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Arrangement
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
import androidx.compose.foundation.lazy.LazyRow
import androidx.compose.foundation.lazy.itemsIndexed
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.SolidColor
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.navigation.NavController
import coil3.compose.AsyncImage
import com.larkes.interestgroups.presentation.main.MainViewModel

import com.larkes.interestgroups.ui.navigation.Screens
import com.larkes.interestgroups.ui.screen.components.CaruselItem
import com.larkes.interestgroups.ui.screen.components.FancyLoader
import com.larkes.interestgroups.ui.screen.components.PostView
import com.larkes.interestgroups.ui.screen.components.SearchTextField
import com.larkes.interestgroups.ui.theme.Theme
import com.larkes.interestgroups.ui.theme.getInterTightFont

@Composable
fun MainScreen(
    navController: NavController,
    viewModel: MainViewModel
) {

    val uiState by viewModel.uiState.collectAsState()

    Column(
        modifier = Modifier.fillMaxSize()
    ) {

        Spacer(modifier = Modifier.height(40.dp))

        LazyRow(
            modifier = Modifier.height(82.dp),
            horizontalArrangement = Arrangement.spacedBy(6.dp)
        ) {
            item { Spacer(modifier = Modifier.width(20.dp)) }
            itemsIndexed(listOf(
                "https://zzbo.ru/wp-content/uploads/2023/04/4V2A1959.jpg",
                "https://www.stanki-zavod.ru/pic/news/title/64.jpg",
                "https://www.stanki-zavod.ru/pic/news/title/157.jpg",
                "https://all-events.ru/upload/iblock/366/36v0spu9r2ac2oovdofxp5ghyqq7datp.jpg",
                "https://pzmzavod.ru/uploads/2024/10/cifrovye-tehnologii-v-proizvodstve-put-k-effektivnosti.webp"
            )){index, item ->
                AsyncImage(
                    item,
                    contentDescription = "",
                    modifier = Modifier.fillMaxWidth().size(80.dp).clip(RoundedCornerShape(100)),
                    contentScale = ContentScale.Crop,
                    onError = { error ->
                    },
                )
            }
        }

        Column(modifier = Modifier.padding(horizontal = 20.dp)) {
            Spacer(modifier = Modifier.height(20.dp))
            SearchTextField(
                value = "",
                hint = "Компания или событие",
                onValueChange = {},
                modifier = Modifier.fillMaxWidth().height(50.dp)
            )
        }
        Spacer(modifier = Modifier.height(20.dp))
        LazyColumn{
            item {
                if(uiState.posts.isEmpty()){
                   Box(modifier = Modifier.fillMaxWidth(), contentAlignment = Alignment.Center){
                       FancyLoader(
                           modifier = Modifier.size(200.dp)
                       )
                   }
                }
            }
            itemsIndexed(uiState.posts){index, item ->
                Column(modifier = Modifier.padding(horizontal = 20.dp)){
                    PostView(
                        image = item.image,
                        title = item.title
                    ){
                        navController.navigate(Screens.PostDetailScreen(item.id))
                    }
                    Spacer(modifier = Modifier.height(20.dp))
                }
            }
            item{
               Column (
                   modifier = Modifier.padding(start = 20.dp)
               ) {
                   Spacer(modifier = Modifier.height(12.dp))
                   Text(
                       text = "больше",
                       style = Theme.fonts.headlineLarge,
                       modifier = Modifier.fillMaxWidth(),
                       textAlign = TextAlign.Center
                   )
                   Spacer(modifier = Modifier.height(40.dp))
                   Text(
                       text = "Компании по твоей специальности",
                       fontSize = 24.sp,
                       fontWeight = FontWeight.Normal,
                       color = Color.Black,
                       fontFamily = getInterTightFont(),
                       textAlign = TextAlign.Start
                   )
                   Spacer(modifier = Modifier.height(12.dp))
               }
            }
            item {
                if(uiState.communities.isEmpty()){
                    Box(modifier = Modifier.fillMaxWidth(), contentAlignment = Alignment.Center){
                        FancyLoader(
                            modifier = Modifier.size(200.dp)
                        )
                    }
                }
            }
            item{
                LazyRow(
                    modifier = Modifier.height(210.dp),
                    horizontalArrangement = Arrangement.spacedBy(10.dp)
                ) {
                    item { Spacer(modifier = Modifier.width(10.dp)) }
                    itemsIndexed(uiState.companies.reversed()){index, item ->
                        CaruselItem(
                            image = item.image,
                            leftTopText = item.logo,
                            bottomText = item.highlight,
                            title = item.title,
                            bottomBackText = Color(0xffCDEEFF),
                            bottomColorText = Color(0xff2AABEE)
                        ){
                            navController.navigate(Screens.CompanyDetailScreen(item.id))
                        }
                    }
                }
            }

            item {
                Spacer(modifier = Modifier.height(12.dp))
                Text(
                    text = "смотреть все",
                    style = Theme.fonts.headlineLarge,
                    modifier = Modifier.fillMaxWidth(),
                    textAlign = TextAlign.Center
                )
                Spacer(modifier = Modifier.height(32.dp))
            }
            item {
                Text(
                    text = "Сообщества, к которым можно присоединиться",
                    fontSize = 24.sp,
                    fontWeight = FontWeight.Normal,
                    color = Color.Black,
                    fontFamily = getInterTightFont(),
                    textAlign = TextAlign.Start,
                    modifier = Modifier.padding(start = 20.dp)
                )
                Spacer(modifier = Modifier.height(12.dp))
                if(uiState.communities.isEmpty()){
                    Box(modifier = Modifier.fillMaxWidth(), contentAlignment = Alignment.Center){
                        FancyLoader(
                            modifier = Modifier.size(200.dp)
                        )
                    }
                }
                LazyRow(
                    modifier = Modifier.height(210.dp),
                    horizontalArrangement = Arrangement.spacedBy(10.dp)
                ) {
                    item { Spacer(modifier = Modifier.width(10.dp)) }
                    itemsIndexed(uiState.communities){index, item ->
                        CaruselItem(
                            image = item.image,
                            leftTopText = item.logo,
                            rightTopText = "New",
                            bottomText = item.highlight,
                            title = item.title
                        ){
                            navController.navigate(Screens.CommunityDetailScreen(item.id))
                        }
                    }
                }
            }
            item {
                Spacer(modifier = Modifier.height(12.dp))
                Text(
                    text = "смотреть все",
                    style = Theme.fonts.headlineLarge,
                    modifier = Modifier.fillMaxWidth(),
                    textAlign = TextAlign.Center
                )
                Spacer(modifier = Modifier.height(32.dp))
            }
            item {
                Text(
                    text = "Ближайшие события",
                    fontSize = 24.sp,
                    fontWeight = FontWeight.Normal,
                    color = Color.Black,
                    fontFamily = getInterTightFont(),
                    textAlign = TextAlign.Start,
                    modifier = Modifier.padding(start = 20.dp)
                )
                Spacer(modifier = Modifier.height(12.dp))
                if(uiState.events.isEmpty()){
                    Box(modifier = Modifier.fillMaxWidth(), contentAlignment = Alignment.Center){
                        FancyLoader(
                            modifier = Modifier.size(200.dp)
                        )
                    }
                }
                LazyRow(
                    modifier = Modifier.height(210.dp),
                    horizontalArrangement = Arrangement.spacedBy(10.dp)
                ) {
                    item { Spacer(modifier = Modifier.width(10.dp)) }
                    itemsIndexed(uiState.events){index, item ->
                        CaruselItem(
                            image = item.image,
                            rightTopText = item.date,
                            bottomText = item.highlight,
                            title = item.title
                        ){

                        }
                    }
                }
            }
            item {
                Spacer(modifier = Modifier.height(12.dp))
                Text(
                    text = "смотреть все",
                    style = Theme.fonts.headlineLarge,
                    modifier = Modifier.fillMaxWidth(),
                    textAlign = TextAlign.Center
                )
                Spacer(modifier = Modifier.height(32.dp))
            }
            item {
                Spacer(modifier = Modifier.height(60.dp))
            }
        }
    }

}