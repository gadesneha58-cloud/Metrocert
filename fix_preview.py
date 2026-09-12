with open("app/src/main/java/com/example/ui/PreviewScreen.kt", "r") as f:
    content = f.read()

target = """                Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween) {
                    Text("OVERALL VERDICT", style = MaterialTheme.typography.titleLarge, fontWeight = FontWeight.Bold, color = TextDark)
                    Text(report.status.uppercase(), style = MaterialTheme.typography.titleLarge, fontWeight = FontWeight.Bold, color = statusColor)
                }"""

new_target = """                Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween) {
                    Text("OVERALL VERDICT", style = MaterialTheme.typography.titleLarge, fontWeight = FontWeight.Bold, color = TextDark)
                    val verdictText = if (report.status == "Fail") "TEST FAILED: Impermissible Errors Detected" else "TEST PASSED"
                    Text(verdictText, style = MaterialTheme.typography.titleMedium, fontWeight = FontWeight.Bold, color = statusColor)
                }"""

content = content.replace(target, new_target)

with open("app/src/main/java/com/example/ui/PreviewScreen.kt", "w") as f:
    f.write(content)
