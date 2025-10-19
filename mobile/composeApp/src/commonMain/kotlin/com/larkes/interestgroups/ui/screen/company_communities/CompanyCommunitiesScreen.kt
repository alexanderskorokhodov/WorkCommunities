package com.larkes.interestgroups.ui.screen.company_communities

import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.itemsIndexed
import androidx.compose.material3.Divider
import androidx.compose.material3.DividerDefaults
import androidx.compose.material3.HorizontalDivider
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.navigation.NavController
import com.larkes.interestgroups.presentation.company_communities.CompanyCommunitiesViewModel
import com.larkes.interestgroups.ui.navigation.Screens
import com.larkes.interestgroups.ui.screen.components.CompanyCommunityComponent
import com.larkes.interestgroups.ui.theme.getInterTightFont

@Composable
fun CompanyCommunitiesScreen(
    viewModel: CompanyCommunitiesViewModel,
    navController: NavController
){

    val communities by viewModel._communities.collectAsState()
    val isLoading by viewModel._isLoading.collectAsState()


    Column {
        Spacer(modifier = Modifier.height(32.dp))
        Text(
            text = "${communities.size} Сообществ",
            color = Color(0xff2AABEE),
            fontSize = 16.sp,
            fontFamily = getInterTightFont(),
            fontWeight = FontWeight.Normal,
            modifier = Modifier.padding(start = 20.dp)
        )
        Spacer(modifier = Modifier.height(20.dp))
        LazyColumn(
            modifier = Modifier.padding(horizontal = 20.dp)
        ) {
            itemsIndexed(communities) {index, item ->
                CompanyCommunityComponent(
                    title = item.name,
                    subtitle = item.description,
                    participents = item.members_count ?: 4,
                    keys = 1,
                    solves = 11
                ){
                    navController.navigate(Screens.CompanyCommunitiesDetailsScreen(item.id))
                }
                Spacer(modifier = Modifier.height(20.dp))
                HorizontalDivider(Modifier.fillMaxWidth().height(1.dp), DividerDefaults.Thickness, Color(0xffD8D8D8))
                Spacer(modifier = Modifier.height(20.dp))
            }
            item {
                Spacer(modifier = Modifier.height(120.dp))
            }
        }
    }

}