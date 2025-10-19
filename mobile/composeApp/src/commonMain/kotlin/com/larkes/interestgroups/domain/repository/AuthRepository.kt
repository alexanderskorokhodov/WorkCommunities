package com.larkes.interestgroups.domain.repository

import com.larkes.interestgroups.data.dto.CodeRequest
import com.larkes.interestgroups.data.dto.CompanyRegRequest
import com.larkes.interestgroups.data.dto.GroupDto
import com.larkes.interestgroups.data.dto.GroupListResponse
import com.larkes.interestgroups.data.dto.NumberRequest
import com.larkes.interestgroups.data.dto.StatusListResponse
import com.larkes.interestgroups.data.dto.UserProfileDto
import com.larkes.interestgroups.domain.models.UpdateUserProfileRequest
import com.larkes.interestgroups.presentation.login.models.RoleType
import com.larkes.interestgroups.utils.Resource
import kotlinx.coroutines.flow.Flow

interface AuthRepository {

    fun sendNumber(number: NumberRequest, isCompany: Boolean): Flow<Resource<Unit>>
     fun sendCode(code: CodeRequest, isCompany: Boolean): Flow<Resource<Unit>>
    fun companySignIn(request: CompanyRegRequest): Flow<Resource<Unit>>
     fun createProfile(updateUserProfileRequest: UpdateUserProfileRequest): Flow<Resource<Unit>>
    fun checkUserAuth(): Pair<Boolean, RoleType>
    fun fetchSkills(): Flow<Resource<GroupListResponse>>
    fun fetchStatuses(): Flow<Resource<StatusListResponse>>
    fun cleanSession()
    fun fetchViewProfile(id: String): Flow<Resource<UserProfileDto>>
}