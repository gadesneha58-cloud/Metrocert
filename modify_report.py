import re

with open("app/src/main/java/com/example/data/Report.kt", "r") as f:
    content = f.read()

# Add isInService: Boolean = false to Report data class
if "val isInService: Boolean = false" not in content:
    content = content.replace("val accuracyClass: String = \"III\",", "val accuracyClass: String = \"III\",\n    val isInService: Boolean = false,")
    with open("app/src/main/java/com/example/data/Report.kt", "w") as f:
        f.write(content)

