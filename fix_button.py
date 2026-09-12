with open("app/src/main/java/com/example/ui/LoginScreen.kt", "r") as f:
    content = f.read()

btn_old = """                    Button(
                        onClick = onSignInClick,
                        modifier = Modifier
                            .fillMaxWidth()
                            .height(56.dp)
                            .shadow(8.dp, RoundedCornerShape(16.dp), spotColor = primaryPurple),
                        shape = RoundedCornerShape(16.dp),
                        colors = ButtonDefaults.buttonColors(containerColor = primaryPurple)
                    ) {
                        Text("Login", fontSize = 18.sp, fontWeight = FontWeight.Bold, color = Color.White)
                    }"""

btn_new = """                    Box(
                        modifier = Modifier
                            .fillMaxWidth()
                            .height(56.dp)
                            .shadow(8.dp, RoundedCornerShape(16.dp), spotColor = primaryPurple, ambientColor = primaryPurple)
                            .background(
                                brush = Brush.horizontalGradient(
                                    colors = listOf(Color(0xFF8E54E9), Color(0xFF5C33B5))
                                ),
                                shape = RoundedCornerShape(16.dp)
                            )
                            .clickable { onSignInClick() },
                        contentAlignment = Alignment.Center
                    ) {
                        Text("Login", fontSize = 18.sp, fontWeight = FontWeight.Bold, color = Color.White)
                    }"""

content = content.replace(btn_old, btn_new)

with open("app/src/main/java/com/example/ui/LoginScreen.kt", "w") as f:
    f.write(content)

