import re

with open("app/src/main/java/com/example/ui/TestingScreen.kt", "r") as f:
    content = f.read()

# Add dialog state variables
state_vars = """    val state = remember { TestingState() }"""

new_state_vars = """    val state = remember { TestingState() }
    var showFailDialog by remember { mutableStateOf(false) }
    var failedTestsList by remember { mutableStateOf(listOf<String>()) }"""

content = content.replace(state_vars, new_state_vars)

# Replace the "GENERATE REPORT" button logic
old_button = """        Button(
            onClick = {
                val inputs = state.toTestInputs(
                    t1Loads, t3Load, t4BaseLoad, t4ExtraLoad, t5Load, t6Load, t7Load, t8Load, t9Loads, t10Load, t11Load, t13Load, t14Load
                )
                viewModel.processTests(inputs)
                onNext()
            },"""

new_button = """        if (showFailDialog) {
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
            },"""

content = content.replace(old_button, new_button)

with open("app/src/main/java/com/example/ui/TestingScreen.kt", "w") as f:
    f.write(content)

