package com.larkes.interestgroups.ui.screen.post_detail

import androidx.compose.foundation.Image
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.shape.RoundedCornerShape
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
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.navigation.NavController
import coil3.compose.AsyncImage
import com.larkes.interestgroups.presentation.post_detail.PostDetailViewModel
import com.larkes.interestgroups.ui.screen.components.PrimaryButton
import com.larkes.interestgroups.ui.theme.getInterTightFont
import interestgroups.composeapp.generated.resources.Res
import interestgroups.composeapp.generated.resources.arrow_left
import interestgroups.composeapp.generated.resources.calendar
import interestgroups.composeapp.generated.resources.coin
import interestgroups.composeapp.generated.resources.link
import interestgroups.composeapp.generated.resources.message
import org.jetbrains.compose.resources.painterResource

@Composable
fun PostDetailScreen(
    navController: NavController,
    viewModel: PostDetailViewModel,
    id: String
){

    val uiState by viewModel.uiState.collectAsState()

    LaunchedEffect(id){
        viewModel.getPost(id)
    }

    Column(
        modifier = Modifier.padding(horizontal = 20.dp)
    ) {
        Spacer(modifier = Modifier.height(60.dp))
        Box(
            modifier = Modifier.fillMaxWidth(),
            contentAlignment = Alignment.Center
        ){
            if(uiState.post == null){
                CircularProgressIndicator()
            }
        }
        uiState.post?.let { post ->
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
            Spacer(modifier = Modifier.height(25.dp))
            LazyColumn(
                modifier = Modifier.fillMaxWidth()
            ) {
                item {
                    AsyncImage(
                        post.image,
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
                            text = "5 баллов начислится",
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
                        text = post.title,
                        fontFamily = getInterTightFont(),
                        fontSize = 24.sp,
                        fontWeight = FontWeight.Normal,
                        color = Color.Black
                    )
                    Spacer(modifier = Modifier.height(10.dp))
                    Text(
                        text = post.text,
                        fontFamily = getInterTightFont(),
                        fontSize = 16.sp,
                        fontWeight = FontWeight.Normal,
                        color = Color.Black
                    )
                    Spacer(modifier = Modifier.height(14.dp))
                }
                item {
                    post.date?.let { date ->
                        Row {
                            Image(
                                painter = painterResource(Res.drawable.calendar),
                                contentDescription = null,
                                modifier = Modifier.width(18.dp).height(20.dp),
                                contentScale = ContentScale.Crop
                            )
                            Spacer(modifier = Modifier.width(9.dp))
                            Text(
                                text = date,
                                fontFamily = getInterTightFont(),
                                fontSize = 16.sp,
                                fontWeight = FontWeight.Normal,
                                color = Color.Black
                            )
                        }
                    }
                    Spacer(modifier = Modifier.height(10.dp))
                }
                item {
                    post.format?.let { date ->
                        Row {
                            Image(
                                painter = painterResource(Res.drawable.message),
                                contentDescription = null,
                                modifier = Modifier.width(18.dp).height(18.dp),
                                contentScale = ContentScale.Crop
                            )
                            Spacer(modifier = Modifier.width(9.dp))
                            Text(
                                text = date,
                                fontFamily = getInterTightFont(),
                                fontSize = 16.sp,
                                fontWeight = FontWeight.Normal,
                                color = Color.Black
                            )
                        }
                    }
                    Spacer(modifier = Modifier.height(10.dp))
                }
                item {
                    post.registration?.let { reg ->
                        Row {
                            Image(
                                painter = painterResource(Res.drawable.link),
                                contentDescription = null,
                                modifier = Modifier.width(18.dp).height(18.dp),
                                contentScale = ContentScale.Crop
                            )
                            Spacer(modifier = Modifier.width(9.dp))
                            Text(
                                text = reg,
                                fontFamily = getInterTightFont(),
                                fontSize = 16.sp,
                                fontWeight = FontWeight.Normal,
                                color = Color.Black
                            )
                        }
                    }
                    Spacer(modifier = Modifier.height(10.dp))
                }
                item {
                    Spacer(modifier = Modifier.height(20.dp))
                    PrimaryButton(
                        text = "Записаться",
                        isPrimary = true
                    ){

                    }
                }
            }
        }
    }

}
