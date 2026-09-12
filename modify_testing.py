import re

with open("app/src/main/java/com/example/ui/TestingScreen.kt", "r") as f:
    content = f.read()

# Let's remove the autoFill and autoFillFailing functions inside TestingScreen.kt
func_pattern = re.compile(r'    fun autoFill\(\) \{.*?    \}\n\n    fun autoFillFailing\(\) \{.*?    \}', re.DOTALL)
content = func_pattern.sub('', content)

# Remove the Top Command Bar for Demo Auto-Population
box_pattern = re.compile(r'        // Top Command Bar for Demo Auto-Population.*?Spacer\(modifier = Modifier.height\(20.dp\)\)', re.DOTALL)
content = box_pattern.sub('', content)

with open("app/src/main/java/com/example/ui/TestingScreen.kt", "w") as f:
    f.write(content)
