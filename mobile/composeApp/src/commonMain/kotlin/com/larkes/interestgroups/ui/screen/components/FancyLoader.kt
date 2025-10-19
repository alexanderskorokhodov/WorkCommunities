package com.larkes.interestgroups.ui.screen.components

import androidx.compose.animation.core.*
import androidx.compose.foundation.Canvas
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.alpha
import androidx.compose.ui.draw.scale
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.geometry.Rect
import androidx.compose.ui.geometry.Size
import androidx.compose.ui.graphics.*
import androidx.compose.ui.graphics.drawscope.Stroke
import androidx.compose.ui.graphics.drawscope.rotate
import androidx.compose.ui.unit.Dp
import androidx.compose.ui.unit.dp

/**
 * Кроссплатформенный анимированный лоадер (Compose Multiplatform).
 *
 * Просто передай размер через Modifier: Modifier.size(80.dp)
 */
@Composable
fun FancyLoader(
    modifier: Modifier = Modifier,
    ringColor: Color = Color(0xFF2AABEE),
    trackColor: Color = Color(0xFFE7F6FB),
    stroke: Dp = 6.dp
) {
    val infiniteTransition = rememberInfiniteTransition()

    // 🔹 Плавное вращение
    val rotation by infiniteTransition.animateFloat(
        initialValue = 0f,
        targetValue = 360f,
        animationSpec = infiniteRepeatable(
            animation = tween(1200, easing = LinearEasing)
        )
    )

    // 🔹 Изменение длины дуги (эффект "растущей дуги")
    val sweep by infiniteTransition.animateFloat(
        initialValue = 30f,
        targetValue = 280f,
        animationSpec = infiniteRepeatable(
            animation = tween(900, easing = FastOutSlowInEasing),
            repeatMode = RepeatMode.Reverse
        )
    )

    // 🔹 Пульсирующий центр
    val pulse by infiniteTransition.animateFloat(
        initialValue = 0.92f,
        targetValue = 1.08f,
        animationSpec = infiniteRepeatable(
            animation = tween(1000, easing = FastOutSlowInEasing),
            repeatMode = RepeatMode.Reverse
        )
    )

    Box(
        modifier = modifier,
        contentAlignment = Alignment.Center
    ) {
        Canvas(modifier = Modifier.fillMaxSize()) {
            val strokePx = stroke.toPx()
            val diameter = size.minDimension
            val rect = Rect(
                Offset(strokePx / 2, strokePx / 2),
                Size(diameter - strokePx, diameter - strokePx)
            )

            // Фоновое кольцо
            drawArc(
                color = trackColor,
                startAngle = 0f,
                sweepAngle = 360f,
                useCenter = false,
                topLeft = rect.topLeft,
                size = rect.size,
                style = Stroke(strokePx, cap = StrokeCap.Round)
            )

            // Основная анимированная дуга
            val gradient = Brush.sweepGradient(
                0.0f to ringColor,
                0.7f to ringColor.copy(alpha = 0.8f),
                1f to ringColor.copy(alpha = 0.4f)
            )

            rotate(rotation) {
                drawArc(
                    brush = gradient,
                    startAngle = -90f,
                    sweepAngle = sweep,
                    useCenter = false,
                    topLeft = rect.topLeft,
                    size = rect.size,
                    style = Stroke(strokePx, cap = StrokeCap.Round)
                )
            }
        }

        // Центральная пульсирующая точка
        Box(
            modifier = Modifier
                .size(20.dp)
                .scale(pulse)
                .alpha(0.95f)
                .background(Color.White, CircleShape)
        )
    }
}