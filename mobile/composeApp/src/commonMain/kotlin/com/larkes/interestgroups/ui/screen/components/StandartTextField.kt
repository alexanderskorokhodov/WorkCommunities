package com.larkes.interestgroups.ui.screen.components

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.defaultMinSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.text.BasicTextField
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.SolidColor
import androidx.compose.ui.unit.dp
import com.larkes.interestgroups.ui.theme.Theme

@Composable
fun StandartTextField(
    value: String,
    onValueChange: (String) -> Unit,
    hint: String,
    modifier: Modifier = Modifier,
    textFieldModifier: Modifier = Modifier
        .fillMaxWidth()
        .defaultMinSize(minHeight = 36.dp),
    singleLine: Boolean = false,
    label: String? = null
){

    Column {
        label?.let {
            Text(
                text = it,
                style = Theme.fonts.headlineMedium
            )
            Spacer(modifier = Modifier.height(6.dp))
        }
        Box(
            modifier = modifier
                .clip(RoundedCornerShape(20.dp))
                .background(Color(0xffF6F6F6))
                .padding(start = 22.dp)
                .padding(vertical = 16.dp),
        ){
            BasicTextField(
                value = value,
                onValueChange = onValueChange,
                textStyle = Theme.fonts.headlineLarge.copy(color = Theme.colors.title),
                modifier = textFieldModifier,
                cursorBrush = SolidColor(Theme.colors.hint),
                singleLine = singleLine
            )
            if (value.isEmpty()) {
                Box(contentAlignment = Alignment.Center) {
                    Text(
                        text = hint,
                        style = Theme.fonts.headlineLarge
                    )
                }
            }
        }
    }


}