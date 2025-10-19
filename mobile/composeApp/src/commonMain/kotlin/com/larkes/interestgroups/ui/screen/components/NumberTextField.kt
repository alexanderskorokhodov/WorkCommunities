package com.larkes.interestgroups.ui.screen.components

import androidx.compose.foundation.Image
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.defaultMinSize
import androidx.compose.foundation.layout.fillMaxHeight
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.text.BasicTextField
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.SolidColor
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.text.TextStyle
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.larkes.interestgroups.ui.theme.Theme
import com.larkes.interestgroups.ui.theme.getInterTightFont
import interestgroups.composeapp.generated.resources.Res
import interestgroups.composeapp.generated.resources.flag
import org.jetbrains.compose.resources.painterResource

@Composable
fun NumberTextField(
    value: String,
    onValueChange: (String) -> Unit,
    hint: String,
    modifier: Modifier = Modifier,
    textFieldModifier: Modifier = Modifier
        .fillMaxWidth()
        .defaultMinSize(minHeight = 20.dp),
    singleLine: Boolean = false
){
    Row (
        modifier = modifier.clip(RoundedCornerShape(100.dp)).background(Theme.colors.primary).border(1.dp, Theme.colors.formBorderColor,
            RoundedCornerShape(100.dp)),
        verticalAlignment = Alignment.CenterVertically

    ) {
        Spacer(modifier = Modifier.width(24.dp))
        Image(
            painter = painterResource(Res.drawable.flag),
            contentDescription = null,
            modifier = Modifier.width(28.dp).height(18.dp),
            contentScale = ContentScale.Crop
        )
        Spacer(modifier = Modifier.width(5.dp))
        Text(
            text = "+7",
            fontFamily = getInterTightFont(),
            fontWeight = FontWeight.Normal,
            color = Theme.colors.title,
            fontSize = 16.sp
        )
        Spacer(modifier = Modifier.width(12.dp))
        Box(){
            Box(modifier = Modifier.fillMaxHeight(), contentAlignment = Alignment.Center){
                BasicTextField(
                    value = value,
                    onValueChange = onValueChange,
                    textStyle = Theme.fonts.headlineLarge.copy(Theme.colors.title),
                    modifier = textFieldModifier,
                    cursorBrush = SolidColor(Theme.colors.hint),
                    singleLine = singleLine,
                    )
           }
            if (value.isEmpty()) {
                Box(modifier = Modifier.fillMaxHeight(), contentAlignment = Alignment.Center) {
                    Text(
                        text = hint,
                        style = Theme.fonts.headlineLarge
                    )
                }
            }
        }
    }
}