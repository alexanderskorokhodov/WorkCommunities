package com.larkes.interestgroups.presentation.login.models

sealed class LoginUIEvent {
    data object SpecialistButtonClicked: LoginUIEvent()
    data object CompanyClicked: LoginUIEvent()
    data class NameEntered(val name: String): LoginUIEvent()
    data class SkillClicked(val skill: String): LoginUIEvent()
    data class StatusClicked(val status: String): LoginUIEvent()
    data class AboutMeEntered(val text: String): LoginUIEvent()
    data class ProfileEntered(val text: String): LoginUIEvent()
    data object ContinueNumberClicked: LoginUIEvent()
    data class EnterCodeClicked(val code: String): LoginUIEvent()
    data object AboutMeDoneClicked: LoginUIEvent()
    data object AboutMeSkipClicked: LoginUIEvent()
    data class NumberEntered(val number: String): LoginUIEvent()
    data object EnterCodeBackClicked: LoginUIEvent()
    data class CompanyNameEntered(val name: String): LoginUIEvent()
    data class CompanyDescriptionEntered(val description: String): LoginUIEvent()
    data class CompanySpecialAdded(val item: String): LoginUIEvent()
    data object CompanyDoneClicked: LoginUIEvent()
    data object CompanySkipClicked: LoginUIEvent()
    data class SmsCodeEntered(val code: String): LoginUIEvent()
}