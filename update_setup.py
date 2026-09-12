with open('app/src/main/java/com/example/ui/SetupScreen.kt', 'r') as f:
    content = f.read()

# We want to remove the call to InstrumentCatalogSection inside SetupScreen
call_block = """        InstrumentCatalogSection(
            catalog = catalog,
            onSelect = { item ->
                manufacturer = item.manufacturer
                model = item.model
                accuracyClass = item.accuracyClass
                
                // Convert kg to internal kg fields if needed. But let's assume the fields expect what's typed
                // Wait, if it says unit: "g" but field says "Max (kg)", we should convert it!
                val mx = if (item.unit == "g") item.maxCapacity / 1000 else item.maxCapacity
                val scInt = if (item.unit == "g") item.scaleInterval / 1000 else if (item.unit == "mg") item.scaleInterval / 1000000 else item.scaleInterval
                
                // format without trailing zeros if possible
                fun fmt(v: Double): String = if (v == v.toLong().toDouble()) v.toLong().toString() else v.toString()
                
                val mnInt = if (item.unit == "g") item.minCapacity / 1000 else if (item.unit == "mg") item.minCapacity / 1000000 else item.minCapacity
                minCapacity = fmt(mnInt)
                maxCapacity = fmt(mx)
                e = fmt(scInt)
            }
        )
        Spacer(modifier = Modifier.height(24.dp))
        Text("Manual Details Entry", style = MaterialTheme.typography.titleLarge, fontWeight = FontWeight.Bold, color = TextDark)
        Spacer(modifier = Modifier.height(24.dp))"""

if call_block in content:
    content = content.replace(call_block, "")
else:
    print("Could not find call block")

# We also want to remove the function definition of InstrumentCatalogSection. 
# It's at the end of the file.
import re
pattern = re.compile(r'fun InstrumentCatalogSection\(.*', re.DOTALL)
content = pattern.sub('', content)

with open('app/src/main/java/com/example/ui/SetupScreen.kt', 'w') as f:
    f.write(content)
