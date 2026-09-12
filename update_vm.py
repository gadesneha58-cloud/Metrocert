with open('app/src/main/java/com/example/MetroCertViewModel.kt', 'r') as f:
    content = f.read()

new_method = """
    fun startNewInspectionWithInstrument(item: InstrumentCatalogItem) {
        startNewInspection()
        updateInstrumentDetails(
            manufacturer = item.manufacturer,
            model = item.model,
            serial = "",
            certNo = "",
            accuracyClass = item.accuracyClass,
            maxCapacity = item.maxCapacity,
            e = item.scaleInterval,
            minCapacity = item.minCapacity
        )
    }
"""
if "startNewInspectionWithInstrument" not in content:
    content = content.replace("fun addMachine() {", new_method + "\n    fun addMachine() {")
    with open('app/src/main/java/com/example/MetroCertViewModel.kt', 'w') as f:
        f.write(content)
