import re

with open("app/src/main/java/com/example/ui/SetupScreen.kt", "r") as f:
    content = f.read()

# Replace applyDemoData()
func_pattern = re.compile(r'    fun applyDemoData\(\) \{.*?viewModel\.autoPopulateDemoSetup\(\)\n    \}', re.DOTALL)
new_func = """    fun applyDemoData(pass: Boolean) {
        manufacturer = "Mettler Toledo"
        model = "ICS689 Precision"
        serial = "MT-2026-XPR984"
        certNo = "CERT-OIML-2026-088"
        accuracyClass = "III"
        minCapacity = "0.1"
        maxCapacity = "30"
        e = "0.005"
        temp = "20.0"
        humidity = "50.0"
        pressure = "1013.25"
        standardId = "OIML-E2-STD-2026"
        nValidationError = null
        viewModel.autoPopulateFullDemo(pass = pass)
    }"""
content = func_pattern.sub(new_func, content)

with open("app/src/main/java/com/example/ui/SetupScreen.kt", "w") as f:
    f.write(content)

