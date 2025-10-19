package com.larkes.interestgroups.ui.screen.components

import androidx.compose.foundation.Image
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.larkes.interestgroups.ui.theme.getInterTightFont
import interestgroups.composeapp.generated.resources.Res
import interestgroups.composeapp.generated.resources.coin
import org.jetbrains.compose.resources.painterResource

@Composable
fun CompanyParticipant(
    text: String,
    backColor: Color,
    color: Color,
    participantKind: String,
    coins: Int
){

    Row(
        horizontalArrangement = Arrangement.spacedBy(10.dp)
    ) {
        Text(
            text = text,
            color = Color.Black,
            fontSize = 18.sp,
            fontFamily = getInterTightFont(),
            fontWeight = FontWeight.Normal
        )
        Text(
            text = participantKind,
            color = color,
            fontWeight = FontWeight.Normal,
            fontSize = 14.sp,
            fontFamily = getInterTightFont(),
            modifier = Modifier.clip(
                RoundedCornerShape(9.dp)
            ).background(backColor).padding(horizontal = 10.dp, vertical = 2.dp)
        )
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
                text = coins.toString(),
                color = Color(0xffE0A100),
                fontWeight = FontWeight.Normal,
                fontSize = 14.sp,
                fontFamily = getInterTightFont()
            )
        }

    }

}