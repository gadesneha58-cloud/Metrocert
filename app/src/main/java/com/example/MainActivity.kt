package com.example

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.setValue
import com.example.ui.LoginScreen
import com.example.ui.MetroCertApp
import com.example.ui.theme.MetroCertTheme

class MainActivity : ComponentActivity() {
    private var isSignedIn by mutableStateOf(false)

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        
        enableEdgeToEdge()
        setContent {
            MetroCertTheme {
                if (isSignedIn) {
                    MetroCertApp(
                        onSignOut = {
                            isSignedIn = false
                        }
                    )
                } else {
                    LoginScreen(onSignInClick = { 
                        // Bypass actual login logic for local preview mode
                        isSignedIn = true 
                    })
                }
            }
        }
    }
}

