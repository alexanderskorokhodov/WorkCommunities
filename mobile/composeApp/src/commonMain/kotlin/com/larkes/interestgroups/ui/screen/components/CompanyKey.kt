package com.larkes.interestgroups.ui.screen.components

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.larkes.interestgroups.ui.theme.getInterTightFont

@Composable
fun CompanyKey(
    title: String,
    solves: Int,
    date: String
){

    Row(
        modifier = Modifier
            .clip(RoundedCornerShape(20.dp))
            .background(Color(0xffF6F6F6))
            .padding(horizontal = 20.dp, vertical = 16.dp),
        horizontalArrangement = Arrangement.SpaceBetween
    ) {
        Column(modifier = Modifier.weight(0.85f)) {
            Text(
                text = title,
                color = Color.Black,
                fontSize = 18.sp,
                fontFamily = getInterTightFont(),
                fontWeight = FontWeight.Normal
            )
            Spacer(modifier = Modifier.height(13.dp))
            Text(
                text = "$solves решений",
                color = Color(0xff2C91C5),
                fontWeight = FontWeight.Normal,
                fontSize = 14.sp,
                fontFamily = getInterTightFont(),
                modifier = Modifier.clip(
                    RoundedCornerShape(9.dp)
                ).background(Color(0xffCDEEFF)).padding(horizontal = 10.dp, vertical = 2.dp)
            )
        }
        Text(
            text = date,
            color = Color(0xff2AABEE),
            fontWeight = FontWeight.Normal,
            fontSize = 16.sp,
            fontFamily = getInterTightFont(),
            modifier = Modifier.weight(0.15f)
        )
    }
}
