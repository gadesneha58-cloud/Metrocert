with open('app/src/main/java/com/example/MetroCertViewModel.kt', 'r') as f:
    content = f.read()

replacement = """    fun deleteMachine(index: Int) {
        if (_activeReports.value.size > 1 && index in _activeReports.value.indices) {
            _activeReports.update { it.filterIndexed { i, _ -> i != index } }
            
            // Shift the testing states
            val newStates = mutableMapOf<Int, com.example.ui.TestingState>()
            for ((k, v) in testingStates) {
                if (k < index) newStates[k] = v
                else if (k > index) newStates[k - 1] = v
            }
            testingStates.clear()
            testingStates.putAll(newStates)
            
            if (_currentIndex.value >= _activeReports.value.size) {
                _currentIndex.value = _activeReports.value.size - 1
            }
        } else if (_activeReports.value.size == 1 && index == 0) {
            // Reset if it's the last one
            _activeReports.update { listOf(Report()) }
            _currentIndex.value = 0
            testingStates.clear()
        }
    }"""

import re
content = re.sub(r'    fun deleteMachine\(index: Int\) \{[\s\S]*?\}', replacement, content)

with open('app/src/main/java/com/example/MetroCertViewModel.kt', 'w') as f:
    f.write(content)
