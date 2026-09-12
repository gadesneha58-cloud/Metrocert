with open('app/src/main/java/com/example/ui/MetroCertApp.kt', 'r') as f:
    content = f.read()

import_statement = """import androidx.compose.ui.input.pointer.pointerInput
import androidx.compose.foundation.gestures.detectVerticalDragGestures
import androidx.compose.ui.unit.IntOffset
import kotlin.math.roundToInt
import kotlin.math.abs
"""

if "detectVerticalDragGestures" not in content:
    content = content.replace("import androidx.compose.ui.Modifier", import_statement + "import androidx.compose.ui.Modifier")

old_box = """                        val isSelected = index == currentIndex
                        Box(
                            modifier = Modifier
                                .neoShadow(cornerRadius = 16.dp, isPressed = isSelected)
                                .clip(RoundedCornerShape(16.dp))
                                .background(if (isSelected) NeoAccent else NeoSurface)
                                .clickable { viewModel.switchMachine(index) }
                                .padding(horizontal = 16.dp, vertical = 8.dp)
                        ) {
                            Text(
                                "Machine ${index + 1}",
                                color = if (isSelected) androidx.compose.ui.graphics.Color.White else TextDark,
                                fontWeight = androidx.compose.ui.text.font.FontWeight.Bold
                            )
                        }"""

new_box = """                        val isSelected = index == currentIndex
                        var offsetY by remember { mutableStateOf(0f) }
                        
                        Box(
                            modifier = Modifier
                                .offset { IntOffset(0, offsetY.roundToInt()) }
                                .neoShadow(cornerRadius = 16.dp, isPressed = isSelected)
                                .clip(RoundedCornerShape(16.dp))
                                .background(if (isSelected) NeoAccent else NeoSurface)
                                .pointerInput(Unit) {
                                    detectVerticalDragGestures(
                                        onDragEnd = {
                                            if (abs(offsetY) > 150f) {
                                                viewModel.deleteMachine(index)
                                            }
                                            offsetY = 0f
                                        },
                                        onDragCancel = {
                                            offsetY = 0f
                                        },
                                        onVerticalDrag = { change, dragAmount ->
                                            change.consume()
                                            offsetY += dragAmount
                                        }
                                    )
                                }
                                .clickable { viewModel.switchMachine(index) }
                                .padding(horizontal = 16.dp, vertical = 8.dp)
                        ) {
                            Text(
                                "Machine ${index + 1}",
                                color = if (isSelected) androidx.compose.ui.graphics.Color.White else TextDark,
                                fontWeight = androidx.compose.ui.text.font.FontWeight.Bold
                            )
                        }"""

content = content.replace(old_box, new_box)

with open('app/src/main/java/com/example/ui/MetroCertApp.kt', 'w') as f:
    f.write(content)

