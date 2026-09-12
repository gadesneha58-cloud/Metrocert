import re

with open('app/src/main/java/com/example/MetroCertViewModel.kt', 'r') as f:
    content = f.read()

def replace_func(match):
    return """    private fun fetchOrSeedCatalog() {
        val seedData = listOf(
            InstrumentCatalogItem("Mettler Toledo", "XPR Microbalance", "Micro-analytical", "I", 0.002, 0.0001, "kg", 0.000001, 0.000001),
            InstrumentCatalogItem("Sartorius", "Cubis II", "Micro-analytical", "I", 0.005, 0.0001, "kg", 0.000001, 0.000001),
            InstrumentCatalogItem("Sartorius", "Entris II", "Precision Balance", "II", 0.6, 0.02, "kg", 0.01, 0.001),
            InstrumentCatalogItem("OHAUS", "Explorer Precision", "Precision Balance", "II", 10.0, 0.5, "kg", 0.1, 0.01),
            InstrumentCatalogItem("CAS", "CL5200", "Retail Scale", "III", 15.0, 0.1, "kg", 0.005, 0.005),
            InstrumentCatalogItem("DIGI", "SM-120", "Retail POS", "III", 30.0, 0.2, "kg", 0.01, 0.01),
            InstrumentCatalogItem("Mettler Toledo", "ICS689", "Bench/Platform", "III", 60.0, 0.4, "kg", 0.02, 0.02),
            InstrumentCatalogItem("Avery Weigh-Tronix", "BridgeMont", "Weighbridge", "IIII", 80000.0, 400.0, "kg", 20.0, 20.0),
            InstrumentCatalogItem("Rice Lake", "Survivor OTR", "Truck Scale", "IIII", 100000.0, 500.0, "kg", 20.0, 20.0),
            InstrumentCatalogItem("Cardinal", "Armor Truck Scale", "Truck Scale", "IIII", 120000.0, 500.0, "kg", 20.0, 20.0)
        )
        _instrumentCatalog.value = seedData
    }"""

pattern = re.compile(r'    private fun fetchOrSeedCatalog\(\) \{.*?\n    \}', re.DOTALL)
content = pattern.sub(replace_func, content, count=1)

with open('app/src/main/java/com/example/MetroCertViewModel.kt', 'w') as f:
    f.write(content)
