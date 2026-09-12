with open("app/src/main/java/com/example/ui/SetupScreen.kt", "r") as f:
    content = f.read()

old_apply_func = """    fun applyDemoData() {
        manufacturer = "Mettler Toledo"
        model = "ICS689 Precision"
        serial = "MT-2026-XPR984"
        certNo = "CERT-OIML-2026-088"
        accuracyClass = "III"
        maxCapacity = "30.0"
        minCapacity = "0.1"
        e = "0.005"
        temp = "20.0"
        humidity = "50.0"
        pressure = "1013.25"
        standardId = "OIML-E2-STD-2026"
        nValidationError = null
        viewModel.autoPopulateDemoSetup()
    }"""

new_apply_func = """    fun applyDemoData(pass: Boolean) {
        manufacturer = "Mettler Toledo"
        model = "ICS689 Precision"
        serial = "MT-2026-XPR984"
        certNo = "CERT-OIML-2026-088"
        accuracyClass = "III"
        maxCapacity = "30.0"
        minCapacity = "0.1"
        e = "0.005"
        temp = "20.0"
        humidity = "50.0"
        pressure = "1013.25"
        standardId = "OIML-E2-STD-2026"
        nValidationError = null
        viewModel.autoPopulateFullDemo(pass = pass)
    }"""

content = content.replace(old_apply_func, new_apply_func)

old_buttons = """        TextButton(
            onClick = { applyDemoData() },
            modifier = Modifier.fillMaxWidth()
        ) {
            Icon(Icons.Default.AutoAwesome, contentDescription = null, tint = NeoAccent, modifier = Modifier.size(18.dp))
            Spacer(modifier = Modifier.width(8.dp))
            Text("Auto-fill Data", color = NeoAccent, fontWeight = FontWeight.SemiBold)
        }"""

new_buttons = """        Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.spacedBy(8.dp)) {
            Button(
                onClick = { applyDemoData(pass = true) },
                colors = ButtonDefaults.buttonColors(containerColor = NeoAccent),
                shape = RoundedCornerShape(12.dp),
                modifier = Modifier.weight(1f)
            ) {
                Icon(Icons.Default.AutoAwesome, contentDescription = null, tint = androidx.compose.ui.graphics.Color.White, modifier = Modifier.size(16.dp))
                Spacer(modifier = Modifier.width(4.dp))
                Text("Pass", color = androidx.compose.ui.graphics.Color.White, fontWeight = FontWeight.Bold, style = MaterialTheme.typography.labelMedium)
            }
            Button(
                onClick = { applyDemoData(pass = false) },
                colors = ButtonDefaults.buttonColors(containerColor = FailText),
                shape = RoundedCornerShape(12.dp),
                modifier = Modifier.weight(1f)
            ) {
                Text("Fail", color = androidx.compose.ui.graphics.Color.White, fontWeight = FontWeight.Bold, style = MaterialTheme.typography.labelMedium)
            }
        }"""

content = content.replace(old_buttons, new_buttons)

with open("app/src/main/java/com/example/ui/SetupScreen.kt", "w") as f:
    f.write(content)

