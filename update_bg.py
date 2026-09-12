with open("app/src/main/java/com/example/ui/LoginScreen.kt", "r") as f:
    content = f.read()

import_str = "import androidx.compose.material.icons.outlined.Speed\nimport androidx.compose.material.icons.outlined.Straighten\nimport androidx.compose.material.icons.outlined.Build\n"
content = content.replace("import androidx.compose.material.icons.outlined.Speed\n", import_str)

bg_icons = """        // Background icons to simulate the tools
        Icon(
            imageVector = Icons.Outlined.Straighten,
            contentDescription = null,
            modifier = Modifier
                .align(Alignment.TopEnd)
                .offset(x = (-30).dp, y = 150.dp)
                .size(80.dp)
                .drawBehind { 
                    // Rotate
                    drawContext.transform.rotate(45f)
                },
            tint = Color(0xFFD4C8EB).copy(alpha = 0.5f)
        )
        Icon(
            imageVector = Icons.Outlined.Build,
            contentDescription = null,
            modifier = Modifier
                .align(Alignment.CenterStart)
                .offset(x = (-10).dp, y = (-100).dp)
                .size(70.dp),
            tint = Color(0xFFD4C8EB).copy(alpha = 0.5f)
        )
"""

content = content.replace("        Column(", bg_icons + "        Column(")

with open("app/src/main/java/com/example/ui/LoginScreen.kt", "w") as f:
    f.write(content)

