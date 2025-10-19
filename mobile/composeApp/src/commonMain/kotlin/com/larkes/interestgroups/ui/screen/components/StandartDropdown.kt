package com.larkes.interestgroups.ui.screen.components

import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.FlowRow
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.DropdownMenu
import androidx.compose.material3.DropdownMenuItem
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.larkes.interestgroups.ui.theme.Theme

@Composable
fun StandartDropdown(
    values: List<String>,
    onValueChange: (String) -> Unit,
    options: List<String>,
    hint: String,
    textBackgroundColor: Color,
    textColor: Color,
    modifier: Modifier = Modifier,
    label: String? = null
) {
    var expanded by remember { mutableStateOf(false) }

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
                .background(Color(0xFFF6F6F6))
                .padding(start = 22.dp)
                .padding(vertical = 16.dp)
                .clickable {
                    expanded = true
                }
        ) {
            // TextField с возможностью выбора
            FlowRow(
                modifier = Modifier
                    .fillMaxWidth(),
                verticalArrangement = Arrangement.spacedBy(4.dp),
                horizontalArrangement = Arrangement.spacedBy(4.dp)
            ) {
                values.forEach { item ->
                    Text(
                        text = item,
                        modifier = Modifier
                            .background(textBackgroundColor, RoundedCornerShape(6.dp))
                            .padding(horizontal = 10.dp, vertical = 6.dp),
                        fontSize = 14.sp,
                        color = textColor
                    )
                }
            }


            if (values.isEmpty()) {
                Box(contentAlignment = Alignment.CenterStart) {
                    Text(
                        text = hint,
                        style = Theme.fonts.headlineLarge.copy(color = Theme.colors.hint)
                    )
                }
            }

            DropdownMenu(
                expanded = expanded && options.isNotEmpty(),
                onDismissRequest = { expanded = false },
                modifier = Modifier
                    .fillMaxWidth()
                    .background(Color.White)
            ) {
                options.forEach { option ->
                    DropdownMenuItem(
                        text = { Text(option, style = Theme.fonts.headlineLarge.copy(color = Theme.colors.title)) },
                        onClick = {
                            onValueChange(option)
                            expanded = false
                        }
                    )
                }
            }
        }
    }
}
