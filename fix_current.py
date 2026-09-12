with open('app/src/main/java/com/example/MetroCertViewModel.kt', 'r') as f:
    content = f.read()

missing2 = """
    val currentReport = combine(_activeReports, _currentIndex) { reports, index ->
        if (reports.isNotEmpty() && index in reports.indices) reports[index] else Report()
    }.stateIn(viewModelScope, SharingStarted.Lazily, Report())

    fun startNewInspection() {
        val currentList = _activeReports.value.toMutableList()
        currentList.add(Report())
        _activeReports.value = currentList
        _currentIndex.value = currentList.size - 1
        testingStates[_currentIndex.value] = com.example.ui.TestingState()
    }

    fun addMachine() {
        startNewInspection()
    }
"""

content = content.replace("    val currentIndex = _currentIndex.asStateFlow()", "    val currentIndex = _currentIndex.asStateFlow()\n" + missing2)

with open('app/src/main/java/com/example/MetroCertViewModel.kt', 'w') as f:
    f.write(content)
