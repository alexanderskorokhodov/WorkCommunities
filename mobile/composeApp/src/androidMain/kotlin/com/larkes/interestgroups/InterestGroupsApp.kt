package com.larkes.interestgroups

import android.app.Application
import com.larkes.interestgroups.di.PlatformConfiguration
import com.larkes.interestgroups.di.PlatformSDK

class InterestGroupsApp: Application() {
    override fun onCreate() {
        super.onCreate()
        PlatformSDK.init(PlatformConfiguration(this))
    }
}