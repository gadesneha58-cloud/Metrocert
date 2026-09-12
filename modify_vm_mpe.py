with open("app/src/main/java/com/example/MetroCertViewModel.kt", "r") as f:
    content = f.read()

content = content.replace("RulesConfig.getMpe(load / e, c, e)", "RulesConfig.getMpe(load / e, c, e, report.isInService)")

# Also, we need to add isInService to updateInstrumentDetails
old_update = """    fun updateInstrumentDetails(
        manufacturer: String, model: String, serial: String, certNo: String,
        accuracyClass: String, minCapacity: Double, maxCapacity: Double, e: Double
    ) {"""

new_update = """    fun updateInstrumentDetails(
        manufacturer: String, model: String, serial: String, certNo: String,
        accuracyClass: String, minCapacity: Double, maxCapacity: Double, e: Double, isInService: Boolean = false
    ) {"""

content = content.replace(old_update, new_update)

old_update_body = """            it.copy(
                manufacturer = manufacturer, modelNumber = model, serialNumber = serial,
                certificateNo = certNo, accuracyClass = accuracyClass, minCapacity = minCapacity,
                maxCapacity = maxCapacity, e = e, n = n
            )"""
new_update_body = """            it.copy(
                manufacturer = manufacturer, modelNumber = model, serialNumber = serial,
                certificateNo = certNo, accuracyClass = accuracyClass, minCapacity = minCapacity,
                maxCapacity = maxCapacity, e = e, n = n, isInService = isInService
            )"""

content = content.replace(old_update_body, new_update_body)

with open("app/src/main/java/com/example/MetroCertViewModel.kt", "w") as f:
    f.write(content)
