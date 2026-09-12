package com.example.ui

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import com.example.MetroCertViewModel
import com.example.ui.theme.*
import java.text.SimpleDateFormat
import java.util.Date
import java.util.Locale

@Composable
fun PreviewScreen(
    viewModel: MetroCertViewModel,
    onBack: () -> Unit,
    onExportPdf: () -> Unit,
    onExportConsolidatedPdf: () -> Unit
) {
    val report by viewModel.currentReport.collectAsStateWithLifecycle()
    val activeReports by viewModel.activeReports.collectAsStateWithLifecycle()
    val dateStr = SimpleDateFormat("yyyy-MM-dd", Locale.getDefault()).format(Date(report.date))
    val isPass = report.status == "Pass"
    val statusColor = if (isPass) PassText else FailText

    Column(
        modifier = Modifier
            .fillMaxSize()
            .background(androidx.compose.ui.graphics.Color.White)
            .padding(24.dp)
            .verticalScroll(rememberScrollState())
    ) {
        Text("Report Preview", style = MaterialTheme.typography.headlineMedium, fontWeight = FontWeight.Bold, color = TextDark)
        Spacer(modifier = Modifier.height(24.dp))

        Box(
            modifier = Modifier
                .fillMaxWidth()
                .neoShadow(cornerRadius = 24.dp)
                .background(NeoSurface, RoundedCornerShape(24.dp))
                .padding(24.dp)
        ) {
            Column {
                Text("Certificate No: ${report.certificateNo}", style = MaterialTheme.typography.titleMedium, fontWeight = FontWeight.Bold, color = TextDark)
                Text("Date: $dateStr", style = MaterialTheme.typography.bodyMedium, color = TextMuted)
                Spacer(modifier = Modifier.height(16.dp))

                Text("Instrument: ${report.manufacturer} ${report.modelNumber}", style = MaterialTheme.typography.bodyLarge, color = TextDark)
                Text("Serial: ${report.serialNumber}", style = MaterialTheme.typography.bodyMedium, color = TextMuted)
                Text("Class: ${report.accuracyClass} | Max: ${report.maxCapacity} | e: ${report.e}", style = MaterialTheme.typography.bodyMedium, color = TextMuted)
                
                Spacer(modifier = Modifier.height(24.dp))
                Text("Test Results Summary", style = MaterialTheme.typography.titleMedium, fontWeight = FontWeight.Bold, color = NeoAccent)
                Spacer(modifier = Modifier.height(8.dp))
                
                val results = listOf(
                    "1. Weighing Performance" to (report.weighingResults.isNotEmpty() && report.weighingResults.all { it.isPass }),
                    "2. Temp Effect" to (report.tempEffectResult?.isPass == true),
                    "3. Eccentricity" to (report.eccentricityResult?.isPass == true),
                    "4. Discrimination" to (report.discriminationResult?.isPass == true),
                    "5. Repeatability" to (report.repeatabilityResult?.isPass == true),
                    "6. Time-Dependence" to (report.timeDependenceResult?.isPass == true),
                    "7. Stability" to (report.stabilityResult?.isPass == true),
                    "8. Tilting" to (report.tiltingResult?.isPass == true),
                    "9. Tare" to (report.tareResult?.isPass == true),
                    "10. Warm-up" to (report.warmUpResult?.isPass == true),
                    "11. Voltage" to (report.voltageResult?.isPass == true),
                    "12. EMC" to (report.emcResult?.isPass == true),
                    "13. Damp Heat" to (report.dampHeatResult?.isPass == true),
                    "14. Span Stability" to (report.spanStabilityResult?.isPass == true),
                    "15. Endurance" to (report.enduranceResult?.isPass == true)
                )

                results.forEach { (name, pass) ->
                    Row(modifier = Modifier.fillMaxWidth().padding(vertical = 4.dp), horizontalArrangement = Arrangement.SpaceBetween) {
                        Text(name, style = MaterialTheme.typography.bodyMedium, color = TextDark)
                        Text(if (pass) "PASS" else "FAIL", style = MaterialTheme.typography.bodyMedium, color = if (pass) PassText else FailText, fontWeight = FontWeight.Bold)
                    }
                }

                Spacer(modifier = Modifier.height(24.dp))
                HorizontalDivider(color = NeoBackground)
                Spacer(modifier = Modifier.height(16.dp))
                
                if (report.digitalSignature.isNotEmpty()) {
                    Text("Digital Signature: ${report.digitalSignature}", style = MaterialTheme.typography.bodyMedium, color = TextDark)
                }
                if (report.photoAttached) {
                    Text("Attachments: Photographs and supporting documents appended.", style = MaterialTheme.typography.bodyMedium, color = TextDark)
                }
                
                Spacer(modifier = Modifier.height(16.dp))
                Column(
                    modifier = Modifier.fillMaxWidth().padding(vertical = 16.dp),
                    horizontalAlignment = androidx.compose.ui.Alignment.CenterHorizontally
                ) {
                    Text("OVERALL VERDICT", style = MaterialTheme.typography.titleSmall, color = TextMuted)
                    Spacer(modifier = Modifier.height(8.dp))
                    val verdictText = if (report.status == "Fail") "TEST FAILED" else "TEST PASSED"
                    Text(verdictText, style = MaterialTheme.typography.headlineMedium, fontWeight = FontWeight.Bold, color = statusColor)
                    if (report.status == "Fail") {
                        Spacer(modifier = Modifier.height(4.dp))
                        Text("Impermissible Errors Detected", style = MaterialTheme.typography.bodyMedium, color = FailText)
                    }
                }
            }
        }
        
        Spacer(modifier = Modifier.height(32.dp))
        
        Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.spacedBy(16.dp)) {
            Button(
                onClick = onBack,
                modifier = Modifier.weight(1f).height(56.dp).neoShadow(cornerRadius = 28.dp, isPressed = false),
                shape = RoundedCornerShape(28.dp),
                colors = ButtonDefaults.buttonColors(containerColor = NeoSurface)
            ) {
                Text("BACK", color = TextDark, fontWeight = FontWeight.Bold)
            }
            Button(
                onClick = onExportPdf,
                modifier = Modifier.weight(1f).height(56.dp).neoShadow(cornerRadius = 28.dp, isPressed = false),
                shape = RoundedCornerShape(28.dp),
                colors = ButtonDefaults.buttonColors(containerColor = NeoSurface)
            ) {
                Text("EXPORT PDF", color = NeoAccent, fontWeight = FontWeight.Bold)
            }
        }
        if (activeReports.size > 1) {
            Spacer(modifier = Modifier.height(16.dp))
            Button(
                onClick = onExportConsolidatedPdf,
                modifier = Modifier.fillMaxWidth().height(56.dp).neoShadow(cornerRadius = 28.dp, isPressed = false),
                shape = RoundedCornerShape(28.dp),
                colors = ButtonDefaults.buttonColors(containerColor = NeoAccent)
            ) {
                Text("EXPORT ALL (${activeReports.size} MACHINES)", color = androidx.compose.ui.graphics.Color.White, fontWeight = FontWeight.Bold)
            }
        }
        Spacer(modifier = Modifier.height(32.dp))
    }
}
