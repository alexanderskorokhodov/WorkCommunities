package com.larkes.interestgroups.ui.screen.components

import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
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
import coil3.compose.AsyncImage
import com.larkes.interestgroups.ui.theme.Theme
import com.larkes.interestgroups.ui.theme.getInterTightFont

@Composable
fun PostView(
    image: String,
    title: String,
    onClick:() -> Unit
){

    Column(
        modifier = Modifier.clickable{
            onClick()
        }
    ) {
        AsyncImage(
            image,
            contentDescription = "",
            modifier = Modifier.fillMaxWidth().height(300.dp).clip(RoundedCornerShape(20.dp)),
            contentScale = ContentScale.Crop,
            onError = { error ->
            },
        )
        Spacer(modifier = Modifier.height(5.dp))
        Text(
            text = title,
            fontFamily = getInterTightFont(),
            fontSize = 24.sp,
            color = Color.Black,
            fontWeight = FontWeight.Normal
        )
    }


}