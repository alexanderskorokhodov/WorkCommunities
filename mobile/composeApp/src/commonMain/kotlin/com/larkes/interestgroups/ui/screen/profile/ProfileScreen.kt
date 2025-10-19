package com.larkes.interestgroups.ui.screen.profile

import androidx.compose.foundation.Image
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
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
import com.larkes.interestgroups.ui.theme.getInterTightFont
import interestgroups.composeapp.generated.resources.Res
import interestgroups.composeapp.generated.resources.settings
import org.jetbrains.compose.resources.painterResource

@Composable
fun ProfileScreen(
    navController: NavController
){

    Box(
        modifier = Modifier
            .padding(horizontal = 20.dp)
            .padding(top = 50.dp)
    ){
        Column(
            modifier = Modifier.fillMaxWidth(),
            horizontalAlignment = Alignment.CenterHorizontally
        ) {
            AsyncImage(
                "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQoFRQjM-wM_nXMA03AGDXgJK3VeX7vtD3ctA&s",
                contentDescription = "",
                modifier = Modifier.size(130.dp).clip(RoundedCornerShape(100)),
                contentScale = ContentScale.Crop,
                onError = { error ->
                },
            )
            Spacer(modifier = Modifier.height(12.dp))
            Text(
                text = "Ксения Хакатонова",
                fontFamily = getInterTightFont(),
                fontSize = 32.sp,
                color = Color.Black,
                fontWeight = FontWeight.Normal
            )
            Spacer(modifier = Modifier.height(12.dp))
            Column(modifier = Modifier.fillMaxWidth().padding(start = 20.dp)) {
                Text(
                    text = "Ты участвуешь в",
                    fontFamily = getInterTightFont(),
                    fontSize = 18.sp,
                    color = Color.Black,
                    fontWeight = FontWeight.Normal,
                    modifier = Modifier.fillMaxWidth()
                )
                Spacer(modifier = Modifier.height(10.dp))
                Row {
                    Text(
                        text = "3 сообществах",
                        modifier = Modifier
                            .background(Color(0xffF0DBF7), RoundedCornerShape(6.dp))
                            .padding(horizontal = 10.dp, vertical = 6.dp),
                        fontSize = 20.sp,
                        color = Color.Black
                    )
                    Spacer(modifier = Modifier.width(10.dp))
                    Text(
                        text = "1 cобытие",
                        modifier = Modifier
                            .background(Color(0xffCDEEFF), RoundedCornerShape(6.dp))
                            .padding(horizontal = 10.dp, vertical = 6.dp),
                        fontSize = 20.sp,
                        color = Color.Black
                    )
                }
            }
        }
        Image(
            painter = painterResource(Res.drawable.settings),
            contentDescription = null,
            modifier = Modifier.size(26.dp).align(Alignment.TopEnd),
            contentScale = ContentScale.Crop
        )
    }

}