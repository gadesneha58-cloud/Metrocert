cat << 'INNER_EOF' > app/src/main/java/com/example/data/Report.kt
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
    val maxCapacity: Double = 0.0,
    val e: Double = 0.0,
    val minCapacity: Double = 0.0,
    val n: Double = 0.0,
    val ambientTemp: Double = 20.0,
    val relativeHumidity: Double = 50.0,
    val atmosphericPressure: Double = 1013.25,
    val standardWeightId: String = "",
    
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
INNER_EOF

cat << 'INNER_EOF' > app/src/main/java/com/example/data/TestInputs.kt
package com.example.data

data class TestInputs(
    val t1Loads: List<Double>, val t1Up: List<String>, val t1Down: List<String>,
    val t2Z1: String, val t2T1: String, val t2Z2: String, val t2T2: String,
    val t3Load: Double, val t3Readings: Map<String, String>,
    val t4BaseLoad: Double, val t4BaseRead: String, val t4ExtraLoad: Double, val t4NewRead: String,
    val t5Load: Double, val t5Readings: List<String>,
    val t6Load: Double, val t6ZB: String, val t6ZA: String, val t6C0: String, val t6C5: String, val t6C15: String, val t6C30: String,
    val t7Load: Double, val t7Readings: List<String>,
    val t8Load: Double, val t8Ref: String, val t8Tilt: String,
    val t9Tare: String, val t9Loads: List<Double>, val t9Gross: List<String>,
    val t10Load: Double, val t10E0: String, val t10E5: String, val t10E15: String, val t10E30: String,
    val t11Load: Double, val t11Min: String, val t11Nom: String, val t11Max: String,
    val t12Dips: Boolean, val t12Bursts: Boolean, val t12Surges: Boolean, val t12Esd: Boolean, val t12Rad: Boolean, val t12Cond: Boolean, val t12Veh: Boolean,
    val t13Load: Double, val t13Init: String, val t13High: String, val t13Final: String,
    val t14Load: Double, val t14Errors: List<String>,
    val t15Cycles: String, val t15Init: String, val t15Final: String, val t15Dates: String
)
INNER_EOF

sed -i 's/version = 2/version = 3/g' app/src/main/java/com/example/data/AppDatabase.kt
