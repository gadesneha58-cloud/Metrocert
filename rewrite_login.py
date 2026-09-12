import os

code = """package com.example.ui

import androidx.compose.foundation.Canvas
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.outlined.Lock
import androidx.compose.material.icons.outlined.Person
import androidx.compose.material.icons.outlined.Visibility
import androidx.compose.material.icons.outlined.Speed
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.geometry.CornerRadius
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.geometry.Size
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.drawscope.Stroke
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.example.ui.theme.NeoAccent

@Composable
fun LoginScreen(onSignInClick: () -> Unit) {
    var username by remember { mutableStateOf("") }
    var password by remember { mutableStateOf("") }
    var rememberMe by remember { mutableStateOf(true) }

    val bgColor = Color(0xFFF0E5FF)
    val surfaceColor = Color(0xFFF5EEFF)
    val primaryPurple = Color(0xFF6C3CD1)
    val textPurple = Color(0xFF5A31B2)
    val lightShadow = Color.White
    val darkShadow = Color(0xFFD4C8EB)

    val bgGradient = Brush.verticalGradient(
        colors = listOf(Color(0xFFF6EEFF), Color(0xFFE8DBFA))
    )

    Box(
        modifier = Modifier
            .fillMaxSize()
            .background(bgGradient),
        contentAlignment = Alignment.Center
    ) {
        // Decorative background elements
        Canvas(modifier = Modifier.fillMaxSize()) {
            // Top left circles
            drawCircle(
                color = Color(0xFFF0E5FF).copy(alpha = 0.5f),
                radius = 200f,
                center = Offset(0f, 100f)
            )
            // Bottom right circles
            drawCircle(
                color = Color(0xFFE5D5F9).copy(alpha = 0.5f),
                radius = 300f,
                center = Offset(size.width, size.height)
            )
            // Some dots top right
            for (i in 0..3) {
                for (j in 0..4) {
                    drawCircle(
                        color = Color(0xFFD4C8EB).copy(alpha = 0.4f),
                        radius = 4f,
                        center = Offset(size.width - 150f + i * 30f, 150f + j * 30f)
                    )
                }
            }
            // Some dots bottom left
            for (i in 0..4) {
                for (j in 0..3) {
                    drawCircle(
                        color = Color(0xFFD4C8EB).copy(alpha = 0.4f),
                        radius = 4f,
                        center = Offset(100f + i * 30f, size.height - 200f + j * 30f)
                    )
                }
            }
        }

        Column(
            horizontalAlignment = Alignment.CenterHorizontally,
            modifier = Modifier
                .fillMaxWidth()
                .padding(24.dp)
        ) {
            // Top Logo
            Box(
                modifier = Modifier
                    .size(100.dp)
                    .neoShadow(cornerRadius = 50.dp, lightShadowColor = lightShadow, darkShadowColor = darkShadow, elevation = 8.dp)
                    .background(surfaceColor, CircleShape),
                contentAlignment = Alignment.Center
            ) {
                Icon(
                    imageVector = Icons.Outlined.Speed,
                    contentDescription = "Logo",
                    modifier = Modifier.size(50.dp),
                    tint = primaryPurple
                )
            }
            
            Spacer(modifier = Modifier.height(40.dp))

            // Main Card
            Box(
                modifier = Modifier
                    .fillMaxWidth()
                    .neoShadow(cornerRadius = 32.dp, lightShadowColor = lightShadow, darkShadowColor = darkShadow, elevation = 12.dp)
                    .background(surfaceColor, RoundedCornerShape(32.dp))
                    .padding(horizontal = 24.dp, vertical = 32.dp)
            ) {
                Column(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalAlignment = Alignment.CenterHorizontally
                ) {
                    // Username
                    TextField(
                        value = username,
                        onValueChange = { username = it },
                        placeholder = { Text("Email or Username", color = Color.Gray, fontSize = 14.sp) },
                        leadingIcon = { Icon(Icons.Outlined.Person, contentDescription = null, tint = textPurple) },
                        modifier = Modifier
                            .fillMaxWidth()
                            .height(56.dp)
                            .neoShadow(cornerRadius = 16.dp, isPressed = true, lightShadowColor = lightShadow, darkShadowColor = darkShadow, elevation = 4.dp),
                        shape = RoundedCornerShape(16.dp),
                        colors = TextFieldDefaults.colors(
                            focusedContainerColor = surfaceColor,
                            unfocusedContainerColor = surfaceColor,
                            focusedIndicatorColor = Color.Transparent,
                            unfocusedIndicatorColor = Color.Transparent,
                            focusedTextColor = Color.DarkGray,
                            unfocusedTextColor = Color.DarkGray
                        ),
                        singleLine = true
                    )

                    Spacer(modifier = Modifier.height(20.dp))

                    // Password
                    TextField(
                        value = password,
                        onValueChange = { password = it },
                        placeholder = { Text("Password", color = Color.Gray, fontSize = 14.sp) },
                        leadingIcon = { Icon(Icons.Outlined.Lock, contentDescription = null, tint = textPurple) },
                        trailingIcon = { Icon(Icons.Outlined.Visibility, contentDescription = null, tint = textPurple) },
                        modifier = Modifier
                            .fillMaxWidth()
                            .height(56.dp)
                            .neoShadow(cornerRadius = 16.dp, isPressed = true, lightShadowColor = lightShadow, darkShadowColor = darkShadow, elevation = 4.dp),
                        shape = RoundedCornerShape(16.dp),
                        colors = TextFieldDefaults.colors(
                            focusedContainerColor = surfaceColor,
                            unfocusedContainerColor = surfaceColor,
                            focusedIndicatorColor = Color.Transparent,
                            unfocusedIndicatorColor = Color.Transparent,
                            focusedTextColor = Color.DarkGray,
                            unfocusedTextColor = Color.DarkGray
                        ),
                        singleLine = true
                    )

                    Spacer(modifier = Modifier.height(20.dp))

                    Row(
                        modifier = Modifier.fillMaxWidth(),
                        verticalAlignment = Alignment.CenterVertically,
                        horizontalArrangement = Arrangement.SpaceBetween
                    ) {
                        Row(verticalAlignment = Alignment.CenterVertically) {
                            Box(
                                modifier = Modifier
                                    .size(24.dp)
                                    .neoShadow(cornerRadius = 6.dp, isPressed = true, lightShadowColor = lightShadow, darkShadowColor = darkShadow, elevation = 3.dp)
                                    .background(if (rememberMe) surfaceColor else surfaceColor, RoundedCornerShape(6.dp))
                                    .clickable { rememberMe = !rememberMe },
                                contentAlignment = Alignment.Center
                            ) {
                                if (rememberMe) {
                                    Icon(
                                        painter = painterResource(android.R.drawable.checkbox_on_background), 
                                        contentDescription = null, 
                                        tint = primaryPurple, 
                                        modifier = Modifier.size(16.dp)
                                    )
                                }
                            }
                            Spacer(modifier = Modifier.width(8.dp))
                            Text("Remember me", fontSize = 12.sp, color = textPurple)
                        }
                        Text("Forgot password?", fontSize = 12.sp, color = textPurple, modifier = Modifier.clickable { })
                    }

                    Spacer(modifier = Modifier.height(32.dp))

                    Button(
                        onClick = onSignInClick,
                        modifier = Modifier
                            .fillMaxWidth()
                            .height(56.dp)
                            .shadow(8.dp, RoundedCornerShape(16.dp), spotColor = primaryPurple),
                        shape = RoundedCornerShape(16.dp),
                        colors = ButtonDefaults.buttonColors(containerColor = primaryPurple)
                    ) {
                        Text("Login", fontSize = 18.sp, fontWeight = FontWeight.Bold, color = Color.White)
                    }

                    Spacer(modifier = Modifier.height(32.dp))

                    Row(
                        verticalAlignment = Alignment.CenterVertically,
                        modifier = Modifier.fillMaxWidth()
                    ) {
                        HorizontalDivider(modifier = Modifier.weight(1f), color = Color.LightGray.copy(alpha = 0.5f))
                        Text("or continue with", fontSize = 12.sp, color = textPurple, modifier = Modifier.padding(horizontal = 16.dp))
                        HorizontalDivider(modifier = Modifier.weight(1f), color = Color.LightGray.copy(alpha = 0.5f))
                    }

                    Spacer(modifier = Modifier.height(24.dp))

                    Row(
                        horizontalArrangement = Arrangement.spacedBy(20.dp),
                        modifier = Modifier.fillMaxWidth(),
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        SocialButtonText(text = "G", color = Color(0xFFEA4335), surfaceColor = surfaceColor, lightShadow = lightShadow, darkShadow = darkShadow)
                        SocialButtonText(text = "a", color = Color(0xFF34A853), surfaceColor = surfaceColor, lightShadow = lightShadow, darkShadow = darkShadow)
                        SocialButtonText(text = "Ap", color = Color.Black, surfaceColor = surfaceColor, lightShadow = lightShadow, darkShadow = darkShadow)
                    }

                    Spacer(modifier = Modifier.height(32.dp))

                    Row {
                        Text("Don't have an account? ", fontSize = 14.sp, color = Color.DarkGray)
                        Text("Sign up", fontSize = 14.sp, color = textPurple, fontWeight = FontWeight.Bold, modifier = Modifier.clickable { })
                    }
                }
            }
        }
    }
}

@Composable
fun RowScope.SocialButtonText(text: String, color: Color, surfaceColor: Color, lightShadow: Color, darkShadow: Color) {
    Box(
        modifier = Modifier
            .weight(1f)
            .height(60.dp)
            .neoShadow(cornerRadius = 16.dp, lightShadowColor = lightShadow, darkShadowColor = darkShadow, elevation = 6.dp)
            .background(surfaceColor, RoundedCornerShape(16.dp))
            .clickable { },
        contentAlignment = Alignment.Center
    ) {
        Text(text = text, color = color, fontWeight = FontWeight.Bold, fontSize = 24.sp)
    }
}
"""

with open("app/src/main/java/com/example/ui/LoginScreen.kt", "w") as f:
    f.write(code)

