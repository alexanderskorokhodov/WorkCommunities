package com.larkes.interestgroups.presentation.login.models

sealed class LoginUIAction{
    data object OpenCreateProfile: LoginUIAction()
    data object OpenChoseRole: LoginUIAction()
    data object OpenCode: LoginUIAction()
    data object OpenAboutNe: LoginUIAction()
    data object OpenCompany: LoginUIAction()
    data object OpenMain: LoginUIAction()
    data object OpenCompanyProfile: LoginUIAction()
}