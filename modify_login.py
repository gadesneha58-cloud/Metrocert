import re

with open("app/src/main/java/com/example/ui/LoginScreen.kt", "r") as f:
    content = f.read()

# Replace ic_menu_compass with a standard icon
content = content.replace('painter = painterResource(android.R.drawable.ic_menu_compass), // fallback placeholder', 'imageVector = androidx.compose.material.icons.Icons.Outlined.Star,')

# Replace SocialButton usages
social_buttons = """
                        SocialButtonText(text = "G", color = Color(0xFFDB4437))
                        SocialButtonText(text = "a", color = Color(0xFF3DDC84))
                        SocialButtonText(text = "Ap", color = Color.Black)
"""
content = re.sub(r'SocialButton\(iconRes = .*?\n.*?\n.*?\)', social_buttons, content, flags=re.MULTILINE|re.DOTALL)

# Add SocialButtonText composable
social_button_text = """
@Composable
fun RowScope.SocialButtonText(text: String, color: Color) {
    Box(
        modifier = Modifier
            .weight(1f)
            .height(56.dp)
            .shadow(4.dp, RoundedCornerShape(16.dp))
            .background(Color.White, RoundedCornerShape(16.dp))
            .clickable { },
        contentAlignment = Alignment.Center
    ) {
        Text(text = text, color = color, fontWeight = FontWeight.Bold, fontSize = 24.sp)
    }
}
"""

content = content.replace('@Composable\nfun RowScope.SocialButton', social_button_text + '\n@Composable\nfun RowScope.SocialButton')

# Remove unused SocialButton to avoid any errors, or just let it be. Let's remove it.
content = re.sub(r'@Composable\s*fun RowScope\.SocialButton\(iconRes: Int, color: Color\) \{[\s\S]*?\}', '', content)

with open("app/src/main/java/com/example/ui/LoginScreen.kt", "w") as f:
    f.write(content)

