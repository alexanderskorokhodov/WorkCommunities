package com.larkes.interestgroups

import androidx.compose.ui.window.ComposeUIViewController
import com.larkes.interestgroups.di.PlatformConfiguration
import com.larkes.interestgroups.di.PlatformSDK
import com.larkes.interestgroups.ui.App

fun MainViewController() = ComposeUIViewController {
    PlatformSDK.init(PlatformConfiguration())
    App() 
}