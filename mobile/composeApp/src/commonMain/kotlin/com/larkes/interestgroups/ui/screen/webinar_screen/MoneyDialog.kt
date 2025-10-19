package com.larkes.interestgroups.ui.screen.webinar_screen

import androidx.compose.animation.AnimatedVisibility
import androidx.compose.animation.ExperimentalAnimationApi
import androidx.compose.animation.core.Animatable
import androidx.compose.animation.core.EaseOutBounce
import androidx.compose.animation.core.Easing
import androidx.compose.animation.core.FastOutSlowInEasing
import androidx.compose.animation.core.LinearEasing
import androidx.compose.animation.core.tween
import androidx.compose.animation.fadeIn
import androidx.compose.animation.fadeOut
import androidx.compose.animation.scaleIn
import androidx.compose.animation.scaleOut
import androidx.compose.foundation.Image
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.offset
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.Button
import androidx.compose.material3.ButtonDefaults
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.remember
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.draw.rotate
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.compose.ui.window.Dialog
import com.larkes.interestgroups.ui.theme.getInterTightFont
import interestgroups.composeapp.generated.resources.Res
import interestgroups.composeapp.generated.resources.coin
import interestgroups.composeapp.generated.resources.subbonus
import kotlinx.coroutines.launch
import org.jetbrains.compose.resources.DrawableResource
import org.jetbrains.compose.resources.painterResource

@OptIn(ExperimentalAnimationApi::class)
@Composable
fun BonusDialog(
    onDismiss: () -> Unit,
    title: String,
    subtitle: String,
    buttonText: String = "Отлично"
) {
    Dialog(onDismissRequest = { onDismiss() }) {
        AnimatedVisibility(
            visible = true,
            enter = fadeIn(animationSpec = tween(300)) + scaleIn(initialScale = 0.8f, animationSpec = tween(300)),
            exit = fadeOut(animationSpec = tween(200)) + scaleOut(targetScale = 0.8f, animationSpec = tween(200))
        ) {
            // 🔹 Вертикальное движение монетки
            val coinOffset = remember { Animatable(0f) }
            // 🔹 Вращение монетки
            val rotation = remember { Animatable(0f) }

            LaunchedEffect(Unit) {
                // Подскок
                launch {
                    coinOffset.animateTo(
                        targetValue = -40f,
                        animationSpec = tween(400, easing = FastOutSlowInEasing)
                    )
                    coinOffset.animateTo(
                        targetValue = 0f,
                        animationSpec = tween(600, easing = EaseOutBounce)
                    )
                }
                // Вращение
                launch {
                    rotation.animateTo(
                        targetValue = 360f,
                        animationSpec = tween(800, easing = LinearEasing)
                    )
                }
            }

            Box(
                modifier = Modifier
                    .clip(RoundedCornerShape(20.dp))
                    .background(Color.White)
                    .padding(24.dp)
                    .padding(top = 34.dp)
                    .fillMaxWidth(0.95f)
            ) {
                Column(
                    horizontalAlignment = Alignment.CenterHorizontally,
                    verticalArrangement = Arrangement.spacedBy(16.dp)
                ) {
                    // 🔹 Подложка бонуса и монетка
                    Box(contentAlignment = Alignment.Center) {
                        Image(
                            painter = painterResource(Res.drawable.subbonus),
                            contentDescription = null,
                            modifier = Modifier
                                .height(71.dp)
                                .width(141.dp),
                            contentScale = ContentScale.Crop
                        )
                        Image(
                            painter = painterResource(Res.drawable.coin),
                            contentDescription = null,
                            modifier = Modifier
                                .width(53.dp)
                                .height(35.dp)
                                .offset(y = coinOffset.value.dp)
                                .rotate(rotation.value),
                            contentScale = ContentScale.Crop
                        )
                    }

                    Text(
                        text = title,
                        fontFamily = getInterTightFont(),
                        fontWeight = FontWeight.SemiBold,
                        fontSize = 20.sp,
                        color = Color.Black,
                        textAlign = TextAlign.Center
                    )

                    Text(
                        text = subtitle,
                        fontFamily = getInterTightFont(),
                        fontWeight = FontWeight.Normal,
                        fontSize = 14.sp,
                        color = Color(0xFF9E9E9E),
                        textAlign = TextAlign.Center
                    )

                    Spacer(modifier = Modifier.height(8.dp))

                    Button(
                        onClick = { onDismiss() },
                        colors = ButtonDefaults.buttonColors(containerColor = Color(0xFF2AABEE)),
                        shape = RoundedCornerShape(12.dp),
                        modifier = Modifier
                            .fillMaxWidth()
                            .height(46.dp)
                    ) {
                        Text(
                            text = buttonText,
                            fontFamily = getInterTightFont(),
                            fontWeight = FontWeight.Medium,
                            fontSize = 16.sp,
                            color = Color.White
                        )
                    }
                }
            }
        }
    }
}
