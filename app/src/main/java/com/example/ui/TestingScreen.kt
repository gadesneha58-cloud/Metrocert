package com.example.ui

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import com.example.MetroCertViewModel
import com.example.ui.theme.*

import androidx.compose.foundation.clickable
import androidx.compose.foundation.interaction.MutableInteractionSource
import androidx.compose.animation.AnimatedVisibility
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.KeyboardArrowUp
import androidx.compose.material.icons.filled.KeyboardArrowDown
import androidx.compose.material.icons.filled.AutoAwesome
import androidx.compose.material.icons.filled.Bolt
import androidx.compose.ui.Alignment

@Composable
fun TestCard(title: String, description: String, content: @Composable () -> Unit) {
    var expanded by remember { mutableStateOf(false) }
    
    Box(
        modifier = Modifier
            .fillMaxWidth()
            .padding(bottom = 16.dp)
            .neoShadow(cornerRadius = 24.dp)
            .background(NeoSurface, RoundedCornerShape(24.dp))
            .clickable(
                interactionSource = remember { MutableInteractionSource() },
                indication = null
            ) { expanded = !expanded }
            .padding(24.dp)
    ) {
        Column {
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically
            ) {
                Column(modifier = Modifier.weight(1f)) {
                    Text(title, style = MaterialTheme.typography.titleMedium, fontWeight = FontWeight.Bold, color = NeoAccent)
                    Text(description, style = MaterialTheme.typography.bodySmall, color = TextMuted, modifier = Modifier.padding(top = 4.dp))
                }
                Icon(
                    imageVector = if (expanded) Icons.Default.KeyboardArrowUp else Icons.Default.KeyboardArrowDown,
                    contentDescription = "Expand",
                    tint = NeoAccent
                )
            }
            AnimatedVisibility(visible = expanded) {
                Column(modifier = Modifier.padding(top = 16.dp)) {
                    content()
                }
            }
        }
    }
}

@Composable
fun TestingScreen(viewModel: MetroCertViewModel, onNext: () -> Unit) {
    val report by viewModel.currentReport.collectAsStateWithLifecycle()
    val currentIndex by viewModel.currentIndex.collectAsStateWithLifecycle()
    val maxCap = report.maxCapacity
    val e = report.e
    val minCap = report.minCapacity
    
    val t1Loads = listOf(minCap, maxCap * 0.25, maxCap * 0.5, maxCap * 0.75, maxCap)
    val t3Load = maxCap / 3
    val t4BaseLoad = minCap
    val t4ExtraLoad = 1.4 * e
    val t5Load = maxCap * 0.8
    val t6Load = maxCap * 0.5
    val t7Load = maxCap * 0.5
    val t8Load = maxCap
    val t9Loads = listOf(minCap, maxCap * 0.5, maxCap * 0.9)
    val t10Load = maxCap * 0.5
    val t11Load = maxCap * 0.5
    val t13Load = maxCap * 0.5
    val t14Load = maxCap * 0.5

    val state = viewModel.getTestingState(currentIndex)
    var showFailDialog by remember { mutableStateOf(false) }
    var failedTestsList by remember { mutableStateOf(listOf<String>()) }
    
    LaunchedEffect(currentIndex) {
        viewModel.loadDraftFromFirestore(currentIndex)
        while (true) {
            kotlinx.coroutines.delay(5000)
            viewModel.triggerAutoSave(currentIndex)
        }
    }



    Column(modifier = Modifier.fillMaxSize().background(MaterialTheme.colorScheme.background).padding(24.dp).verticalScroll(rememberScrollState())) {


        Text("OIML R-76 Test Procedures", style = MaterialTheme.typography.titleLarge, fontWeight = FontWeight.Bold, color = TextDark)
        Spacer(modifier = Modifier.height(16.dp))
        
        TestCard("1. Weighing Performance", "Increasing and decreasing loads.") {
            t1Loads.forEachIndexed { i, load ->
                Row(horizontalArrangement = Arrangement.spacedBy(8.dp), modifier = Modifier.fillMaxWidth().padding(bottom = 8.dp)) {
                    Text("Load: $load", modifier = Modifier.weight(1f))
                    NeoTextField(value = state.t1Up[i] ?: "", onValueChange = { state.t1Up[i] = it }, label = "Up", modifier = Modifier.weight(1f))
                    NeoTextField(value = state.t1Down[i] ?: "", onValueChange = { state.t1Down[i] = it }, label = "Down", modifier = Modifier.weight(1f))
                }
            }
        }
        
        TestCard("2. Temperature Effect on No-Load", "Drift in zero reading due to temperature.") {
            Row(horizontalArrangement = Arrangement.spacedBy(8.dp), modifier = Modifier.fillMaxWidth()) {
                NeoTextField(value = state.t2Z1.value, onValueChange = { state.t2Z1.value = it }, label = "Zero 1", modifier = Modifier.weight(1f))
                NeoTextField(value = state.t2T1.value, onValueChange = { state.t2T1.value = it }, label = "Temp 1", modifier = Modifier.weight(1f))
            }
            Spacer(modifier = Modifier.height(8.dp))
            Row(horizontalArrangement = Arrangement.spacedBy(8.dp), modifier = Modifier.fillMaxWidth()) {
                NeoTextField(value = state.t2Z2.value, onValueChange = { state.t2Z2.value = it }, label = "Zero 2", modifier = Modifier.weight(1f))
                NeoTextField(value = state.t2T2.value, onValueChange = { state.t2T2.value = it }, label = "Temp 2", modifier = Modifier.weight(1f))
            }
        }

        TestCard("3. Eccentricity", "Readings at 5 positions at Load = $t3Load") {
            listOf("Center", "Front Left", "Back Left", "Back Right", "Front Right").forEach { pos ->
                NeoTextField(value = state.t3Readings[pos] ?: "", onValueChange = { state.t3Readings[pos] = it }, label = pos, modifier = Modifier.fillMaxWidth().padding(bottom = 8.dp))
            }
        }
        
        TestCard("4. Discrimination & Sensitivity", "Add $t4ExtraLoad to base load $t4BaseLoad") {
            NeoTextField(value = state.t4BaseRead.value, onValueChange = { state.t4BaseRead.value = it }, label = "Base Reading", modifier = Modifier.fillMaxWidth().padding(bottom = 8.dp))
            NeoTextField(value = state.t4NewRead.value, onValueChange = { state.t4NewRead.value = it }, label = "New Reading", modifier = Modifier.fillMaxWidth())
        }

        TestCard("5. Repeatability", "10 repetitions at Load = $t5Load") {
            for (i in 0 until 5) {
                Row(horizontalArrangement = Arrangement.spacedBy(8.dp), modifier = Modifier.fillMaxWidth().padding(bottom = 8.dp)) {
                    NeoTextField(value = state.t5Readings[i*2] ?: "", onValueChange = { state.t5Readings[i*2] = it }, label = "R${i*2+1}", modifier = Modifier.weight(1f))
                    NeoTextField(value = state.t5Readings[i*2+1] ?: "", onValueChange = { state.t5Readings[i*2+1] = it }, label = "R${i*2+2}", modifier = Modifier.weight(1f))
                }
            }
        }

        TestCard("6. Time-Dependence", "Creep & zero return under sustained load ($t6Load)") {
            Row(horizontalArrangement = Arrangement.spacedBy(8.dp), modifier = Modifier.fillMaxWidth().padding(bottom = 8.dp)) {
                NeoTextField(value = state.t6ZB.value, onValueChange = { state.t6ZB.value = it }, label = "Zero Before", modifier = Modifier.weight(1f))
                NeoTextField(value = state.t6ZA.value, onValueChange = { state.t6ZA.value = it }, label = "Zero After 30m", modifier = Modifier.weight(1f))
            }
            Row(horizontalArrangement = Arrangement.spacedBy(8.dp), modifier = Modifier.fillMaxWidth().padding(bottom = 8.dp)) {
                NeoTextField(value = state.t6C0.value, onValueChange = { state.t6C0.value = it }, label = "Creep 0m", modifier = Modifier.weight(1f))
                NeoTextField(value = state.t6C5.value, onValueChange = { state.t6C5.value = it }, label = "Creep 5m", modifier = Modifier.weight(1f))
            }
            Row(horizontalArrangement = Arrangement.spacedBy(8.dp), modifier = Modifier.fillMaxWidth()) {
                NeoTextField(value = state.t6C15.value, onValueChange = { state.t6C15.value = it }, label = "Creep 15m", modifier = Modifier.weight(1f))
                NeoTextField(value = state.t6C30.value, onValueChange = { state.t6C30.value = it }, label = "Creep 30m", modifier = Modifier.weight(1f))
            }
        }

        TestCard("7. Stability of Equilibrium", "5 readings within seconds at $t7Load") {
            Row(horizontalArrangement = Arrangement.spacedBy(8.dp), modifier = Modifier.fillMaxWidth()) {
                for(i in 0 until 5) NeoTextField(value = state.t7Readings[i] ?: "", onValueChange = { state.t7Readings[i] = it }, label = "R${i+1}", modifier = Modifier.weight(1f))
            }
        }

        TestCard("8. Tilting (Simulated)", "Compare ref vs tilted at max load ($t8Load)") {
            NeoTextField(value = state.t8Ref.value, onValueChange = { state.t8Ref.value = it }, label = "Reference Reading", modifier = Modifier.fillMaxWidth().padding(bottom = 8.dp))
            NeoTextField(value = state.t8Tilt.value, onValueChange = { state.t8Tilt.value = it }, label = "Simulated tilt reading (no physical tilt fixture used)", modifier = Modifier.fillMaxWidth())
        }
        
        TestCard("9. Tare (Weighing Test)", "Net errors with tare.") {
            NeoTextField(value = state.t9Tare.value, onValueChange = { state.t9Tare.value = it }, label = "Tare Weight", modifier = Modifier.fillMaxWidth().padding(bottom = 8.dp))
            t9Loads.forEachIndexed { i, load ->
                NeoTextField(value = state.t9Gross[i] ?: "", onValueChange = { state.t9Gross[i] = it }, label = "Gross @ Net Load $load", modifier = Modifier.fillMaxWidth().padding(bottom = 8.dp))
            }
        }

        TestCard("10. Warm-up Time", "Loaded error at intervals.") {
            Row(horizontalArrangement = Arrangement.spacedBy(8.dp), modifier = Modifier.fillMaxWidth().padding(bottom = 8.dp)) {
                NeoTextField(value = state.t10E0.value, onValueChange = { state.t10E0.value = it }, label = "Err 0m", modifier = Modifier.weight(1f))
                NeoTextField(value = state.t10E5.value, onValueChange = { state.t10E5.value = it }, label = "Err 5m", modifier = Modifier.weight(1f))
            }
            Row(horizontalArrangement = Arrangement.spacedBy(8.dp), modifier = Modifier.fillMaxWidth()) {
                NeoTextField(value = state.t10E15.value, onValueChange = { state.t10E15.value = it }, label = "Err 15m", modifier = Modifier.weight(1f))
                NeoTextField(value = state.t10E30.value, onValueChange = { state.t10E30.value = it }, label = "Err 30m", modifier = Modifier.weight(1f))
            }
        }

        TestCard("11. Voltage Variations", "Readings at Min, Nom, Max voltages.") {
            Row(horizontalArrangement = Arrangement.spacedBy(8.dp), modifier = Modifier.fillMaxWidth()) {
                NeoTextField(value = state.t11Min.value, onValueChange = { state.t11Min.value = it }, label = "Min", modifier = Modifier.weight(1f))
                NeoTextField(value = state.t11Nom.value, onValueChange = { state.t11Nom.value = it }, label = "Nom", modifier = Modifier.weight(1f))
                NeoTextField(value = state.t11Max.value, onValueChange = { state.t11Max.value = it }, label = "Max", modifier = Modifier.weight(1f))
            }
        }

        TestCard("12. Electrical Disturbances", "EMC Fault Checklist (A certified EMC lab is better suited)") {
            Text("A certified EMC lab is better suited than the software for this analysis.", color = FailText, style = MaterialTheme.typography.bodySmall, modifier = Modifier.padding(bottom = 8.dp))
            val items = listOf(
                "Dips" to state.t12Dips, "Bursts" to state.t12Bursts, "Surges" to state.t12Surges,
                "ESD" to state.t12Esd, "Radiated EM" to state.t12Rad, "Conducted RF" to state.t12Cond, "Vehicle Transients" to state.t12Veh
            )
            items.forEach { (label, flag) ->
                Row(verticalAlignment = androidx.compose.ui.Alignment.CenterVertically) {
                    Checkbox(checked = flag.value, onCheckedChange = { flag.value = it })
                    Text("$label (Fault occurred?)")
                }
            }
        }

        TestCard("13. Damp Heat, Steady State", "High Temp & Humidity.") {
            Row(horizontalArrangement = Arrangement.spacedBy(8.dp), modifier = Modifier.fillMaxWidth()) {
                NeoTextField(value = state.t13Init.value, onValueChange = { state.t13Init.value = it }, label = "Init", modifier = Modifier.weight(1f))
                NeoTextField(value = state.t13High.value, onValueChange = { state.t13High.value = it }, label = "High", modifier = Modifier.weight(1f))
                NeoTextField(value = state.t13Final.value, onValueChange = { state.t13Final.value = it }, label = "Final", modifier = Modifier.weight(1f))
            }
        }

        TestCard("14. Span Stability", "Session errors over time.") {
            Row(horizontalArrangement = Arrangement.spacedBy(8.dp), modifier = Modifier.fillMaxWidth()) {
                for(i in 0 until 5) NeoTextField(value = state.t14Errors[i] ?: "", onValueChange = { state.t14Errors[i] = it }, label = "E${i+1}", modifier = Modifier.weight(1f))
            }
        }

        TestCard("15. Endurance (Pre-recorded Batch Entry)", "Endurance results (from pre-recorded test cycles).") {
            NeoTextField(value = state.t15Cycles.value, onValueChange = { state.t15Cycles.value = it }, label = "Cycle Count", modifier = Modifier.fillMaxWidth().padding(bottom = 8.dp))
            Row(horizontalArrangement = Arrangement.spacedBy(8.dp), modifier = Modifier.fillMaxWidth().padding(bottom = 8.dp)) {
                NeoTextField(value = state.t15Init.value, onValueChange = { state.t15Init.value = it }, label = "Initial Reading", modifier = Modifier.weight(1f))
                NeoTextField(value = state.t15Final.value, onValueChange = { state.t15Final.value = it }, label = "Final Reading", modifier = Modifier.weight(1f))
            }
            NeoTextField(value = state.t15Dates.value, onValueChange = { state.t15Dates.value = it }, label = "Date Range", modifier = Modifier.fillMaxWidth())
        }

        TestCard("16. Signatures & Attachments", "Provide digital signature and attach supporting documents.") {
            NeoTextField(value = state.signature.value, onValueChange = { state.signature.value = it }, label = "Digital Signature (Type Name)", modifier = Modifier.fillMaxWidth().padding(bottom = 16.dp))
            Row(verticalAlignment = Alignment.CenterVertically) {
                Checkbox(checked = state.photoAttached.value, onCheckedChange = { state.photoAttached.value = it })
                Text("Attach device photographs (Simulated)", color = TextDark)
            }
        }

        if (showFailDialog) {
            AlertDialog(
                onDismissRequest = { showFailDialog = false },
                title = { Text("Impermissible Errors Detected", color = FailText, fontWeight = FontWeight.Bold) },
                text = { 
                    Column {
                        Text("These values are not in permissible limits according to OIML R76. Change them or send this report back to your manufacturer to improve on this.", color = TextDark)
                        Spacer(modifier = Modifier.height(16.dp))
                        failedTestsList.forEach { 
                            Text("• $it", color = FailText, fontWeight = FontWeight.SemiBold)
                        }
                    }
                },
                confirmButton = {
                    TextButton(onClick = { 
                        showFailDialog = false
                        onNext()
                    }) {
                        Text("Send to Manufacturer", color = FailText)
                    }
                },
                dismissButton = {
                    TextButton(onClick = { showFailDialog = false }) {
                        Text("Edit Values", color = TextDark)
                    }
                },
                containerColor = NeoSurface
            )
        }

        Button(
            onClick = {
                val inputs = state.toTestInputs(
                    t1Loads, t3Load, t4BaseLoad, t4ExtraLoad, t5Load, t6Load, t7Load, t8Load, t9Loads, t10Load, t11Load, t13Load, t14Load
                )
                viewModel.processTests(inputs)
                val currentReportObj = viewModel.activeReports.value[viewModel.currentIndex.value]
                if (currentReportObj.status == "Fail") {
                    val failed = mutableListOf<String>()
                    if (currentReportObj.weighingResults.any { !it.isPass }) failed.add("1. Weighing Performance")
                    if (currentReportObj.tempEffectResult?.isPass == false) failed.add("2. Temperature Effect")
                    if (currentReportObj.eccentricityResult?.isPass == false) failed.add("3. Eccentricity")
                    if (currentReportObj.discriminationResult?.isPass == false) failed.add("4. Discrimination")
                    if (currentReportObj.repeatabilityResult?.isPass == false) failed.add("5. Repeatability")
                    if (currentReportObj.timeDependenceResult?.isPass == false) failed.add("6. Time-Dependence (Creep)")
                    if (currentReportObj.stabilityResult?.isPass == false) failed.add("7. Stability of Equilibrium")
                    if (currentReportObj.tiltingResult?.isPass == false) failed.add("8. Tilting Effect")
                    if (currentReportObj.tareResult?.isPass == false) failed.add("9. Tare Operation")
                    if (currentReportObj.warmUpResult?.isPass == false) failed.add("10. Warm-up Time")
                    if (currentReportObj.voltageResult?.isPass == false) failed.add("11. Voltage Variations")
                    if (currentReportObj.emcResult?.isPass == false) failed.add("12. EMC/RF Immunity")
                    if (currentReportObj.dampHeatResult?.isPass == false) failed.add("13. Damp Heat (Steady State)")
                    if (currentReportObj.spanStabilityResult?.isPass == false) failed.add("14. Span Stability")
                    if (currentReportObj.enduranceResult?.isPass == false) failed.add("15. Endurance")
                    
                    failedTestsList = failed
                    showFailDialog = true
                } else {
                    onNext()
                }
            },
            modifier = Modifier.fillMaxWidth().height(56.dp).neoShadow(cornerRadius = 28.dp, isPressed = false),
            shape = RoundedCornerShape(28.dp),
            colors = ButtonDefaults.buttonColors(containerColor = NeoSurface)
        ) {
            Text("GENERATE REPORT", style = MaterialTheme.typography.titleMedium, color = NeoAccent, fontWeight = FontWeight.Bold)
        }
        Spacer(modifier = Modifier.height(32.dp))
    }
}
