package com.larkes.interestgroups.presentation.login

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.larkes.interestgroups.data.dto.CodeRequest
import com.larkes.interestgroups.data.dto.CompanyRegRequest
import com.larkes.interestgroups.data.dto.NumberRequest
import com.larkes.interestgroups.data.dto.StatusDTO
import com.larkes.interestgroups.domain.models.UpdateUserProfileRequest
import com.larkes.interestgroups.domain.repository.AuthRepository
import com.larkes.interestgroups.presentation.login.models.AboutMeUIState
import com.larkes.interestgroups.presentation.login.models.CompanyUIState
import com.larkes.interestgroups.presentation.login.models.CreateProfileUIState
import com.larkes.interestgroups.presentation.login.models.EnterCodeUIState
import com.larkes.interestgroups.presentation.login.models.LoginUIAction
import com.larkes.interestgroups.presentation.login.models.LoginUIEvent
import com.larkes.interestgroups.presentation.login.models.RoleType
import com.larkes.interestgroups.presentation.login.models.SkillModel
import com.larkes.interestgroups.utils.Resource
import com.russhwolf.settings.Settings
import kotlinx.coroutines.delay
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.launchIn
import kotlinx.coroutines.flow.onEach
import kotlinx.coroutines.launch

class LoginViewModel(
    private val authRepository: AuthRepository
): ViewModel() {

    private val _uiAction: MutableStateFlow<LoginUIAction> = MutableStateFlow(LoginUIAction.OpenChoseRole)
    val uiAction: StateFlow<LoginUIAction> = _uiAction
    private val _aboutMeUIState = MutableStateFlow(AboutMeUIState())
    val aboutMeUIState: StateFlow<AboutMeUIState> = _aboutMeUIState
    private val _createProfileUIState = MutableStateFlow(CreateProfileUIState())
    val createProfileUIState: StateFlow<CreateProfileUIState> = _createProfileUIState
    private val _enterCodeUIState: MutableStateFlow<EnterCodeUIState> = MutableStateFlow(EnterCodeUIState())
    val enterCodeUIState: StateFlow<EnterCodeUIState> = _enterCodeUIState

    private var _skillsServer: List<SkillModel> = listOf()
    private var _statusesServer: List<StatusDTO> = listOf()

    private val _companyUIState: MutableStateFlow<CompanyUIState> = MutableStateFlow(CompanyUIState())
    val companyUIState: StateFlow<CompanyUIState> = _companyUIState

    init {
        val res = authRepository.checkUserAuth()

        if(res.first){
            if(res.second == RoleType.Specialist){
                _uiAction.value = LoginUIAction.OpenMain
            }else{
                _uiAction.value = LoginUIAction.OpenCompanyProfile
            }
        }
    }


    private var _role: RoleType? = null

    fun onEvent(loginUIEvent: LoginUIEvent){
        when(loginUIEvent){
            LoginUIEvent.SpecialistButtonClicked -> {
                _role = RoleType.Specialist
                _uiAction.value = LoginUIAction.OpenCreateProfile
            }
            LoginUIEvent.CompanyClicked -> {
                _role = RoleType.Company
                _uiAction.value = LoginUIAction.OpenCreateProfile
            }
            is LoginUIEvent.AboutMeEntered -> {
                _aboutMeUIState.value = aboutMeUIState.value.copy(
                    aboutMe = loginUIEvent.text
                )
                checkAboutMeDoneAvailable()
            }
            is LoginUIEvent.NameEntered -> {
                _aboutMeUIState.value = aboutMeUIState.value.copy(
                    name = loginUIEvent.name
                )
                checkAboutMeDoneAvailable()
            }
            is LoginUIEvent.ProfileEntered -> {
                _aboutMeUIState.value = aboutMeUIState.value.copy(
                    portfolio = loginUIEvent.text
                )
                checkAboutMeDoneAvailable()
            }
            is LoginUIEvent.SkillClicked -> {
                val skills = aboutMeUIState.value.skills.toMutableList()
                skills.add(loginUIEvent.skill)
                _aboutMeUIState.value = aboutMeUIState.value.copy(
                    skills = skills
                )
                checkAboutMeDoneAvailable()
            }
            is LoginUIEvent.StatusClicked -> {
                val status = aboutMeUIState.value.status.toMutableList()
                status.add(loginUIEvent.status)
                _aboutMeUIState.value = aboutMeUIState.value.copy(
                    status = status
                )
                checkAboutMeDoneAvailable()
            }

            LoginUIEvent.AboutMeDoneClicked -> {

                authRepository.createProfile(UpdateUserProfileRequest(
                    full_name = aboutMeUIState.value.name,
                    portfolio_url = aboutMeUIState.value.portfolio,
                    description = aboutMeUIState.value.aboutMe,
                    skill_uids = aboutMeUIState.value.skills.map { item ->
                        val id = _skillsServer.find { it.title ==  item}
                        id?.id ?: ""
                    },
                    status_uids = aboutMeUIState.value.status.map { item ->
                        val id = _statusesServer.find { it.title ==  item}
                        id?.id ?: ""
                    }
                )).onEach {
                    when(it){
                        is Resource.Success -> {
                            Settings().putString("role", _role?.name.toString())
                            _uiAction.value = LoginUIAction.OpenMain
                        }
                        is Resource.Error -> {

                        }
                    }
                }.launchIn(viewModelScope)
            }
            LoginUIEvent.AboutMeSkipClicked -> {
                Settings().putString("role", _role?.name.toString())
                authRepository.createProfile(UpdateUserProfileRequest(
                    full_name = aboutMeUIState.value.name,
                    portfolio_url = aboutMeUIState.value.portfolio,
                    description = aboutMeUIState.value.aboutMe,
                    skill_uids = aboutMeUIState.value.skills.map { item ->

                        val id = _skillsServer.find { it.title ==  item}
                        id?.id ?: ""
                    },
                    status_uids = aboutMeUIState.value.status.map { item ->
                        val id = _statusesServer.find { it.title ==  item}
                        id?.id ?: ""
                    }
                )).onEach {
                    when(it){
                        is Resource.Success -> {
                            _uiAction.value = LoginUIAction.OpenMain
                        }
                        is Resource.Error -> {

                        }
                    }
                }.launchIn(viewModelScope)
            }

            LoginUIEvent.ContinueNumberClicked -> {
                viewModelScope.launch {
                    authRepository.sendNumber(NumberRequest(phone = "+7${createProfileUIState.value.number}"), isCompany = _role == RoleType.Company).onEach {
                        when(it){
                            is Resource.Success -> {
                                _uiAction.value = LoginUIAction.OpenCode
                                _enterCodeUIState.value = _enterCodeUIState.value.copy(number = "+7${createProfileUIState.value.number}")
                                setupCodeRepeatTime()
                            }
                            is Resource.Error -> {

                            }
                        }
                    }.launchIn(viewModelScope)
                }
            }
            is LoginUIEvent.EnterCodeClicked -> {

            }
            is LoginUIEvent.NumberEntered -> {
                _createProfileUIState.value = createProfileUIState.value.copy(number = loginUIEvent.number)
            }
            is LoginUIEvent.EnterCodeBackClicked -> {
                _uiAction.value = LoginUIAction.OpenCreateProfile
                _enterCodeUIState.value = EnterCodeUIState()
            }

            is LoginUIEvent.CompanyDescriptionEntered -> {
                _companyUIState.value = companyUIState.value.copy(
                    description = loginUIEvent.description
                )
            }
            LoginUIEvent.CompanyDoneClicked -> {
                Settings().putString("role", _role?.name.toString())
                _uiAction.value = LoginUIAction.OpenCompanyProfile
            }
            LoginUIEvent.CompanySkipClicked -> {
                Settings().putString("role", _role?.name.toString())
                _uiAction.value = LoginUIAction.OpenCompanyProfile
            }
            is LoginUIEvent.CompanyNameEntered -> {
                _companyUIState.value = companyUIState.value.copy(
                    companyName = loginUIEvent.name
                )
                checkCompanyAvailable()
            }
            is LoginUIEvent.CompanySpecialAdded -> {
                val specs = companyUIState.value.specialities.toMutableList()
                specs.add(loginUIEvent.item)
                _companyUIState.value = companyUIState.value.copy(
                    specialities = specs
                )
            }

            is LoginUIEvent.SmsCodeEntered -> {
                _enterCodeUIState.value = enterCodeUIState.value.copy(code = loginUIEvent.code)
                if(enterCodeUIState.value.code.length >= 5){
                    viewModelScope.launch {
                        authRepository.sendCode(CodeRequest(phone = "+7${createProfileUIState.value.number}", code = enterCodeUIState.value.code), isCompany = _role == RoleType.Company).onEach {
                            when(it){
                                is Resource.Success -> {
                                    fetchSkills()
                                    fetchStatuses()
                                    _uiAction.value = if(_role == RoleType.Specialist) LoginUIAction.OpenAboutNe else LoginUIAction.OpenCompany
                                }
                                is Resource.Error -> {
                                    _enterCodeUIState.value = enterCodeUIState.value.copy(code = "")
                                }
                            }
                        }.launchIn(viewModelScope)
                    }
                }
            }
        }
    }

    private fun fetchStatuses() {
        authRepository.fetchStatuses().onEach {
            when(it){
                is Resource.Success -> {
                    it.data?.let { res ->
                        _statusesServer = res
                        _aboutMeUIState.value = aboutMeUIState.value.copy(
                            statuesOptions = res
                        )
                    }
                }
                is Resource.Error -> {
                    _enterCodeUIState.value = enterCodeUIState.value.copy(code = "")
                }
            }
        }.launchIn(viewModelScope)
    }

    private fun fetchSkills() {
        authRepository.fetchSkills().onEach {
            when(it){
                is Resource.Success -> {
                    it.data?.let { res ->
                        _skillsServer = res.map { skill ->
                            SkillModel(
                                title = skill.title,
                                backColor = skill.sphere.background_color,
                                color = skill.sphere.text_color,
                                id = skill.id
                            )
                        }
                        _aboutMeUIState.value = aboutMeUIState.value.copy(
                            skillsOptions = res.map { skill ->
                                SkillModel(
                                    title = skill.title,
                                    backColor = skill.sphere.background_color,
                                    color = skill.sphere.text_color,
                                    id = skill.id
                                )
                            }
                        )
                    }
                }
                is Resource.Error -> {
                    _enterCodeUIState.value = enterCodeUIState.value.copy(code = "")
                }
            }
        }.launchIn(viewModelScope)
    }



    private fun setupCodeRepeatTime(){
        viewModelScope.launch {
            repeat(40){
                delay(1000)
                _enterCodeUIState.value = _enterCodeUIState.value.copy(repeatTime = enterCodeUIState.value.repeatTime - 1)
            }
        }
    }

    private fun checkCompanyAvailable(){
        _companyUIState.value = companyUIState.value.copy(
            isAvailable = companyUIState.value.companyName.isNotEmpty()
        )
    }
    private fun checkAboutMeDoneAvailable(){
        val about = _aboutMeUIState.value
        _aboutMeUIState.value = _aboutMeUIState
            .value
            .copy(isClickAvailable =
                about.name.isNotEmpty()
                        && about.skills.isNotEmpty()
                        && about.status.isNotEmpty()
                        && about.aboutMe.isNotEmpty()
                        && about.portfolio.isNotEmpty()
        )
    }

}