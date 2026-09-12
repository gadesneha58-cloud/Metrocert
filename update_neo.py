import re

with open('app/src/main/java/com/example/ui/SetupScreen.kt', 'r') as f:
    content = f.read()

pattern = re.compile(r'fun NeoTextField\(.*?modifier = modifier\.neoShadow.*?colors = TextFieldDefaults\.colors\(.*?\)\n    \)', re.DOTALL)

def replace(m):
    original = m.group(0)
    if 'textStyle' not in original:
        return original.replace('colors = TextFieldDefaults', 'textStyle = androidx.compose.material3.LocalTextStyle.current.copy(fontSize = androidx.compose.ui.unit.sp.TextUnit(16f, androidx.compose.ui.unit.TextUnitType.Sp)),\n        colors = TextFieldDefaults')
    return original

new_content = pattern.sub(replace, content)

with open('app/src/main/java/com/example/ui/SetupScreen.kt', 'w') as f:
    f.write(new_content)
