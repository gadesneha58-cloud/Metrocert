with open('app/src/main/java/com/example/MetroCertViewModel.kt', 'r') as f:
    content = f.read()

old_fun = """    fun updateInstrumentDetails(
        manufacturer: String, model: String, serial: String, certNo: String,
        accuracyClass: String, maxCapacity: Double, e: Double
    ) {
        val minCapacity = 20 * e
        val n = if (e > 0) maxCapacity / e else 0.0
        updateCurrentReport {
            it.copy(
                manufacturer = manufacturer, modelNumber = model, serialNumber = serial, certificateNo = certNo,
                accuracyClass = accuracyClass, maxCapacity = maxCapacity, e = e, minCapacity = minCapacity, n = n
            )
        }
    }"""

new_fun = """    fun updateInstrumentDetails(
        manufacturer: String, model: String, serial: String, certNo: String,
        accuracyClass: String, maxCapacity: Double, e: Double, minCapacity: Double
    ) {
        val n = if (e > 0) maxCapacity / e else 0.0
        updateCurrentReport {
            it.copy(
                manufacturer = manufacturer, modelNumber = model, serialNumber = serial, certificateNo = certNo,
                accuracyClass = accuracyClass, maxCapacity = maxCapacity, e = e, minCapacity = minCapacity, n = n
            )
        }
    }"""

content = content.replace(old_fun, new_fun)

with open('app/src/main/java/com/example/MetroCertViewModel.kt', 'w') as f:
    f.write(content)
