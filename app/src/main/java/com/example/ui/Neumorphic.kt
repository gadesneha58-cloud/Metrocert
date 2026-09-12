package com.example.ui

import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.drawBehind
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.Paint
import androidx.compose.ui.graphics.drawscope.drawIntoCanvas
import androidx.compose.ui.graphics.toArgb
import androidx.compose.ui.unit.Dp
import androidx.compose.ui.unit.dp

fun Modifier.neoShadow(
    cornerRadius: Dp = 16.dp,
    lightShadowColor: Color = Color(0xFFFFFFFF),
    darkShadowColor: Color = Color(0xFFA3B1C6),
    elevation: Dp = 6.dp,
    isPressed: Boolean = false
) = this.drawBehind {
    drawIntoCanvas { canvas ->
        val paint = Paint()
        val frameworkPaint = paint.asFrameworkPaint()
        val radius = cornerRadius.toPx()
        
        frameworkPaint.color = Color.Transparent.toArgb()
        
        if (isPressed) {
            // Subtle inset feel
            frameworkPaint.setShadowLayer(
                (elevation / 3).toPx(),
                (elevation / 4).toPx(),
                (elevation / 4).toPx(),
                darkShadowColor.toArgb()
            )
            canvas.drawRoundRect(0f, 0f, size.width, size.height, radius, radius, paint)
            
            frameworkPaint.setShadowLayer(
                (elevation / 3).toPx(),
                -(elevation / 4).toPx(),
                -(elevation / 4).toPx(),
                lightShadowColor.toArgb()
            )
            canvas.drawRoundRect(0f, 0f, size.width, size.height, radius, radius, paint)
        } else {
            // Outer shadow (bottom right)
            frameworkPaint.setShadowLayer(
                elevation.toPx(),
                elevation.toPx() / 2,
                elevation.toPx() / 2,
                darkShadowColor.toArgb()
            )
            canvas.drawRoundRect(0f, 0f, size.width, size.height, radius, radius, paint)

            // Outer highlight (top left)
            frameworkPaint.setShadowLayer(
                elevation.toPx(),
                -(elevation.toPx() / 2),
                -(elevation.toPx() / 2),
                lightShadowColor.toArgb()
            )
            canvas.drawRoundRect(0f, 0f, size.width, size.height, radius, radius, paint)
        }
    }
}
