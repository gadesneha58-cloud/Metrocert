import re

with open('app/src/main/java/com/example/ui/MetroCertApp.kt', 'r') as f:
    content = f.read()

# Make the bottom bar only show Dashboard and Config
pattern = re.compile(r'val tabs = MetroCertRoute\.values\(\)\.toList\(\)')
content = pattern.sub('val tabs = listOf(MetroCertRoute.Dashboard, MetroCertRoute.Config)', content)

# Remove Dashboard from bottom if current route is not one of them
# Wait, let's just only show the bottom bar if the route is Dashboard or Config
pattern2 = re.compile(r'bottomBar = \{\n\s*Box\(')
content = pattern2.sub('''bottomBar = {
            if (currentRoute in listOf(MetroCertRoute.Dashboard.name, MetroCertRoute.Config.name)) {
            Box(''', content)

# We need to close the if statement
# The Box ends before the `) { innerPadding ->`
pattern3 = re.compile(r'(\s*)\}\n\s*\) \{ innerPadding ->')
content = pattern3.sub(r'\1}\n            }\n        }\n    ) { innerPadding ->', content)

with open('app/src/main/java/com/example/ui/MetroCertApp.kt', 'w') as f:
    f.write(content)
