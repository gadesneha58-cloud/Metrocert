with open('app/src/main/java/com/example/ui/TestingScreen.kt', 'r') as f:
    content = f.read()

# Fix NeoTextField values
import re
content = re.sub(r'value = (state\.t\d+(?:Up|Down|Readings|Gross|Errors)\[.*?\]),', r'value = \1 ?: "",', content)

with open('app/src/main/java/com/example/ui/TestingScreen.kt', 'w') as f:
    f.write(content)

