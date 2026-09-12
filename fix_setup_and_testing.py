import re

with open("app/src/main/java/com/example/ui/SetupScreen.kt", "r") as f:
    content = f.read()

content = content.replace("applyDemoData(pass = true)", "applyDemoData(true)")
content = content.replace("applyDemoData(pass = false)", "applyDemoData(false)")

with open("app/src/main/java/com/example/ui/SetupScreen.kt", "w") as f:
    f.write(content)

