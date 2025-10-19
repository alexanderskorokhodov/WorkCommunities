package com.larkes.interestgroups.ui.theme

import androidx.compose.material3.Text
import androidx.compose.material3.Typography
import androidx.compose.runtime.Composable
import androidx.compose.runtime.staticCompositionLocalOf
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.TextStyle
import androidx.compose.ui.text.font.Font
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.sp
import interestgroups.composeapp.generated.resources.Res
import interestgroups.composeapp.generated.resources.intertightmedium
import interestgroups.composeapp.generated.resources.intertightregular
import org.jetbrains.compose.resources.Font

@Composable
fun getInterTightFont() = FontFamily(
    Font(
        Res.font.intertightmedium,
        FontWeight.Medium
    ),
    Font(
        Res.font.intertightregular,
        FontWeight.Normal
    )
)

@Composable
fun getTypography() = Typography(
    titleLarge = TextStyle(
        fontFamily = getInterTightFont(),
        fontSize = 52.sp,
        color = Color.Black,
        fontWeight = FontWeight.Medium
    ),
    titleMedium = TextStyle(
        fontFamily = getInterTightFont(),
        fontSize = 24.sp,
        color = Color.Black,
        fontWeight = FontWeight.Normal
    ),
    headlineLarge = TextStyle(
        fontFamily = getInterTightFont(),
        fontSize = 18.sp,
        color = Color(0xff9F9F9F),
        fontWeight = FontWeight.Normal
    ),
    headlineMedium = TextStyle(
        fontFamily = getInterTightFont(),
        fontSize = 14.sp,
        color = Color(0xff9F9F9F),
        fontWeight = FontWeight.Normal
    ),
    headlineSmall = TextStyle(
        fontFamily = getInterTightFont(),
        fontSize = 10.sp,
        color = Color(0xff9F9F9F),
        fontWeight = FontWeight.Normal
    ),
    bodyMedium =  TextStyle(
        fontFamily = getInterTightFont(),
        fontSize = 18.sp,
        color = Color.Black,
        fontWeight = FontWeight.Normal
    )
)

val LocalFontProvider = staticCompositionLocalOf<Typography> {
    error("")
}
