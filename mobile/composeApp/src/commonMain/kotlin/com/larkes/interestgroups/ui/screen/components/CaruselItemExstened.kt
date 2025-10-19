package com.larkes.interestgroups.ui.screen.components

import androidx.compose.foundation.Image
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.FlowRow
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
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
import coil3.compose.AsyncImage
import com.larkes.interestgroups.ui.theme.Theme
import com.larkes.interestgroups.ui.theme.getInterTightFont
import interestgroups.composeapp.generated.resources.Res
import interestgroups.composeapp.generated.resources.face
import org.jetbrains.compose.resources.painterResource

@Composable
fun CaruselItemExstened(
    image: String,
    leftTopText: String? = null,
    rightTopText: String? = null,
    bottomText: List<String>? = null,
    title: String,
    subtitle: String,
    participants: Int,
    onClick:() -> Unit
){
    Column(modifier = Modifier
        .width(220.dp)
        .clickable{
            onClick()
        }
    ) {
        Box(modifier = Modifier.fillMaxWidth().height(180.dp)){
            AsyncImage(
                image,
                contentDescription = "",
                modifier = Modifier.fillMaxWidth().height(180.dp).clip(RoundedCornerShape(20.dp)),
                contentScale = ContentScale.Crop,
                onError = { error ->
                },
            )
            Box(
                modifier = Modifier.fillMaxSize().padding(horizontal = 11.dp).padding(top = 10.dp, bottom = 12.dp)
            ){
                leftTopText?.let {
                    Box(modifier = Modifier.align(Alignment.TopStart)){
                        CaruselText(it)
                    }
                }
                rightTopText?.let {
                    Box(modifier = Modifier.align(Alignment.TopEnd)){
                        CaruselText(it)
                    }
                }
                bottomText?.let {
                    FlowRow(
                        modifier = Modifier
                            .align(Alignment.BottomStart)
                            .fillMaxWidth(),
                        verticalArrangement = Arrangement.spacedBy(4.dp),
                        horizontalArrangement = Arrangement.spacedBy(4.dp)
                    ) {
                        it.map {
                                text ->
                            Row {
                                CaruselText(text)
                                Spacer(modifier = Modifier.width(4.dp))
                            }
                        }
                    }
                }

            }
        }
        Spacer(modifier = Modifier.height(5.dp))
        Text(
            text = title,
            fontFamily = getInterTightFont(),
            fontSize = 24.sp,
            color = Color.Black,
            fontWeight = FontWeight.Normal
        )
        Spacer(modifier = Modifier.height(4.dp))
        Text(
            text = subtitle,
            style = Theme.fonts.headlineLarge
        )
        Spacer(modifier = Modifier.height(4.dp))
        Row {
            Image(
                painter = painterResource(Res.drawable.face),
                contentDescription = null,
                modifier = Modifier.width(19.dp).height(22.dp),
                contentScale = ContentScale.Crop
            )
            Spacer(modifier = Modifier.width(4.dp))
            Text(
                text = "$participants участников",
                fontFamily = getInterTightFont(),
                fontSize = 14.sp,
                color = Color.Black,
                fontWeight = FontWeight.Normal
            )
        }
    }
}