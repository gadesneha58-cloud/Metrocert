with open('app/src/main/java/com/example/MetroCertViewModel.kt', 'r') as f:
    content = f.read()

missing = """
    val savedReports: StateFlow<List<Report>> = reportDao.getAllReports()
        .stateIn(viewModelScope, SharingStarted.Lazily, emptyList())
        
    private val _activeReports = MutableStateFlow(listOf(Report()))
    val activeReports = _activeReports.asStateFlow()

    private val _currentIndex = MutableStateFlow(0)
    val currentIndex = _currentIndex.asStateFlow()

    private val testingStates = mutableMapOf<Int, com.example.ui.TestingState>()

    fun getTestingState(index: Int): com.example.ui.TestingState {
        return testingStates.getOrPut(index) { com.example.ui.TestingState() }
    }

    private fun updateCurrentReport(update: (Report) -> Report) {
        val currentList = _activeReports.value.toMutableList()
        val index = _currentIndex.value
        if (index in currentList.indices) {
            currentList[index] = update(currentList[index])
            _activeReports.value = currentList
        }
    }

    fun switchMachine(index: Int) {
        if (index in _activeReports.value.indices) {
            _currentIndex.value = index
        }
    }

    fun deleteMachine(index: Int) {
        val currentList = _activeReports.value.toMutableList()
        if (index in currentList.indices) {
            currentList.removeAt(index)
            
            val newStates = mutableMapOf<Int, com.example.ui.TestingState>()
            testingStates.forEach { (k, v) ->
                if (k < index) newStates[k] = v
                else if (k > index) newStates[k - 1] = v
            }
            testingStates.clear()
            testingStates.putAll(newStates)

            if (currentList.isEmpty()) {
                currentList.add(Report())
                testingStates[0] = com.example.ui.TestingState()
                _currentIndex.value = 0
            } else {
                if (_currentIndex.value >= currentList.size) {
                    _currentIndex.value = currentList.size - 1
                }
            }
            _activeReports.value = currentList
        }
    }

    fun triggerAutoSave(index: Int) {}
    fun loadDraftFromFirestore(index: Int) {}

    fun updateEnvironmentalConditions(temp: Double, humidity: Double, pressure: Double, standardId: String) {
        updateCurrentReport { 
            it.copy(
                ambientTemp = temp,
                relativeHumidity = humidity,
                atmosphericPressure = pressure,
                standardWeightId = standardId
            )
        }
    }

    fun updateInstrumentDetails(manufacturer: String, model: String, serial: String, certNo: String, accuracyClass: String, maxCapacity: Double, e: Double, minCapacity: Double) {
        val n = if (e > 0) maxCapacity / e else 0.0
        updateCurrentReport {
            it.copy(
                manufacturer = manufacturer, modelNumber = model, serialNumber = serial, certificateNo = certNo,
                accuracyClass = accuracyClass, maxCapacity = maxCapacity, e = e, minCapacity = minCapacity, n = n
            )
        }
    }

"""

# insert it right before `fun processTests`
content = content.replace("    fun processTests", missing + "    fun processTests")

with open('app/src/main/java/com/example/MetroCertViewModel.kt', 'w') as f:
    f.write(content)
