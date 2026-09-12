with open("app/src/main/java/com/example/ui/TestingScreen.kt", "r") as f:
    lines = f.readlines()

while lines and lines[-1].strip() == "":
    lines.pop()
    
if lines and lines[-1].strip() == "}":
    # Let's count open and close braces overall
    content = "".join(lines)
    open_b = content.count("{")
    close_b = content.count("}")
    while close_b > open_b and lines[-1].strip() == "}":
        lines.pop()
        content = "".join(lines)
        close_b = content.count("}")

with open("app/src/main/java/com/example/ui/TestingScreen.kt", "w") as f:
    f.writelines(lines)
