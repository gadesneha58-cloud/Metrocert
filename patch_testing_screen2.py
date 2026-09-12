import re

with open("app/src/main/java/com/example/ui/TestingScreen.kt", "r") as f:
    content = f.read()

# Add dialog state variables
state_vars = """    val state = viewModel.getTestingState(currentIndex)"""

new_state_vars = """    val state = viewModel.getTestingState(currentIndex)
    var showFailDialog by remember { mutableStateOf(false) }
    var failedTestsList by remember { mutableStateOf(listOf<String>()) }"""

if state_vars in content:
    content = content.replace(state_vars, new_state_vars)
else:
    print("Could not find state_vars to replace")


with open("app/src/main/java/com/example/ui/TestingScreen.kt", "w") as f:
    f.write(content)

