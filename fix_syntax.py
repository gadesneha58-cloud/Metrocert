with open("app/src/main/java/com/example/ui/TestingScreen.kt", "r") as f:
    content = f.read()

# Remove the trailing '}' if it's extra
content = content.strip()
if content.endswith("}\n}"):
    content = content[:-1].strip()

with open("app/src/main/java/com/example/ui/TestingScreen.kt", "w") as f:
    f.write(content)
