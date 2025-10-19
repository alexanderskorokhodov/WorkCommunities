package com.larkes.interestgroups.domain.repository

import com.larkes.interestgroups.data.dto.EventListResponse
import com.larkes.interestgroups.utils.Resource
import kotlinx.coroutines.flow.Flow

interface EventRepository {

    fun fetchEvents(): Flow<Resource<EventListResponse>>

}