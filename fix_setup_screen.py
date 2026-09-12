import re

with open('app/src/main/java/com/example/ui/SetupScreen.kt', 'r') as f:
    content = f.read()

# Remove the Top Command Bar for Demo Auto-Population block
pattern = re.compile(r'\s*// Top Command Bar for Demo Auto-Population.*?Spacer\(modifier = Modifier\.height\(20\.dp\)\)', re.DOTALL)
content = pattern.sub('', content)

with open('app/src/main/java/com/example/ui/SetupScreen.kt', 'w') as f:
    f.write(content)
