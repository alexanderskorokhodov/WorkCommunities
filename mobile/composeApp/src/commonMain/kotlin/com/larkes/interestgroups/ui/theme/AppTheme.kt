package com.larkes.interestgroups.ui.theme

import androidx.compose.material3.Typography
import androidx.compose.runtime.Composable
import androidx.compose.runtime.CompositionLocalProvider

@Composable
fun AppTheme(content:@Composable () -> Unit) {

    CompositionLocalProvider(
        LocalStringProvider provides StringResource,
        LocalColorProvider provides palette,
        LocalFontProvider provides getTypography(),
        content = content
    )

}

object Theme{

    val strings: StringResource
        @Composable
        get() = LocalStringProvider.current

    val colors: InterestGroupsColors
        @Composable
        get() = LocalColorProvider.current

    val fonts: Typography
        @Composable
        get() = LocalFontProvider.current
}