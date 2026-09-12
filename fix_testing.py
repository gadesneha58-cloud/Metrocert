with open("app/src/main/java/com/example/ui/TestingScreen.kt", "r") as f:
    content = f.read()

if content.strip().endswith("}\n}"):
    content = content.strip()[:-1].strip()

with open("app/src/main/java/com/example/ui/TestingScreen.kt", "w") as f:
    f.write(content)
