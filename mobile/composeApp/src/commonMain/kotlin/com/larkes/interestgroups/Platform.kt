package com.larkes.interestgroups

interface Platform {
    val name: String
}

expect fun getPlatform(): Platform