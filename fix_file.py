import re

with open('app/src/main/java/com/example/MetroCertViewModel.kt', 'r') as f:
    content = f.read()

# I will just replace from switchMachine to the end (or find the corrupted part)
# Actually, let's just find `fun deleteMachine` and replace the whole block manually
start_idx = content.find("fun switchMachine(index: Int)")
end_idx = content.find("private fun updateCurrentReport")

replacement = """fun switchMachine(index: Int) {
        if (index in _activeReports.value.indices) {
            _currentIndex.value = index
        }
    }

    fun deleteMachine(index: Int) {
        if (_activeReports.value.size > 1 && index in _activeReports.value.indices) {
            _activeReports.update { it.filterIndexed { i, _ -> i != index } }
            
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
            _activeReports.update { listOf(Report()) }
            _currentIndex.value = 0
            testingStates.clear()
        }
    }

    """

content = content[:start_idx] + replacement + content[end_idx:]

with open('app/src/main/java/com/example/MetroCertViewModel.kt', 'w') as f:
    f.write(content)

