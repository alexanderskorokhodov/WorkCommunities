package com.larkes.interestgroups.ui.screen.components

import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.Button
import androidx.compose.material3.ButtonDefaults
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import com.larkes.interestgroups.ui.theme.Theme

@Composable
fun PrimaryButton(
    text: String,
    isPrimary: Boolean = false,
    onClick:() -> Unit
){
    Button(
        onClick = {
            onClick()
        },
        contentPadding = PaddingValues(0.dp),
        colors = ButtonDefaults.buttonColors(
            containerColor = if(isPrimary) Theme.colors.secondary else Theme.colors.formBorderColor
        ),
        shape = RoundedCornerShape(20.dp),
        modifier = Modifier.fillMaxWidth().height(55.dp)
    ){
        Text(
            text = text,
            style = Theme.fonts.titleMedium,
            modifier = Modifier.fillMaxWidth().padding(vertical = 13.dp),
            textAlign = TextAlign.Center,
            color = if(isPrimary) Color.White else Color.Black
        )
    }
}