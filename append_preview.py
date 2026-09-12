with open('app/src/main/java/com/example/ui/PreviewScreen.kt', 'r') as f:
    content = f.read()

target = """                Spacer(modifier = Modifier.height(24.dp))
                HorizontalDivider(color = NeoBackground)
                Spacer(modifier = Modifier.height(16.dp))
                
                Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween) {"""

new_target = """                Spacer(modifier = Modifier.height(24.dp))
                HorizontalDivider(color = NeoBackground)
                Spacer(modifier = Modifier.height(16.dp))
                
                if (report.digitalSignature.isNotEmpty()) {
                    Text("Digital Signature: ${report.digitalSignature}", style = MaterialTheme.typography.bodyMedium, color = TextDark)
                }
                if (report.photoPaths.isNotEmpty()) {
                    Text("Attachments: ${report.photoPaths.size} photo(s) attached.", style = MaterialTheme.typography.bodyMedium, color = TextDark)
                }
                
                Spacer(modifier = Modifier.height(16.dp))
                Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween) {"""

content = content.replace(target, new_target)

with open('app/src/main/java/com/example/ui/PreviewScreen.kt', 'w') as f:
    f.write(content)
