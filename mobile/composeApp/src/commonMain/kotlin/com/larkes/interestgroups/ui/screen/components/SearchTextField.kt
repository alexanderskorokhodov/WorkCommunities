package com.larkes.interestgroups.ui.screen.components

import androidx.compose.foundation.Image
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.defaultMinSize
import androidx.compose.foundation.layout.fillMaxHeight
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
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
import androidx.compose.ui.unit.dp
import com.larkes.interestgroups.ui.theme.Theme
import interestgroups.composeapp.generated.resources.Res
import interestgroups.composeapp.generated.resources.search
import org.jetbrains.compose.resources.painterResource

@Composable
fun SearchTextField(
    value: String,
    onValueChange: (String) -> Unit,
    hint: String,
    modifier: Modifier = Modifier,
    textFieldModifier: Modifier = Modifier
        .fillMaxWidth()
        .defaultMinSize(minHeight = 26.dp),
    singleLine: Boolean = false
){

    Row(modifier = Modifier
        .fillMaxWidth()
        .clip(RoundedCornerShape(100.dp)).background(Theme.colors.primary).border(1.dp, Theme.colors.formBorderColor,
        RoundedCornerShape(100.dp)),
        verticalAlignment = Alignment.CenterVertically
        ) {
        Box(
            modifier = modifier
                .fillMaxHeight()
                .padding(start = 16.dp)
                .weight(0.85f),
        ){
            Box(modifier = Modifier.fillMaxHeight(), contentAlignment = Alignment.Center){
                BasicTextField(
                    value = value,
                    onValueChange = onValueChange,
                    textStyle = Theme.fonts.headlineLarge,
                    modifier = textFieldModifier,
                    cursorBrush = SolidColor(Theme.colors.hint),
                    singleLine = singleLine
                )
                if (value.isEmpty()) {
                    Text(
                        text = hint,
                        style = Theme.fonts.headlineLarge,
                        modifier = Modifier.fillMaxWidth()
                    )
                }
            }
        }
        Box(
            modifier = Modifier.weight(0.15f)
        ) {
            Image(
                painter = painterResource(Res.drawable.search),
                contentDescription = null,
                modifier = Modifier.size(30.dp),
                contentScale = ContentScale.Crop
            )
        }

    }

}