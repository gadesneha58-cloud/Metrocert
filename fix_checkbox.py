with open("app/src/main/java/com/example/ui/LoginScreen.kt", "r") as f:
    content = f.read()

content = content.replace("import androidx.compose.ui.res.painterResource", "import androidx.compose.material.icons.filled.Check")

checkbox_old = """                                    Icon(
                                        painter = painterResource(android.R.drawable.checkbox_on_background), 
                                        contentDescription = null, 
                                        tint = primaryPurple, 
                                        modifier = Modifier.size(16.dp)
                                    )"""
checkbox_new = """                                    Icon(
                                        imageVector = Icons.Default.Check, 
                                        contentDescription = null, 
                                        tint = primaryPurple, 
                                        modifier = Modifier.size(16.dp)
                                    )"""
content = content.replace(checkbox_old, checkbox_new)

with open("app/src/main/java/com/example/ui/LoginScreen.kt", "w") as f:
    f.write(content)

