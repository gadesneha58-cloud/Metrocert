with open('app/src/main/java/com/example/ui/SetupScreen.kt', 'r') as f:
    content = f.read()

bad_block = """                    viewModel.updateEnvironment(
                        temp = temp.toDoubleOrNull() ?: 20.0,
                        humidity = humidity.toDoubleOrNull() ?: 50.0,
                        pressure = pressure.toDoubleOrNull() ?: 1013.25
                    )
                    viewModel.updateStandardWeight(standardId)"""

good_block = """                    viewModel.updateEnvironmentalConditions(
                        temp = temp.toDoubleOrNull() ?: 20.0,
                        humidity = humidity.toDoubleOrNull() ?: 50.0,
                        pressure = pressure.toDoubleOrNull() ?: 1013.25,
                        standardId = standardId
                    )"""

content = content.replace(bad_block, good_block)

with open('app/src/main/java/com/example/ui/SetupScreen.kt', 'w') as f:
    f.write(content)
