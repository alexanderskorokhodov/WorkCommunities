package com.larkes.interestgroups.ui.screen.components

import androidx.compose.foundation.Image
import androidx.compose.foundation.background
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
import com.larkes.interestgroups.ui.theme.Theme
import com.larkes.interestgroups.ui.theme.getInterTightFont
import interestgroups.composeapp.generated.resources.Res
import interestgroups.composeapp.generated.resources.coin
import interestgroups.composeapp.generated.resources.pen
import org.jetbrains.compose.resources.painterResource

@Composable
fun CompanyCommunityComponent(
    title: String,
    subtitle: String,
    participents: Int,
    keys: Int,
    solves: Int,
    onClick:() -> Unit
){

    Column(
        modifier = Modifier.clickable{
            onClick()
        }
    ) {
        Row(
            modifier = Modifier.fillMaxWidth(),
            horizontalArrangement = Arrangement.SpaceBetween,
            verticalAlignment = Alignment.CenterVertically
        ) {
            Text(
                text = title,
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
            text = subtitle,
            style = Theme.fonts.headlineLarge
        )
        Spacer(modifier = Modifier.height(12.dp))
        Row {
            Text(
                text = "\uD83E\uDDD1\uD83C\uDFFB ${participents} участников",
                fontSize = 16.sp,
                color = Color.Black,
                fontFamily = getInterTightFont(),
                fontWeight = FontWeight.Normal
            )
            Spacer(modifier = Modifier.width(12.dp))
            Text(
                text = "\uD83D\uDCBC $keys кейс",
                fontSize = 16.sp,
                color = Color.Black,
                fontFamily = getInterTightFont(),
                fontWeight = FontWeight.Normal
            )
            Spacer(modifier = Modifier.width(12.dp))
            Text(
                text = "+$solves решений",
                color = Color(0xff2C91C5),
                fontWeight = FontWeight.Normal,
                fontSize = 14.sp,
                fontFamily = getInterTightFont(),
                modifier = Modifier.clip(
                    RoundedCornerShape(9.dp)
                ).background(Color(0xffCDEEFF)).padding(horizontal = 10.dp, vertical = 2.dp)
            )
        }
    }

}