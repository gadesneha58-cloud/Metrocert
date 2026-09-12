package com.example.ui

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.*
import androidx.compose.runtime.Composable

import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Description
import androidx.compose.material.icons.filled.Info
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.getValue
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment

import androidx.compose.ui.Modifier
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import com.example.data.RulesConfig
import com.example.ui.theme.*

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun ConfigScreen() {
    var showDocSheet by remember { mutableStateOf(false) }

    Column(modifier = Modifier.fillMaxSize().padding(24.dp).verticalScroll(rememberScrollState())) {
        Text("Rules & Configuration", style = MaterialTheme.typography.headlineMedium, fontWeight = FontWeight.Bold, color = TextDark)
        Spacer(modifier = Modifier.height(8.dp))
        Text("OIML R-76 MPE Thresholds & Constraints", style = MaterialTheme.typography.bodyMedium, color = TextMuted)
        Spacer(modifier = Modifier.height(24.dp))

        // Technical Documentation Button
        Button(
            onClick = { showDocSheet = true },
            modifier = Modifier.fillMaxWidth().padding(bottom = 24.dp),
            shape = RoundedCornerShape(16.dp),
            colors = ButtonDefaults.buttonColors(containerColor = NeoAccent),
            contentPadding = PaddingValues(vertical = 16.dp)
        ) {
            Icon(Icons.Default.Description, contentDescription = "Doc", modifier = Modifier.size(20.dp))
            Spacer(modifier = Modifier.width(8.dp))
            Text("View Technical Documentation", fontWeight = FontWeight.Bold, color = androidx.compose.ui.graphics.Color.White)
        }
        
        if (showDocSheet) {
            ModalBottomSheet(
                onDismissRequest = { showDocSheet = false },
                containerColor = NeoSurface,
                dragHandle = { BottomSheetDefaults.DragHandle(color = NeoAccent) }
            ) {
                Column(
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(horizontal = 24.dp, vertical = 16.dp)
                        .verticalScroll(rememberScrollState())
                ) {
                    Text("Technical Documentation", style = MaterialTheme.typography.headlineMedium, fontWeight = FontWeight.Bold, color = TextDark)
                    Spacer(modifier = Modifier.height(24.dp))
                    
                    DocSection(
                        title = "1. Software Architecture",
                        content = "• Pattern: MVVM (Model-View-ViewModel)\n• UI Framework: Jetpack Compose (Declarative UI)\n• Language: Kotlin\n• State Management: StateFlow & State hoisting\n• Local Persistence: Room Database (SQLite) for offline-first test history repository."
                    )
                    
                    DocSection(
                        title = "2. Calculation Methodology",
                        content = "• Standard: OIML R 76\n• Logic: MPE (Maximum Permissible Error) is calculated dynamically based on the instrument's Accuracy Class (I, II, III, IIII).\n• The applied load (m) is converted to verification scale intervals (e).\n• MPE constraints (±0.5e, ±1.0e, ±1.5e) are enforced through automated threshold checks.\n• Repeatability, eccentricity, and weighing errors are aggregated mathematically in real-time."
                    )
                    
                    DocSection(
                        title = "3. Deployment Framework",
                        content = "• Target: Native Android OS (Tablets and Smartphones)\n• Output Formats: APK/AAB distribution.\n• Reporting: On-device PDF generation utilizing native Android canvas APIs (no external cloud APIs required), providing standardized test reports."
                    )
                    
                    Spacer(modifier = Modifier.height(48.dp))
                }
            }
        }


        RulesConfig.rules.forEach { (className, classRules) ->
            Text("Class $className", style = MaterialTheme.typography.titleMedium, fontWeight = FontWeight.SemiBold, color = NeoAccent)
            Spacer(modifier = Modifier.height(8.dp))
            Text("Verification Scale Intervals (n): ${formatDouble(classRules.nRange.min)} to ${if (classRules.nRange.max == Double.MAX_VALUE) "∞" else formatDouble(classRules.nRange.max)}", style = MaterialTheme.typography.bodySmall, color = TextMuted)
            Spacer(modifier = Modifier.height(16.dp))

            Box(
                modifier = Modifier
                    .fillMaxWidth()
                    .neoShadow(cornerRadius = 16.dp)
                    .background(NeoSurface, RoundedCornerShape(16.dp))
                    .padding(16.dp)
            ) {
                Column(modifier = Modifier.fillMaxWidth()) {
                    Row(modifier = Modifier.fillMaxWidth().padding(bottom = 8.dp)) {
                        Text("Load (m) in 'e'", modifier = Modifier.weight(1.2f), fontWeight = FontWeight.Bold, color = TextMuted, style = MaterialTheme.typography.labelMedium)
                        Text("MPE", modifier = Modifier.weight(0.8f), fontWeight = FontWeight.Bold, color = TextMuted, style = MaterialTheme.typography.labelMedium)
                    }
                    HorizontalDivider(color = NeoBackground)

                    val tiers = classRules.mpeTiers
                    tiers.forEachIndexed { index, tier ->
                        val lowerBound = if (index == 0) 0.0 else tiers[index - 1].uptoE
                        val upperBoundStr = if (tier.uptoE == Double.MAX_VALUE) "∞" else formatDouble(tier.uptoE) + "e"
                        val lowerBoundStr = formatDouble(lowerBound) + "e"
                        
                        val rangeStr = if (index == 0) {
                            "0 ≤ m ≤ $upperBoundStr"
                        } else {
                            "$lowerBoundStr < m ≤ $upperBoundStr"
                        }

                        Row(modifier = Modifier.fillMaxWidth().padding(vertical = 12.dp)) {
                            Text(rangeStr, modifier = Modifier.weight(1.2f), color = TextDark, style = MaterialTheme.typography.bodyMedium)
                            Text("±${tier.mpeMultiplier}e", modifier = Modifier.weight(0.8f), color = TextDark, style = MaterialTheme.typography.bodyMedium)
                        }
                        if (index < tiers.size - 1) {
                            HorizontalDivider(color = NeoBackground)
                        }
                    }
                }
            }
            Spacer(modifier = Modifier.height(32.dp))
        }

        Text("Note: These rules are based on OIML R-76 standard recommendations and are enforced across all test procedures.", color = TextMuted, style = MaterialTheme.typography.bodySmall)
        Spacer(modifier = Modifier.height(24.dp))
    }
}

private fun formatDouble(value: Double): String {
    return if (value == value.toLong().toDouble()) {
        value.toLong().toString()
    } else {
        value.toString()
    }
}

@Composable
fun DocSection(title: String, content: String) {
    Column(modifier = Modifier.fillMaxWidth().padding(bottom = 24.dp)) {
        Row(verticalAlignment = Alignment.CenterVertically) {
            Icon(Icons.Default.Info, contentDescription = null, tint = NeoAccent, modifier = Modifier.size(18.dp))
            Spacer(modifier = Modifier.width(8.dp))
            Text(title, style = MaterialTheme.typography.titleMedium, fontWeight = FontWeight.Bold, color = TextDark)
        }
        Spacer(modifier = Modifier.height(8.dp))
        Box(
            modifier = Modifier
                .fillMaxWidth()
                .background(NeoBackground, RoundedCornerShape(12.dp))
                .padding(16.dp)
        ) {
            Text(content, style = MaterialTheme.typography.bodyMedium, color = TextMuted, lineHeight = androidx.compose.ui.unit.TextUnit(22f, androidx.compose.ui.unit.TextUnitType.Sp))
        }
    }
}
