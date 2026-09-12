with open('app/src/main/java/com/example/ui/ScaleGalleryScreen.kt', 'r') as f:
    content = f.read()

content = content.replace(
    'fun ScaleGalleryScreen(viewModel: MetroCertViewModel, onInstrumentSelected: (InstrumentCatalogItem) -> Unit) {',
    'fun ScaleGalleryScreen(viewModel: MetroCertViewModel, onInstrumentSelected: (InstrumentCatalogItem) -> Unit, onManualEntry: () -> Unit) {'
)

# Add manual entry button next to the title
title_block = """            Text(
                "Instrument Catalog", 
                style = MaterialTheme.typography.titleLarge, 
                fontWeight = FontWeight.Bold, 
                color = TextDark
            )"""

new_title_block = """            Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween, verticalAlignment = Alignment.CenterVertically) {
                Text(
                    "Instrument Catalog", 
                    style = MaterialTheme.typography.titleLarge, 
                    fontWeight = FontWeight.Bold, 
                    color = TextDark
                )
                TextButton(onClick = onManualEntry) {
                    Text("Enter Manually", color = NeoAccent, fontWeight = FontWeight.Bold)
                }
            }"""

content = content.replace(title_block, new_title_block)

with open('app/src/main/java/com/example/ui/ScaleGalleryScreen.kt', 'w') as f:
    f.write(content)
