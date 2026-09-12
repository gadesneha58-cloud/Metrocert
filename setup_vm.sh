cat << 'INNER_EOF' > app/src/main/java/com/example/MetroCertViewModel.kt
package com.example

import android.app.Application
import androidx.lifecycle.AndroidViewModel
import androidx.lifecycle.viewModelScope
import com.example.data.*
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.SharingStarted
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.first
import kotlinx.coroutines.flow.stateIn
import kotlinx.coroutines.flow.update
import kotlinx.coroutines.launch
import kotlin.math.abs

class MetroCertViewModel(application: Application) : AndroidViewModel(application) {
    private val reportDao = AppDatabase.getDatabase(application).reportDao()
    val savedReports: StateFlow<List<Report>> = reportDao.getAllReports()
        .stateIn(viewModelScope, SharingStarted.Lazily, emptyList())

    init {
        viewModelScope.launch {
            reportDao.getAllReports().first().let { currentReports ->
                if (currentReports.isEmpty()) {
                    val demoReports = listOf(
                        Report(certificateNo = "CERT-2026-A01", manufacturer = "Mettler Toledo", modelNumber = "MS204S", status = "Pass", date = System.currentTimeMillis() - 86400000L),
                        Report(certificateNo = "CERT-2026-A02", manufacturer = "Sartorius", modelNumber = "Quintix", status = "Fail", date = System.currentTimeMillis() - (86400000L * 3)),
                        Report(certificateNo = "CERT-2026-B99", manufacturer = "Ohaus", modelNumber = "Adventurer", status = "Pass", date = System.currentTimeMillis() - (86400000L * 7))
                    )
                    demoReports.forEach { reportDao.insertReport(it) }
                }
            }
        }
    }

    private val _currentReport = MutableStateFlow(Report())
    val currentReport = _currentReport.asStateFlow()

    fun startNewInspection() {
        _currentReport.value = Report()
    }

    fun updateInstrumentDetails(manufacturer: String, model: String, serial: String, certNo: String, accuracyClass: String, maxCapacity: Double, e: Double) {
        val minCapacity = 20 * e
        val n = if (e > 0) maxCapacity / e else 0.0
        _currentReport.update {
            it.copy(manufacturer = manufacturer, modelNumber = model, serialNumber = serial, certificateNo = certNo, accuracyClass = accuracyClass, maxCapacity = maxCapacity, e = e, minCapacity = minCapacity, n = n)
        }
    }

    fun updateEnvironmentalConditions(temp: Double, humidity: Double, pressure: Double, standardId: String) {
        _currentReport.update {
            it.copy(ambientTemp = temp, relativeHumidity = humidity, atmosphericPressure = pressure, standardWeightId = standardId)
        }
    }

    fun processTests(inputs: TestInputs) {
        val report = _currentReport.value
        val e = report.e
        val className = report.accuracyClass

        fun mpe(load: Double): Double = RulesConfig.getMpe(if (e > 0) load / e else 0.0, className, e)
        fun parse(s: String) = s.toDoubleOrNull() ?: 0.0

        // T1
        val wResults = inputs.t1Loads.mapIndexed { i, load ->
            val indUp = parse(inputs.t1Up[i])
            val indDown = parse(inputs.t1Down[i])
            val errUp = indUp - load
            val errDown = indDown - load
            val m = mpe(load)
            WeighingResult(load, indUp, indDown, errUp, errDown, m, abs(errUp) <= m && abs(errDown) <= m)
        }
        val t1Pass = wResults.all { it.isPass }

        // T2
        val z1 = parse(inputs.t2Z1); val t1 = parse(inputs.t2T1)
        val z2 = parse(inputs.t2Z2); val t2 = parse(inputs.t2T2)
        val drift = z2 - z1
        val tempDiff = t2 - t1
        val driftPer5 = if (tempDiff != 0.0) (drift / tempDiff) * 5.0 else 0.0
        val t2Pass = abs(driftPer5) <= e
        val r2 = TempEffectResult(z1, t1, z2, t2, driftPer5, t2Pass)

        // T3
        val eccMpe = mpe(inputs.t3Load)
        val eccPos = inputs.t3Readings.map { (k, v) ->
            val ind = parse(v)
            val err = ind - inputs.t3Load
            EccentricityPosition(k, ind, err, eccMpe, abs(err) <= eccMpe)
        }
        val r3 = EccentricityResult(inputs.t3Load, eccPos, eccPos.all { it.isPass })

        // T4
        val bLoad = inputs.t4BaseLoad; val bRead = parse(inputs.t4BaseRead)
        val eLoad = inputs.t4ExtraLoad; val nRead = parse(inputs.t4NewRead)
        val t4Pass = (nRead - bRead) >= e
        val r4 = DiscriminationResult(bLoad, bRead, eLoad, nRead, t4Pass)

        // T5
        val t5R = inputs.t5Readings.map { parse(it) }
        val spread = (t5R.maxOrNull() ?: 0.0) - (t5R.minOrNull() ?: 0.0)
        val r5Mpe = mpe(inputs.t5Load)
        val r5 = RepeatabilityResult(inputs.t5Load, t5R, spread, r5Mpe, spread <= r5Mpe)

        // T6
        val zb = parse(inputs.t6ZB); val za = parse(inputs.t6ZA)
        val c0 = parse(inputs.t6C0); val c5 = parse(inputs.t6C5)
        val c15 = parse(inputs.t6C15); val c30 = parse(inputs.t6C30)
        val zeroReturnPass = abs(za - zb) <= 0.5 * e
        val drifts = listOf(c5 - c0, c15 - c0, c30 - c0).map { abs(it) }
        val maxDrift = drifts.maxOrNull() ?: 0.0
        val creepPass = maxDrift <= 0.5 * e
        val r6 = TimeDependenceResult(inputs.t6Load, zb, za, c0, c5, c15, c30, maxDrift, zeroReturnPass, creepPass, zeroReturnPass && creepPass)

        // T7
        val t7R = inputs.t7Readings.map { parse(it) }
        val t7Spread = (t7R.maxOrNull() ?: 0.0) - (t7R.minOrNull() ?: 0.0)
        val r7 = StabilityResult(inputs.t7Load, t7R, t7Spread, t7Spread <= e)

        // T8
        val t8Ref = parse(inputs.t8Ref); val t8Tilt = parse(inputs.t8Tilt)
        val t8RefErr = t8Ref - inputs.t8Load
        val t8TiltErr = t8Tilt - inputs.t8Load
        val t8Diff = abs(t8RefErr - t8TiltErr)
        val t8Mpe = mpe(inputs.t8Load)
        val r8 = TiltingResult(inputs.t8Load, t8Ref, t8Tilt, t8Diff, t8Mpe, t8Diff <= t8Mpe)

        // T9
        val tare = parse(inputs.t9Tare)
        val t9NetErrors = mutableListOf<Double>()
        val t9Mpes = mutableListOf<Double>()
        var t9Pass = true
        val t9GrossR = inputs.t9Gross.mapIndexed { i, gStr ->
            val gross = parse(gStr)
            val net = gross - tare
            val netLoad = inputs.t9Loads[i]
            val err = net - netLoad
            val currMpe = mpe(netLoad)
            t9NetErrors.add(err)
            t9Mpes.add(currMpe)
            if (abs(err) > currMpe) t9Pass = false
            gross
        }
        val r9 = TareResult(tare, inputs.t9Loads, t9GrossR, t9NetErrors, t9Mpes, t9Pass)

        // T10
        val e0 = parse(inputs.t10E0); val e5 = parse(inputs.t10E5); val e15 = parse(inputs.t10E15); val e30 = parse(inputs.t10E30)
        val t10Mpe = mpe(inputs.t10Load)
        val r10 = WarmUpResult(inputs.t10Load, e0, e5, e15, e30, listOf(e0, e5, e15, e30).all { abs(it) <= t10Mpe })

        // T11
        val vMin = parse(inputs.t11Min); val vNom = parse(inputs.t11Nom); val vMax = parse(inputs.t11Max)
        val vMpe = mpe(inputs.t11Load)
        val r11 = VoltageResult(inputs.t11Load, vMin, vNom, vMax, listOf(vMin, vNom, vMax).all { abs(it - inputs.t11Load) <= vMpe })

        // T12
        val r12 = EmcResult(inputs.t12Dips, inputs.t12Bursts, inputs.t12Surges, inputs.t12Esd, inputs.t12Rad, inputs.t12Cond, inputs.t12Veh, !(inputs.t12Dips || inputs.t12Bursts || inputs.t12Surges || inputs.t12Esd || inputs.t12Rad || inputs.t12Cond || inputs.t12Veh))

        // T13
        val dInit = parse(inputs.t13Init); val dHigh = parse(inputs.t13High); val dFinal = parse(inputs.t13Final)
        val dMpe = mpe(inputs.t13Load)
        val r13 = DampHeatResult(inputs.t13Load, dInit, dHigh, dFinal, listOf(dInit, dHigh, dFinal).all { abs(it - inputs.t13Load) <= dMpe })

        // T14
        val sErrs = inputs.t14Errors.map { parse(it) }
        val sVar = (sErrs.maxOrNull() ?: 0.0) - (sErrs.minOrNull() ?: 0.0)
        val r14 = SpanStabilityResult(inputs.t14Load, sErrs, sVar, sVar <= 1.5 * e)

        // T15
        val cyc = inputs.t15Cycles.toIntOrNull() ?: 0
        val endInit = parse(inputs.t15Init); val endFin = parse(inputs.t15Final)
        val durErr = abs(endFin - endInit)
        val endMpe = mpe(report.maxCapacity)
        val r15 = EnduranceResult(cyc, endInit, endFin, inputs.t15Dates, durErr, durErr <= endMpe)

        val finalReport = report.copy(
            weighingResults = wResults, tempEffectResult = r2, eccentricityResult = r3,
            discriminationResult = r4, repeatabilityResult = r5, timeDependenceResult = r6,
            stabilityResult = r7, tiltingResult = r8, tareResult = r9, warmUpResult = r10,
            voltageResult = r11, emcResult = r12, dampHeatResult = r13, spanStabilityResult = r14,
            enduranceResult = r15
        )
        
        val overall = if (t1Pass && r2.isPass && r3.isPass && r4.isPass && r5.isPass && r6.isPass && r7.isPass && r8.isPass && r9.isPass && r10.isPass && r11.isPass && r12.isPass && r13.isPass && r14.isPass && r15.isPass) "Pass" else "Fail"

        val finalized = finalReport.copy(status = overall, date = System.currentTimeMillis())
        _currentReport.value = finalized
        
        viewModelScope.launch {
            reportDao.insertReport(finalized)
        }
    }
}
INNER_EOF
chmod +x setup_vm.sh
./setup_vm.sh