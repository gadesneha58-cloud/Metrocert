package com.example.data

import androidx.room.TypeConverter
import com.squareup.moshi.Moshi
import com.squareup.moshi.Types
import com.squareup.moshi.kotlin.reflect.KotlinJsonAdapterFactory

class Converters {
    private val moshi = Moshi.Builder()
        .add(KotlinJsonAdapterFactory())
        .build()

    private val weighingResultListType = Types.newParameterizedType(List::class.java, WeighingResult::class.java)
    private val weighingResultAdapter = moshi.adapter<List<WeighingResult>>(weighingResultListType)
    @TypeConverter fun fromWeighingResultList(value: List<WeighingResult>?): String = value?.let { weighingResultAdapter.toJson(it) } ?: "[]"
    @TypeConverter fun toWeighingResultList(value: String): List<WeighingResult> = weighingResultAdapter.fromJson(value) ?: emptyList()

    private val tempEffectAdapter = moshi.adapter(TempEffectResult::class.java)
    @TypeConverter fun fromTempEffectResult(value: TempEffectResult?): String? = value?.let { tempEffectAdapter.toJson(it) }
    @TypeConverter fun toTempEffectResult(value: String?): TempEffectResult? = value?.let { tempEffectAdapter.fromJson(it) }

    private val eccentricityResultAdapter = moshi.adapter(EccentricityResult::class.java)
    @TypeConverter fun fromEccentricityResult(value: EccentricityResult?): String? = value?.let { eccentricityResultAdapter.toJson(it) }
    @TypeConverter fun toEccentricityResult(value: String?): EccentricityResult? = value?.let { eccentricityResultAdapter.fromJson(it) }

    private val discriminationAdapter = moshi.adapter(DiscriminationResult::class.java)
    @TypeConverter fun fromDiscriminationResult(value: DiscriminationResult?): String? = value?.let { discriminationAdapter.toJson(it) }
    @TypeConverter fun toDiscriminationResult(value: String?): DiscriminationResult? = value?.let { discriminationAdapter.fromJson(it) }

    private val repeatabilityAdapter = moshi.adapter(RepeatabilityResult::class.java)
    @TypeConverter fun fromRepeatabilityResult(value: RepeatabilityResult?): String? = value?.let { repeatabilityAdapter.toJson(it) }
    @TypeConverter fun toRepeatabilityResult(value: String?): RepeatabilityResult? = value?.let { repeatabilityAdapter.fromJson(it) }

    private val timeDepAdapter = moshi.adapter(TimeDependenceResult::class.java)
    @TypeConverter fun fromTimeDependenceResult(value: TimeDependenceResult?): String? = value?.let { timeDepAdapter.toJson(it) }
    @TypeConverter fun toTimeDependenceResult(value: String?): TimeDependenceResult? = value?.let { timeDepAdapter.fromJson(it) }

    private val stabilityAdapter = moshi.adapter(StabilityResult::class.java)
    @TypeConverter fun fromStabilityResult(value: StabilityResult?): String? = value?.let { stabilityAdapter.toJson(it) }
    @TypeConverter fun toStabilityResult(value: String?): StabilityResult? = value?.let { stabilityAdapter.fromJson(it) }

    private val tiltingAdapter = moshi.adapter(TiltingResult::class.java)
    @TypeConverter fun fromTiltingResult(value: TiltingResult?): String? = value?.let { tiltingAdapter.toJson(it) }
    @TypeConverter fun toTiltingResult(value: String?): TiltingResult? = value?.let { tiltingAdapter.fromJson(it) }

    private val tareAdapter = moshi.adapter(TareResult::class.java)
    @TypeConverter fun fromTareResult(value: TareResult?): String? = value?.let { tareAdapter.toJson(it) }
    @TypeConverter fun toTareResult(value: String?): TareResult? = value?.let { tareAdapter.fromJson(it) }

    private val warmUpAdapter = moshi.adapter(WarmUpResult::class.java)
    @TypeConverter fun fromWarmUpResult(value: WarmUpResult?): String? = value?.let { warmUpAdapter.toJson(it) }
    @TypeConverter fun toWarmUpResult(value: String?): WarmUpResult? = value?.let { warmUpAdapter.fromJson(it) }

    private val voltageAdapter = moshi.adapter(VoltageResult::class.java)
    @TypeConverter fun fromVoltageResult(value: VoltageResult?): String? = value?.let { voltageAdapter.toJson(it) }
    @TypeConverter fun toVoltageResult(value: String?): VoltageResult? = value?.let { voltageAdapter.fromJson(it) }

    private val emcAdapter = moshi.adapter(EmcResult::class.java)
    @TypeConverter fun fromEmcResult(value: EmcResult?): String? = value?.let { emcAdapter.toJson(it) }
    @TypeConverter fun toEmcResult(value: String?): EmcResult? = value?.let { emcAdapter.fromJson(it) }

    private val dampHeatAdapter = moshi.adapter(DampHeatResult::class.java)
    @TypeConverter fun fromDampHeatResult(value: DampHeatResult?): String? = value?.let { dampHeatAdapter.toJson(it) }
    @TypeConverter fun toDampHeatResult(value: String?): DampHeatResult? = value?.let { dampHeatAdapter.fromJson(it) }

    private val spanStabilityAdapter = moshi.adapter(SpanStabilityResult::class.java)
    @TypeConverter fun fromSpanStabilityResult(value: SpanStabilityResult?): String? = value?.let { spanStabilityAdapter.toJson(it) }
    @TypeConverter fun toSpanStabilityResult(value: String?): SpanStabilityResult? = value?.let { spanStabilityAdapter.fromJson(it) }

    private val enduranceAdapter = moshi.adapter(EnduranceResult::class.java)
    @TypeConverter fun fromEnduranceResult(value: EnduranceResult?): String? = value?.let { enduranceAdapter.toJson(it) }
    @TypeConverter fun toEnduranceResult(value: String?): EnduranceResult? = value?.let { enduranceAdapter.fromJson(it) }
}
