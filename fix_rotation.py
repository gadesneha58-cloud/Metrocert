with open("app/src/main/java/com/example/ui/LoginScreen.kt", "r") as f:
    content = f.read()

import_str = "import androidx.compose.ui.draw.clip\nimport androidx.compose.ui.graphics.graphicsLayer\n"
content = content.replace("import androidx.compose.ui.draw.clip\nimport androidx.compose.ui.draw.drawBehind\n", import_str)

old_draw = """                .drawBehind { 
                    // Rotate
                    drawContext.transform.rotate(45f)
                }"""
new_draw = """                .graphicsLayer { rotationZ = 45f }"""
content = content.replace(old_draw, new_draw)

# Wait, there's another drawBehind error on line 156. Did I add it twice? 
# Oh, my sed replaced both? Wait. My script update_bg.py only had one `drawBehind`.
# Let's check where the other one is. 

with open("app/src/main/java/com/example/ui/LoginScreen.kt", "w") as f:
    f.write(content)

