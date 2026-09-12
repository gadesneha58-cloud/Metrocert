with open('app/src/main/java/com/example/ui/MetroCertApp.kt', 'r') as f:
    content = f.read()

content = content.replace(
    '.clickable { viewModel.addMachine() }',
    '.clickable { navController.navigate(MetroCertRoute.Gallery.name) }'
)

# Replace the composable for Gallery to include onManualEntry
old_gallery = """                    composable(MetroCertRoute.Gallery.name) {
                        ScaleGalleryScreen(viewModel, onInstrumentSelected = { item ->
                            viewModel.startNewInspectionWithInstrument(item)
                            navController.navigate(MetroCertRoute.Setup.name)
                        })
                    }"""

new_gallery = """                    composable(MetroCertRoute.Gallery.name) {
                        ScaleGalleryScreen(
                            viewModel = viewModel, 
                            onInstrumentSelected = { item ->
                                viewModel.startNewInspectionWithInstrument(item)
                                navController.navigate(MetroCertRoute.Setup.name)
                            },
                            onManualEntry = {
                                viewModel.startNewInspection()
                                navController.navigate(MetroCertRoute.Setup.name)
                            }
                        )
                    }"""

content = content.replace(old_gallery, new_gallery)

with open('app/src/main/java/com/example/ui/MetroCertApp.kt', 'w') as f:
    f.write(content)
