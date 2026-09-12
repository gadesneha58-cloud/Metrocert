import re

with open('app/src/main/java/com/example/ui/ScaleGalleryScreen.kt', 'r') as f:
    content = f.read()

content = content.replace('an\nAccuracy', 'an\\nAccuracy')

with open('app/src/main/java/com/example/ui/ScaleGalleryScreen.kt', 'w') as f:
    f.write(content)

with open('app/src/main/java/com/example/ui/SetupScreen.kt', 'r') as f:
    content = f.read()

content = content.replace('androidx.compose.ui.unit.sp.TextUnit', 'androidx.compose.ui.unit.sp')
content = content.replace('textStyle = androidx.compose.material3.LocalTextStyle.current.copy(fontSize = androidx.compose.ui.unit.sp(16f, androidx.compose.ui.unit.TextUnitType.Sp)),', 'textStyle = androidx.compose.material3.LocalTextStyle.current.copy(fontSize = androidx.compose.ui.unit.TextUnit(16f, androidx.compose.ui.unit.TextUnitType.Sp)),')

with open('app/src/main/java/com/example/ui/SetupScreen.kt', 'w') as f:
    f.write(content)
