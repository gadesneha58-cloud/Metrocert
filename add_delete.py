with open('app/src/main/java/com/example/MetroCertViewModel.kt', 'r') as f:
    content = f.read()

replacement = """    fun switchMachine(index: Int) {
        if (index in _activeReports.value.indices) {
            _currentIndex.value = index
        }
    }

    fun deleteMachine(index: Int) {
        if (_activeReports.value.size > 1 && index in _activeReports.value.indices) {
            _activeReports.update { it.filterIndexed { i, _ -> i != index } }
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

content = content.replace("""    fun switchMachine(index: Int) {
        if (index in _activeReports.value.indices) {
            _currentIndex.value = index
        }
    }""", replacement)

with open('app/src/main/java/com/example/MetroCertViewModel.kt', 'w') as f:
    f.write(content)
