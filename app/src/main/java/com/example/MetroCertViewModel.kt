package com.example

import android.app.Application
import androidx.lifecycle.AndroidViewModel
import androidx.lifecycle.viewModelScope
import com.example.data.*
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.SharingStarted
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.combine
import kotlinx.coroutines.flow.stateIn
import kotlinx.coroutines.flow.update
import kotlinx.coroutines.launch
import kotlin.math.abs

import android.content.Context
import android.util.Log
import com.google.firebase.firestore.FirebaseFirestore
import kotlinx.coroutines.Job
import kotlinx.coroutines.delay

class MetroCertViewModel(application: Application) : AndroidViewModel(application) {
    private val reportDao = AppDatabase.getDatabase(application).reportDao()
    private val prefs = application.getSharedPreferences("metrocert_prefs", Context.MODE_PRIVATE)
    
    private var firestore: FirebaseFirestore? = null
    private var autoSaveJob: Job? = null

    private val _instrumentCatalog = MutableStateFlow<List<InstrumentCatalogItem>>(emptyList())
    val instrumentCatalog = _instrumentCatalog.asStateFlow()

    init {
        try {
            firestore = FirebaseFirestore.getInstance()
            Log.d("MetroCert", "Firestore initialized for auto-save")
            fetchOrSeedCatalog()
        } catch (e: Exception) {
            Log.w("MetroCert", "Firestore not initialized (missing google-services.json). Falling back to local auto-save.", e)
            fetchOrSeedCatalog()
        }
    }
    
    private fun fetchOrSeedCatalog() {
        val seedData = listOf(
            InstrumentCatalogItem("Mettler Toledo", "XPR Microbalance", "Micro-analytical", "I", 0.002, 0.0001, "kg", 0.000001, 0.000001),
            InstrumentCatalogItem("Sartorius", "Cubis II", "Micro-analytical", "I", 0.005, 0.0001, "kg", 0.000001, 0.000001),
            InstrumentCatalogItem("Sartorius", "Entris II", "Precision Balance", "II", 0.6, 0.02, "kg", 0.01, 0.001),
            InstrumentCatalogItem("OHAUS", "Explorer Precision", "Precision Balance", "II", 10.0, 0.5, "kg", 0.1, 0.01),
            InstrumentCatalogItem("CAS", "CL5200", "Retail Scale", "III", 15.0, 0.1, "kg", 0.005, 0.005),
            InstrumentCatalogItem("DIGI", "SM-120", "Retail POS", "III", 30.0, 0.2, "kg", 0.01, 0.01),
            InstrumentCatalogItem("Mettler Toledo", "ICS689", "Bench/Platform", "III", 60.0, 0.4, "kg", 0.02, 0.02),
            InstrumentCatalogItem("Avery Weigh-Tronix", "BridgeMont", "Weighbridge", "IIII", 80000.0, 400.0, "kg", 20.0, 20.0),
            InstrumentCatalogItem("Rice Lake", "Survivor OTR", "Truck Scale", "IIII", 100000.0, 500.0, "kg", 20.0, 20.0),
            InstrumentCatalogItem("Cardinal", "Armor Truck Scale", "Truck Scale", "IIII", 120000.0, 500.0, "kg", 20.0, 20.0)
        )
        _instrumentCatalog.value = seedData
    }



    val savedReports: StateFlow<List<Report>> = reportDao.getAllReports()
        .stateIn(viewModelScope, SharingStarted.Lazily, emptyList())
        
    private val _activeReports = MutableStateFlow(listOf(Report()))
    val activeReports = _activeReports.asStateFlow()

    private val _currentIndex = MutableStateFlow(0)
    val currentIndex = _currentIndex.asStateFlow()

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

    
    fun startNewInspectionWithInstrument(item: InstrumentCatalogItem) {
        startNewInspection()
        updateInstrumentDetails(
            manufacturer = item.manufacturer,
            model = item.model,
            serial = "",
            certNo = "",
            accuracyClass = item.accuracyClass,
            maxCapacity = item.maxCapacity,
            e = item.scaleInterval,
            minCapacity = item.minCapacity
        )
    }

    fun addMachine() {
        startNewInspection()
    }


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

    fun updateInstrumentDetails(manufacturer: String, model: String, serial: String, certNo: String, accuracyClass: String, maxCapacity: Double, e: Double, minCapacity: Double, isInService: Boolean = false) {
        val n = if (e > 0) maxCapacity / e else 0.0
        updateCurrentReport {
            it.copy(
                manufacturer = manufacturer, modelNumber = model, serialNumber = serial, certificateNo = certNo,
                accuracyClass = accuracyClass, maxCapacity = maxCapacity, e = e, minCapacity = minCapacity, n = n, isInService = isInService
            )
        }
    }

    fun autoPopulateDemoSetup(index: Int = _currentIndex.value) {
        val currentList = _activeReports.value.toMutableList()
        if (currentList.isEmpty()) {
            startNewInspection()
        }
        val targetIndex = if (index in currentList.indices) index else _currentIndex.value
        _currentIndex.value = targetIndex
        
        updateInstrumentDetails(
            manufacturer = "Mettler Toledo",
            model = "ICS689 Precision",
            serial = "MT-2026-XPR984",
            certNo = "CERT-OIML-2026-088",
            accuracyClass = "III",
            maxCapacity = 30.0,
            e = 0.005,
            minCapacity = 0.1
        )
        updateEnvironmentalConditions(
            temp = 20.0,
            humidity = 50.0,
            pressure = 1013.25,
            standardId = "OIML-E2-STD-2026"
        )
    }

    fun autoPopulateDemoTests(index: Int = _currentIndex.value, pass: Boolean = true) {
        val currentList = _activeReports.value
        val report = if (index in currentList.indices) currentList[index] else Report()
        val maxCap = if (report.maxCapacity > 0.0) report.maxCapacity else 30.0
        val e = if (report.e > 0.0) report.e else 0.005
        val minCap = if (report.minCapacity > 0.0) report.minCapacity else 0.1

        val t1Loads = listOf(minCap, maxCap * 0.25, maxCap * 0.5, maxCap * 0.75, maxCap)
        val t3Load = maxCap / 3
        val t4BaseLoad = minCap
        val t4ExtraLoad = 1.4 * e
        val t5Load = maxCap * 0.8
        val t6Load = maxCap * 0.5
        val t7Load = maxCap * 0.5
        val t8Load = maxCap
        val t9Loads = listOf(minCap, maxCap * 0.5, maxCap * 0.9)
        val t10Load = maxCap * 0.5
        val t11Load = maxCap * 0.5
        val t13Load = maxCap * 0.5

        val state = getTestingState(index)
        if (pass) {
            state.autoFillPassingData(
                t1Loads = t1Loads, t3Load = t3Load, t4BaseLoad = t4BaseLoad, t4ExtraLoad = t4ExtraLoad,
                e = e, t5Load = t5Load, t6Load = t6Load, t7Load = t7Load, t8Load = t8Load,
                t9Loads = t9Loads, t10Load = t10Load, t11Load = t11Load, t13Load = t13Load, maxCap = maxCap
            )
        } else {
            state.autoFillFailingData(
                t1Loads = t1Loads, t3Load = t3Load, t4BaseLoad = t4BaseLoad, t4ExtraLoad = t4ExtraLoad,
                e = e, t5Load = t5Load, t6Load = t6Load, t7Load = t7Load, t8Load = t8Load,
                t9Loads = t9Loads, t10Load = t10Load, t11Load = t11Load, t13Load = t13Load, maxCap = maxCap
            )
        }
    }

    fun autoPopulateFullDemo(index: Int = _currentIndex.value, pass: Boolean = true) {
        autoPopulateDemoSetup(index)
        autoPopulateDemoTests(index, pass)
    }

    fun processTests(inputs: com.example.data.TestInputs) {
        val report = _activeReports.value[_currentIndex.value]
        val max = report.maxCapacity
        val e = report.e
        val c = report.accuracyClass
        
        fun mpe(load: Double): Double {
            return com.example.data.RulesConfig.getMpe(load / e, c, e, report.isInService)
        }

        val weighingResults = inputs.t1Loads.mapIndexed { i, load ->
            val up = inputs.t1Up[i].toDoubleOrNull() ?: 0.0
            val down = inputs.t1Down[i].toDoubleOrNull() ?: 0.0
            val errUp = up - load
            val errDown = down - load
            val m = mpe(load)
            com.example.data.WeighingResult(load, up, down, errUp, errDown, m, kotlin.math.abs(errUp) <= m && kotlin.math.abs(errDown) <= m)
        }

        val z1 = inputs.t2Z1.toDoubleOrNull() ?: 0.0
        val t1 = inputs.t2T1.toDoubleOrNull() ?: 0.0
        val z2 = inputs.t2Z2.toDoubleOrNull() ?: 0.0
        val t2 = inputs.t2T2.toDoubleOrNull() ?: 0.0
        val drift = if (t2 != t1) kotlin.math.abs((z2 - z1) / (t2 - t1)) * 5.0 else 0.0
        // PI limit per 5C is typically p_i * e. Let's just say p_i = 0.5, so 0.5*e for Class III
        val tPass = drift <= (if (c == "I") 1.0*e else 0.5*e) // Simple placeholder rule

        val tempEffectResult = com.example.data.TempEffectResult(z1, t1, z2, t2, drift, tPass)

        val eccPos = inputs.t3Readings.map { (pos, readStr) ->
            val r = readStr.toDoubleOrNull() ?: 0.0
            val err = r - inputs.t3Load
            val m = mpe(inputs.t3Load)
            com.example.data.EccentricityPosition(pos, r, err, m, kotlin.math.abs(err) <= m)
        }
        val eccentricityResult = com.example.data.EccentricityResult(inputs.t3Load, eccPos, eccPos.all { it.isPass })

        val bRead = inputs.t4BaseRead.toDoubleOrNull() ?: 0.0
        val nRead = inputs.t4NewRead.toDoubleOrNull() ?: 0.0
        val dPass = (nRead - bRead) >= (0.7 * inputs.t4ExtraLoad) // Simplification
        val discriminationResult = com.example.data.DiscriminationResult(inputs.t4BaseLoad, bRead, inputs.t4ExtraLoad, nRead, dPass)

        val repReads = inputs.t5Readings.mapNotNull { it.toDoubleOrNull() }
        val range = if (repReads.isNotEmpty()) repReads.maxOrNull()!! - repReads.minOrNull()!! else 0.0
        val m = mpe(inputs.t5Load)
        val repeatabilityResult = com.example.data.RepeatabilityResult(inputs.t5Load, repReads, range, m, range <= kotlin.math.abs(m))

        val zB = inputs.t6ZB.toDoubleOrNull() ?: 0.0
        val zA = inputs.t6ZA.toDoubleOrNull() ?: 0.0
        val c0 = inputs.t6C0.toDoubleOrNull() ?: 0.0
        val c5 = inputs.t6C5.toDoubleOrNull() ?: 0.0
        val c15 = inputs.t6C15.toDoubleOrNull() ?: 0.0
        val c30 = inputs.t6C30.toDoubleOrNull() ?: 0.0
        val zPass = kotlin.math.abs(zA - zB) <= 0.5 * e
        val creeps = listOf(c0, c5, c15, c30)
        val maxDrift = if (creeps.isNotEmpty()) creeps.maxOrNull()!! - creeps.minOrNull()!! else 0.0
        val cPass = maxDrift <= mpe(inputs.t6Load)
        val timeDependenceResult = com.example.data.TimeDependenceResult(inputs.t6Load, zB, zA, c0, c5, c15, c30, maxDrift, zPass, cPass, zPass && cPass)

        val stabReads = inputs.t7Readings.mapNotNull { it.toDoubleOrNull() }
        val sSpread = if (stabReads.isNotEmpty()) stabReads.maxOrNull()!! - stabReads.minOrNull()!! else 0.0
        val stabilityResult = com.example.data.StabilityResult(inputs.t7Load, stabReads, sSpread, sSpread <= 0.5 * e)

        val refR = inputs.t8Ref.toDoubleOrNull() ?: 0.0
        val tiltR = inputs.t8Tilt.toDoubleOrNull() ?: 0.0
        val diff = kotlin.math.abs(tiltR - refR)
        val tmpe = mpe(inputs.t8Load)
        val tiltingResult = com.example.data.TiltingResult(inputs.t8Load, refR, tiltR, diff, tmpe, diff <= tmpe)

        val tareW = inputs.t9Tare.toDoubleOrNull() ?: 0.0
        val grossReads = inputs.t9Gross.mapNotNull { it.toDoubleOrNull() }
        val netErrs = inputs.t9Loads.mapIndexed { i, netLoad ->
            val gr = if (i < grossReads.size) grossReads[i] else 0.0
            val nr = gr - tareW
            nr - netLoad
        }
        val tareMpes = inputs.t9Loads.map { mpe(it) }
        val tPassAll = netErrs.mapIndexed { i, err -> kotlin.math.abs(err) <= tareMpes[i] }.all { it }
        val tareResult = com.example.data.TareResult(tareW, inputs.t9Loads, grossReads, netErrs, tareMpes, tPassAll)

        val e0 = inputs.t10E0.toDoubleOrNull() ?: 0.0
        val e5 = inputs.t10E5.toDoubleOrNull() ?: 0.0
        val e15 = inputs.t10E15.toDoubleOrNull() ?: 0.0
        val e30 = inputs.t10E30.toDoubleOrNull() ?: 0.0
        val warmUpResult = com.example.data.WarmUpResult(inputs.t10Load, e0, e5, e15, e30, kotlin.math.abs(e30 - e0) <= mpe(inputs.t10Load)) // simple check

        val vMin = inputs.t11Min.toDoubleOrNull() ?: 0.0
        val vNom = inputs.t11Nom.toDoubleOrNull() ?: 0.0
        val vMax = inputs.t11Max.toDoubleOrNull() ?: 0.0
        val vMpe = mpe(inputs.t11Load)
        val vPass = kotlin.math.abs(vMin - inputs.t11Load) <= vMpe && kotlin.math.abs(vMax - inputs.t11Load) <= vMpe
        val voltageResult = com.example.data.VoltageResult(inputs.t11Load, vMin, vNom, vMax, vPass)

        val emcResult = com.example.data.EmcResult(inputs.t12Dips, inputs.t12Bursts, inputs.t12Surges, inputs.t12Esd, inputs.t12Rad, inputs.t12Cond, inputs.t12Veh, 
            !(inputs.t12Dips || inputs.t12Bursts || inputs.t12Surges || inputs.t12Esd || inputs.t12Rad || inputs.t12Cond || inputs.t12Veh))

        val dInit = inputs.t13Init.toDoubleOrNull() ?: 0.0
        val dHigh = inputs.t13High.toDoubleOrNull() ?: 0.0
        val dFinal = inputs.t13Final.toDoubleOrNull() ?: 0.0
        val dampPass = kotlin.math.abs(dFinal - dInit) <= 0.5 * e
        val dampHeatResult = com.example.data.DampHeatResult(inputs.t13Load, dInit, dHigh, dFinal, dampPass)

        val spanErrs = inputs.t14Errors.mapNotNull { it.toDoubleOrNull() }
        val variation = if (spanErrs.isNotEmpty()) spanErrs.maxOrNull()!! - spanErrs.minOrNull()!! else 0.0
        val spanStabilityResult = com.example.data.SpanStabilityResult(inputs.t14Load, spanErrs, variation, variation <= 0.5 * e)

        val endCyc = inputs.t15Cycles.toIntOrNull() ?: 0
        val endInit = inputs.t15Init.toDoubleOrNull() ?: 0.0
        val endFinal = inputs.t15Final.toDoubleOrNull() ?: 0.0
        val durErr = endFinal - endInit
        val enduranceResult = com.example.data.EnduranceResult(endCyc, endInit, endFinal, inputs.t15Dates, durErr, kotlin.math.abs(durErr) <= e)
        
        updateCurrentReport { 
            it.copy(
                status = if (weighingResults.all { it.isPass } && tempEffectResult.isPass && eccentricityResult.isPass && discriminationResult.isPass && repeatabilityResult.isPass && timeDependenceResult.isPass && stabilityResult.isPass && tiltingResult.isPass && tareResult.isPass && warmUpResult.isPass && voltageResult.isPass && emcResult.isPass && dampHeatResult.isPass && spanStabilityResult.isPass && enduranceResult.isPass) "Pass" else "Fail",
                weighingResults = weighingResults,
                tempEffectResult = tempEffectResult,
                eccentricityResult = eccentricityResult,
                discriminationResult = discriminationResult,
                repeatabilityResult = repeatabilityResult,
                timeDependenceResult = timeDependenceResult,
                stabilityResult = stabilityResult,
                tiltingResult = tiltingResult,
                tareResult = tareResult,
                warmUpResult = warmUpResult,
                voltageResult = voltageResult,
                emcResult = emcResult,
                dampHeatResult = dampHeatResult,
                spanStabilityResult = spanStabilityResult,
                enduranceResult = enduranceResult,
                digitalSignature = inputs.signature,
                photoAttached = inputs.photoAttached
            )
        }
        viewModelScope.launch {
            reportDao.insertReport(_activeReports.value[_currentIndex.value])
        }
    }

}
