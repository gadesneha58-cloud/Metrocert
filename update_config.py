import re

with open('app/src/main/java/com/example/ui/ConfigScreen.kt', 'r') as f:
    content = f.read()

# Add necessary imports
imports_to_add = """
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Description
import androidx.compose.material.icons.filled.Info
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.getValue
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
"""
content = content.replace('import androidx.compose.ui.theme.*', 'import androidx.compose.ui.theme.*\n' + imports_to_add)

# Change signature to opt-in to ExperimentalMaterial3Api
content = content.replace('@Composable\nfun ConfigScreen() {', '@OptIn(ExperimentalMaterial3Api::class)\n@Composable\nfun ConfigScreen() {\n    var showDocSheet by remember { mutableStateOf(false) }\n')

# Add the button and bottom sheet
doc_ui = """
        // Technical Documentation Button
        Button(
            onClick = { showDocSheet = true },
            modifier = Modifier.fillMaxWidth().padding(bottom = 24.dp),
            shape = RoundedCornerShape(16.dp),
            colors = ButtonDefaults.buttonColors(containerColor = NeoAccent),
            contentPadding = PaddingValues(vertical = 16.dp)
        ) {
            Icon(Icons.Default.Description, contentDescription = "Doc", modifier = Modifier.size(20.dp))
            Spacer(modifier = Modifier.width(8.dp))
            Text("View Technical Documentation", fontWeight = FontWeight.Bold, color = androidx.compose.ui.graphics.Color.White)
        }
        
        if (showDocSheet) {
            ModalBottomSheet(
                onDismissRequest = { showDocSheet = false },
                containerColor = NeoSurface,
                dragHandle = { BottomSheetDefaults.DragHandle(color = NeoAccent) }
            ) {
                Column(
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(horizontal = 24.dp, vertical = 16.dp)
                        .verticalScroll(rememberScrollState())
                ) {
                    Text("Technical Documentation", style = MaterialTheme.typography.headlineMedium, fontWeight = FontWeight.Bold, color = TextDark)
                    Spacer(modifier = Modifier.height(24.dp))
                    
                    DocSection(
                        title = "1. Software Architecture",
                        content = "• Pattern: MVVM (Model-View-ViewModel)\\n• UI Framework: Jetpack Compose (Declarative UI)\\n• Language: Kotlin\\n• State Management: StateFlow & State hoisting\\n• Local Persistence: Room Database (SQLite) for offline-first test history repository."
                    )
                    
                    DocSection(
                        title = "2. Calculation Methodology",
                        content = "• Standard: OIML R 76\\n• Logic: MPE (Maximum Permissible Error) is calculated dynamically based on the instrument's Accuracy Class (I, II, III, IIII).\\n• The applied load (m) is converted to verification scale intervals (e).\\n• MPE constraints (±0.5e, ±1.0e, ±1.5e) are enforced through automated threshold checks.\\n• Repeatability, eccentricity, and weighing errors are aggregated mathematically in real-time."
                    )
                    
                    DocSection(
                        title = "3. Deployment Framework",
                        content = "• Target: Native Android OS (Tablets and Smartphones)\\n• Output Formats: APK/AAB distribution.\\n• Reporting: On-device PDF generation utilizing native Android canvas APIs (no external cloud APIs required), providing standardized test reports."
                    )
                    
                    Spacer(modifier = Modifier.height(48.dp))
                }
            }
        }
"""

content = content.replace('Text("OIML R-76 MPE Thresholds & Constraints", style = MaterialTheme.typography.bodyMedium, color = TextMuted)\n        Spacer(modifier = Modifier.height(24.dp))', 'Text("OIML R-76 MPE Thresholds & Constraints", style = MaterialTheme.typography.bodyMedium, color = TextMuted)\n        Spacer(modifier = Modifier.height(24.dp))\n' + doc_ui)


doc_composable = """
@Composable
fun DocSection(title: String, content: String) {
    Column(modifier = Modifier.fillMaxWidth().padding(bottom = 24.dp)) {
        Row(verticalAlignment = Alignment.CenterVertically) {
            Icon(Icons.Default.Info, contentDescription = null, tint = NeoAccent, modifier = Modifier.size(18.dp))
            Spacer(modifier = Modifier.width(8.dp))
            Text(title, style = MaterialTheme.typography.titleMedium, fontWeight = FontWeight.Bold, color = TextDark)
        }
        Spacer(modifier = Modifier.height(8.dp))
        Box(
            modifier = Modifier
                .fillMaxWidth()
                .background(NeoBackground, RoundedCornerShape(12.dp))
                .padding(16.dp)
        ) {
            Text(content, style = MaterialTheme.typography.bodyMedium, color = TextMuted, lineHeight = androidx.compose.ui.unit.sp.TextUnit(22f, androidx.compose.ui.unit.TextUnitType.Sp))
        }
    }
}
"""
content += doc_composable

# Replace the textunit correctly
content = content.replace("androidx.compose.ui.unit.sp.TextUnit", "androidx.compose.ui.unit.TextUnit")

with open('app/src/main/java/com/example/ui/ConfigScreen.kt', 'w') as f:
    f.write(content)
