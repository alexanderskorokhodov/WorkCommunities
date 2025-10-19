package com.larkes.interestgroups.ui.screen.components

import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.focusable
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.text.BasicTextField
import androidx.compose.foundation.text.KeyboardActions
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.material3.Text
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.focus.FocusRequester
import androidx.compose.ui.focus.focusRequester
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.platform.LocalFocusManager
import androidx.compose.ui.text.TextStyle
import androidx.compose.ui.text.input.ImeAction
import androidx.compose.ui.text.input.KeyboardType
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import kotlinx.coroutines.delay
import kotlinx.coroutines.flow.first
import kotlinx.coroutines.launch

@Composable
fun OtpCodeInput(
    code: String,
    length: Int = 4,
    onCodeChange:(String) -> Unit
) {
    val focusRequester = remember { FocusRequester() }

    LaunchedEffect(Unit) {
        focusRequester.requestFocus()
    }

    Box {
        // Скрытый TextField для ввода
        BasicTextField(
            value = code,
            onValueChange = { newValue ->
                val filtered = newValue.filter { it.isDigit() }.take(length)
                onCodeChange(filtered)

            },
            keyboardOptions = KeyboardOptions(
                keyboardType = KeyboardType.Number,
            ),
            textStyle = TextStyle(
                fontSize = 1.sp,
                color = Color.Transparent
            ),
            singleLine = true,
            modifier = Modifier
                .focusRequester(focusRequester)
                .size(1.dp)
        )

        // Визуальное отображение с кликом для фокуса
        Row(
            horizontalArrangement = Arrangement.spacedBy(8.dp),
            modifier = Modifier.clickable {
                focusRequester.requestFocus()
            }
        ) {
            repeat(length) { index ->
                val digit = if (index < code.length) code[index].toString() else ""

                Box(
                    modifier = Modifier
                        .size(60.dp, 72.dp)
                        .border(
                            1.dp,
                            if (digit.isNotEmpty()) Color.Blue else Color.Gray,
                            RoundedCornerShape(12.dp)
                        )
                        .background(Color.White, RoundedCornerShape(12.dp)),
                    contentAlignment = Alignment.Center
                ) {
                    if (digit.isNotEmpty()) {
                        Text(
                            text = digit,
                            fontSize = 22.sp,
                            color = Color.Black,
                            textAlign = TextAlign.Center
                        )
                    } else {
                        Text("•", color = Color.LightGray, fontSize = 20.sp)
                    }
                }
            }
        }
    }
}