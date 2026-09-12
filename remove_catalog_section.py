import re

with open('app/src/main/java/com/example/ui/SetupScreen.kt', 'r') as f:
    content = f.read()

# Remove the call
call_pattern = re.compile(r'        InstrumentCatalogSection\(.*?\}\n        \)\n        Spacer\(modifier = Modifier\.height\(24\.dp\)\)\n        Text\("Manual Details Entry".*?\n        Spacer\(modifier = Modifier\.height\(24\.dp\)\)', re.DOTALL)
content = call_pattern.sub('', content)

# Remove the function definition
func_pattern = re.compile(r'@Composable\nfun InstrumentCatalogSection\(.*', re.DOTALL)
content = func_pattern.sub('', content)

with open('app/src/main/java/com/example/ui/SetupScreen.kt', 'w') as f:
    f.write(content)
