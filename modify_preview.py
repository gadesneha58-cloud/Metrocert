import re

with open("app/src/main/java/com/example/ui/PreviewScreen.kt", "r") as f:
    content = f.read()

old_verdict = """                Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween) {
                    Text("OVERALL VERDICT", style = MaterialTheme.typography.titleLarge, fontWeight = FontWeight.Bold, color = TextDark)
                    val verdictText = if (report.status == "Fail") "TEST FAILED: Impermissible Errors Detected" else "TEST PASSED"
                    Text(verdictText, style = MaterialTheme.typography.titleMedium, fontWeight = FontWeight.Bold, color = statusColor)
                }"""

new_verdict = """                Column(
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
                }"""

content = content.replace(old_verdict, new_verdict)

with open("app/src/main/java/com/example/ui/PreviewScreen.kt", "w") as f:
    f.write(content)
