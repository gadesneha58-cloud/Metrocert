package com.example.data

import androidx.room.Entity
import androidx.room.PrimaryKey
import com.squareup.moshi.JsonClass
import java.util.UUID

@Entity(tableName = "reports")
@JsonClass(generateAdapter = true)
data class Report(
    @PrimaryKey var id: String = UUID.randomUUID().toString(),
    val certificateNo: String = "",
    val date: Long = System.currentTimeMillis(),
    val manufacturer: String = "",
    val modelNumber: String = "",
    val serialNumber: String = "",
    val accuracyClass: String = "III",
    val isInService: Boolean = false,
    val maxCapacity: Double = 0.0,
    val e: Double = 0.0,
    val minCapacity: Double = 0.0,
    val n: Double = 0.0,
    val ambientTemp: Double = 20.0,
    val relativeHumidity: Double = 50.0,
    val atmosphericPressure: Double = 1013.25,
    val standardWeightId: String = "",
    val digitalSignature: String = "",
    val photoAttached: Boolean = false,
    
    val status: String = "Pending", // Pass, Fail, Pending
    
    val weighingResults: List<WeighingResult> = emptyList(),
    val tempEffectResult: TempEffectResult? = null,
    val eccentricityResult: EccentricityResult? = null,
    val discriminationResult: DiscriminationResult? = null,
    val repeatabilityResult: RepeatabilityResult? = null,
    val timeDependenceResult: TimeDependenceResult? = null,
    val stabilityResult: StabilityResult? = null,
    val tiltingResult: TiltingResult? = null,
    val tareResult: TareResult? = null,
    val warmUpResult: WarmUpResult? = null,
    val voltageResult: VoltageResult? = null,
    val emcResult: EmcResult? = null,
    val dampHeatResult: DampHeatResult? = null,
    val spanStabilityResult: SpanStabilityResult? = null,
    val enduranceResult: EnduranceResult? = null
)

@JsonClass(generateAdapter = true)
data class WeighingResult(val load: Double = 0.0, val indUp: Double = 0.0, val indDown: Double = 0.0, val errUp: Double = 0.0, val errDown: Double = 0.0, val mpe: Double = 0.0, val isPass: Boolean = false)

@JsonClass(generateAdapter = true)
data class TempEffectResult(val zero1: Double, val temp1: Double, val zero2: Double, val temp2: Double, val driftPer5C: Double, val isPass: Boolean)

@JsonClass(generateAdapter = true)
data class EccentricityResult(val referenceWeight: Double = 0.0, val positions: List<EccentricityPosition> = emptyList(), val isPass: Boolean = false)

@JsonClass(generateAdapter = true)
data class EccentricityPosition(val positionName: String = "", val indication: Double = 0.0, val error: Double = 0.0, val mpe: Double = 0.0, val isPass: Boolean = false)

@JsonClass(generateAdapter = true)
data class DiscriminationResult(val baseLoad: Double, val baseReading: Double, val extraLoad: Double, val newReading: Double, val isPass: Boolean)

@JsonClass(generateAdapter = true)
data class RepeatabilityResult(val referenceWeight: Double = 0.0, val readings: List<Double> = emptyList(), val range: Double = 0.0, val mpe: Double = 0.0, val isPass: Boolean = false)

@JsonClass(generateAdapter = true)
data class TimeDependenceResult(val load: Double, val zeroBefore: Double, val zeroAfter30: Double, val creep0: Double, val creep5: Double, val creep15: Double, val creep30: Double, val maxDrift: Double, val zeroReturnPass: Boolean, val creepPass: Boolean, val isPass: Boolean)

@JsonClass(generateAdapter = true)
data class StabilityResult(val load: Double, val readings: List<Double>, val spread: Double, val isPass: Boolean)

@JsonClass(generateAdapter = true)
data class TiltingResult(val load: Double, val refReading: Double, val tiltReading: Double, val diff: Double, val mpe: Double, val isPass: Boolean)

@JsonClass(generateAdapter = true)
data class TareResult(val tareWeight: Double, val netLoads: List<Double>, val grossReadings: List<Double>, val netErrors: List<Double>, val mpes: List<Double>, val isPass: Boolean)

@JsonClass(generateAdapter = true)
data class WarmUpResult(val load: Double, val err0: Double, val err5: Double, val err15: Double, val err30: Double, val isPass: Boolean)

@JsonClass(generateAdapter = true)
data class VoltageResult(val load: Double, val minReading: Double, val nomReading: Double, val maxReading: Double, val isPass: Boolean)

@JsonClass(generateAdapter = true)
data class EmcResult(val dipsFault: Boolean, val burstsFault: Boolean, val surgesFault: Boolean, val esdFault: Boolean, val radiatedFault: Boolean, val conductedFault: Boolean, val vehicleFault: Boolean, val isPass: Boolean)

@JsonClass(generateAdapter = true)
data class DampHeatResult(val load: Double, val initialReading: Double, val highTempReading: Double, val finalReading: Double, val isPass: Boolean)

@JsonClass(generateAdapter = true)
data class SpanStabilityResult(val load: Double, val sessionErrors: List<Double>, val variation: Double, val isPass: Boolean)

@JsonClass(generateAdapter = true)
data class EnduranceResult(val cycleCount: Int, val initialReading: Double, val finalReading: Double, val dateRange: String, val durabilityError: Double, val isPass: Boolean)
