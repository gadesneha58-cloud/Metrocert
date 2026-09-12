import re

with open("app/src/main/java/com/example/ui/SetupScreen.kt", "r") as f:
    content = f.read()

# Add isInService state
if "var isInService" not in content:
    content = content.replace("var accuracyClass by remember { mutableStateOf(report.accuracyClass) }", 
                              "var accuracyClass by remember { mutableStateOf(report.accuracyClass) }\n    var isInService by remember { mutableStateOf(report.isInService) }")
    content = content.replace("if (report.accuracyClass.isNotEmpty()) accuracyClass = report.accuracyClass", 
                              "if (report.accuracyClass.isNotEmpty()) accuracyClass = report.accuracyClass\n        isInService = report.isInService")

# Add UI for isInService right below Accuracy Class
class_info_ui = """        Text(classInfo, style = MaterialTheme.typography.bodySmall, color = NeoAccent, modifier = Modifier.padding(start = 8.dp, top = 4.dp))
        
        Spacer(modifier = Modifier.height(16.dp))"""

inservice_ui = """        Text(classInfo, style = MaterialTheme.typography.bodySmall, color = NeoAccent, modifier = Modifier.padding(start = 8.dp, top = 4.dp))
        
        Spacer(modifier = Modifier.height(16.dp))
        
        Row(
            modifier = Modifier.fillMaxWidth().padding(horizontal = 8.dp),
            verticalAlignment = androidx.compose.ui.Alignment.CenterVertically,
            horizontalArrangement = Arrangement.SpaceBetween
        ) {
            Column {
                Text("In-Service Inspection", style = MaterialTheme.typography.titleSmall, color = TextDark)
                Text("Doubles Maximum Permissible Errors (MPE)", style = MaterialTheme.typography.bodySmall, color = TextMuted)
            }
            Switch(
                checked = isInService,
                onCheckedChange = { isInService = it },
                colors = SwitchDefaults.colors(checkedThumbColor = NeoAccent, checkedTrackColor = NeoAccent.copy(alpha = 0.5f))
            )
        }
        
        Spacer(modifier = Modifier.height(16.dp))"""

content = content.replace(class_info_ui, inservice_ui)

# Add isInService to updateInstrumentDetails
content = content.replace("""                        maxCapacity = maxVal,
                        e = eVal
                    )""", """                        maxCapacity = maxVal,
                        e = eVal,
                        isInService = isInService
                    )""")

with open("app/src/main/java/com/example/ui/SetupScreen.kt", "w") as f:
    f.write(content)
