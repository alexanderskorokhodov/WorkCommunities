package com.larkes.interestgroups.ui.navigation

import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.size
import androidx.compose.material3.Icon
import androidx.compose.material3.NavigationBar
import androidx.compose.material3.NavigationBarItem
import androidx.compose.material3.NavigationBarItemColors
import androidx.compose.material3.NavigationBarItemDefaults
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.ui.Modifier
import androidx.compose.ui.geometry.Rect
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.navigation.NavController
import androidx.navigation.compose.currentBackStackEntryAsState
import com.larkes.interestgroups.ui.theme.Theme
import com.larkes.interestgroups.ui.theme.getInterTightFont
import interestgroups.composeapp.generated.resources.Res
import interestgroups.composeapp.generated.resources.union
import org.jetbrains.compose.resources.DrawableResource
import org.jetbrains.compose.resources.painterResource
import kotlin.collections.forEach

class BottomNavItem(
    val icon: DrawableResource,
    val name:String,
    val route: Screens
)

@Composable
fun BottomNavBar(
    items:List<BottomNavItem>,
    navController: NavController,
    onClick: (BottomNavItem) -> Unit
) {


    val backStackEntry = navController.currentBackStackEntryAsState()

    val showBottomNavState = remember {
        mutableStateOf(true)
    }

    if(backStackEntry.value?.destination?.route != null){
        val backStackEntryValue = backStackEntry.value?.destination?.route!!.split("/")[0]

        showBottomNavState.value = ((backStackEntryValue.contains(Screens.MainScreen::class.simpleName.toString()))
                || (backStackEntryValue.contains(Screens.CompanyProfileScreen::class.simpleName.toString()))
                || (backStackEntryValue.contains(Screens.CompanyCommunitiesScreen::class.simpleName.toString()))
                )
        println("ssdvsdv ${backStackEntryValue} ${Screens.LoginScreen::class.simpleName}")
    }


    if(showBottomNavState.value){
        Box(Modifier.height(75.dp)) {

            NavigationBar(
                containerColor = Color.White
            ) {
                items.forEach { item ->
                    if(backStackEntry.value?.destination?.route != null) {
                        val backStack =
                            backStackEntry.value?.destination?.route!!.split("/")[0]

                        NavigationBarItem(
                            colors = NavigationBarItemDefaults.colors(
                                selectedIconColor = Theme.colors.primary,
                                unselectedIconColor = Color.Black,
                                selectedTextColor = Color.Black,
                                unselectedTextColor = Color.Black,
                                indicatorColor = Color.Transparent
                            ),
                            selected = true,
                            onClick = { onClick(item) },
                            icon = {
                                Icon(
                                    painter = painterResource(item.icon),
                                    contentDescription = null,
                                    modifier = Modifier.size(18.dp),
                                    tint = Color.Black
                                )
                            },
                            label = {
                                Text(
                                    text = item.name,
                                    fontFamily = getInterTightFont(),
                                    fontSize = 12.sp,
                                    color = Color.Black,
                                    fontWeight = FontWeight.Normal
                                )
                            }
                        )
                    }
                }
            }
        }
    }




}