package com.larkes.interestgroups.ui.theme

import androidx.compose.runtime.staticCompositionLocalOf

object StringResource {
    const val CHOOSE_ROLE_TITLE = "Выбери \n свою роль"

}

val LocalStringProvider = staticCompositionLocalOf<StringResource> {
    error("")
}