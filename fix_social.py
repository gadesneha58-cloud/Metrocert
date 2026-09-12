with open("app/src/main/java/com/example/ui/LoginScreen.kt", "r") as f:
    content = f.read()

# Replace the Row containing SocialButtonText calls
old_row = """                    Row(
                        horizontalArrangement = Arrangement.spacedBy(20.dp),
                        modifier = Modifier.fillMaxWidth(),
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        SocialButtonText(text = "G", color = Color(0xFFEA4335), surfaceColor = surfaceColor, lightShadow = lightShadow, darkShadow = darkShadow)
                        SocialButtonText(text = "a", color = Color(0xFF34A853), surfaceColor = surfaceColor, lightShadow = lightShadow, darkShadow = darkShadow)
                        SocialButtonText(text = "Apple", color = Color.Black, surfaceColor = surfaceColor, lightShadow = lightShadow, darkShadow = darkShadow)
                    }"""
new_row = """                    Row(
                        horizontalArrangement = Arrangement.spacedBy(20.dp),
                        modifier = Modifier.fillMaxWidth(),
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        SocialButtonIcon(icon = GoogleIcon, surfaceColor = surfaceColor, lightShadow = lightShadow, darkShadow = darkShadow)
                        SocialButtonIcon(icon = AndroidIcon, surfaceColor = surfaceColor, lightShadow = lightShadow, darkShadow = darkShadow)
                        SocialButtonIcon(icon = AppleIcon, surfaceColor = surfaceColor, lightShadow = lightShadow, darkShadow = darkShadow)
                    }"""

content = content.replace(old_row, new_row)

old_fun = """@Composable
fun RowScope.SocialButtonText(text: String, color: Color, surfaceColor: Color, lightShadow: Color, darkShadow: Color) {
    Box(
        modifier = Modifier
            .weight(1f)
            .height(60.dp)
            .neoShadow(cornerRadius = 16.dp, lightShadowColor = lightShadow, darkShadowColor = darkShadow, elevation = 6.dp)
            .background(surfaceColor, RoundedCornerShape(16.dp))
            .clickable { },
        contentAlignment = Alignment.Center
    ) {
        Text(text = text, color = color, fontWeight = FontWeight.Bold, fontSize = 24.sp)
    }
}"""

new_fun = """@Composable
fun RowScope.SocialButtonIcon(icon: androidx.compose.ui.graphics.vector.ImageVector, surfaceColor: Color, lightShadow: Color, darkShadow: Color) {
    Box(
        modifier = Modifier
            .weight(1f)
            .height(60.dp)
            .neoShadow(cornerRadius = 16.dp, lightShadowColor = lightShadow, darkShadowColor = darkShadow, elevation = 6.dp)
            .background(surfaceColor, RoundedCornerShape(16.dp))
            .clickable { },
        contentAlignment = Alignment.Center
    ) {
        Icon(
            imageVector = icon,
            contentDescription = null,
            modifier = Modifier.size(32.dp),
            tint = Color.Unspecified
        )
    }
}"""

content = content.replace(old_fun, new_fun)

with open("app/src/main/java/com/example/ui/LoginScreen.kt", "w") as f:
    f.write(content)

