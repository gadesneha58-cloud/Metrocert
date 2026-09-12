with open('app/src/main/java/com/example/ui/MetroCertApp.kt', 'r') as f:
    content = f.read()

import re
# We want to remove the Surface inside actions = { ... }
# up to the var menuExpanded line.

pattern = re.compile(r'actions = \{.*?var menuExpanded', re.DOTALL)
content = pattern.sub('actions = {\n                    var menuExpanded', content)

with open('app/src/main/java/com/example/ui/MetroCertApp.kt', 'w') as f:
    f.write(content)
