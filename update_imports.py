with open('app/src/main/java/com/example/ui/ConfigScreen.kt', 'r') as f:
    content = f.read()

imports = """
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Description
import androidx.compose.material.icons.filled.Info
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.getValue
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
"""

if "import androidx.compose.ui.Alignment" not in content:
    content = content.replace('import androidx.compose.ui.Modifier', imports + '\nimport androidx.compose.ui.Modifier')

with open('app/src/main/java/com/example/ui/ConfigScreen.kt', 'w') as f:
    f.write(content)
