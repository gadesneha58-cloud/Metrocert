with open('app/src/main/java/com/example/ui/TestingScreen.kt', 'r') as f:
    content = f.read()

target = """        TestCard("15. Endurance (Pre-recorded Batch Entry)", "Endurance results (from pre-recorded test cycles).") {
            NeoTextField(value = state.t15Cycles.value, onValueChange = { state.t15Cycles.value = it }, label = "Cycle Count", modifier = Modifier.fillMaxWidth().padding(bottom = 8.dp))
            Row(horizontalArrangement = Arrangement.spacedBy(8.dp), modifier = Modifier.fillMaxWidth().padding(bottom = 8.dp)) {
                NeoTextField(value = state.t15Init.value, onValueChange = { state.t15Init.value = it }, label = "Initial Reading", modifier = Modifier.weight(1f))
                NeoTextField(value = state.t15Final.value, onValueChange = { state.t15Final.value = it }, label = "Final Reading", modifier = Modifier.weight(1f))
            }
            NeoTextField(value = state.t15Dates.value, onValueChange = { state.t15Dates.value = it }, label = "Date Range", modifier = Modifier.fillMaxWidth())
        }"""

new_target = target + """

        TestCard("16. Signatures & Attachments", "Provide digital signature and attach supporting documents.") {
            NeoTextField(value = state.signature.value, onValueChange = { state.signature.value = it }, label = "Digital Signature (Type Name)", modifier = Modifier.fillMaxWidth().padding(bottom = 16.dp))
            Row(verticalAlignment = Alignment.CenterVertically) {
                Checkbox(checked = state.photoAttached.value, onCheckedChange = { state.photoAttached.value = it })
                Text("Attach device photographs (Simulated)", color = TextDark)
            }
        }"""

content = content.replace(target, new_target)

with open('app/src/main/java/com/example/ui/TestingScreen.kt', 'w') as f:
    f.write(content)
