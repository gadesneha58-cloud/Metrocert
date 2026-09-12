with open("app/src/main/java/com/example/ui/LoginScreen.kt", "r") as f:
    content = f.read()

content = content.replace("import androidx.compose.foundation.layout.*", "import androidx.compose.foundation.layout.*\nimport androidx.compose.foundation.rememberScrollState\nimport androidx.compose.foundation.verticalScroll")

col_old = """        Column(
            horizontalAlignment = Alignment.CenterHorizontally,
            modifier = Modifier
                .fillMaxWidth()
                .padding(24.dp)
        ) {"""

col_new = """        Column(
            horizontalAlignment = Alignment.CenterHorizontally,
            modifier = Modifier
                .fillMaxWidth()
                .verticalScroll(rememberScrollState())
                .padding(24.dp)
        ) {"""

content = content.replace(col_old, col_new)

with open("app/src/main/java/com/example/ui/LoginScreen.kt", "w") as f:
    f.write(content)

