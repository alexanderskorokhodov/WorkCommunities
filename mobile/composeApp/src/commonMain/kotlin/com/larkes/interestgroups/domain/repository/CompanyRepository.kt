package com.larkes.interestgroups.domain.repository

import com.larkes.interestgroups.data.dto.CommunityWithDetailsDto
import com.larkes.interestgroups.data.dto.CompanyCommunityItemDto
import com.larkes.interestgroups.data.dto.CompanyCommunityListResponse
import com.larkes.interestgroups.data.dto.CompanyDto
import com.larkes.interestgroups.data.dto.CompanyInfoDto
import com.larkes.interestgroups.data.dto.CompanyListResponse
import com.larkes.interestgroups.data.dto.CompanyWithCommunitiesDto
import com.larkes.interestgroups.data.dto.ProjectDto
import com.larkes.interestgroups.utils.Resource
import kotlinx.coroutines.flow.Flow

interface CompanyRepository {

    fun fetchCompanies(): Flow<Resource<CompanyListResponse>>
    fun fetchCompanyInfo(id: String): Flow<Resource<CompanyWithCommunitiesDto>>
    fun fetchCompanyInfo(): Flow<Resource<CompanyWithCommunitiesDto>>
    fun fetchCompanyCommunities(): Flow<Resource<CompanyCommunityListResponse>>

}