package com.larkes.interestgroups.ui.theme

import androidx.compose.runtime.staticCompositionLocalOf
import androidx.compose.ui.graphics.Color

data class InterestGroupsColors(
    val primary: Color,
    val title: Color,
    val hint: Color,
    val third: Color,
    val secondary: Color,
    val formBorderColor: Color
)

val palette = InterestGroupsColors(
    primary = Color(0xffffffff),
    title = Color.Black,
    hint = Color(0xff9F9F9F),
    third = Color(0xffF6F1F1),
    secondary = Color(0xff2AABEE),
    formBorderColor = Color(0xffD8D8D8)
)

val LocalColorProvider = staticCompositionLocalOf<InterestGroupsColors> {
    error("")
}