sed -i 's/label = { Text(label) },/label = if (label.isNotEmpty()) { { Text(label) } } else null,/g' app/src/main/java/com/example/ui/SetupScreen.kt
