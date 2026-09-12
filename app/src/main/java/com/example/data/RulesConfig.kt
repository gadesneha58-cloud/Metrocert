package com.example.data

data class NRange(val min: Double, val max: Double)
data class MpeTier(val uptoE: Double, val mpeMultiplier: Double)
data class ClassRules(val className: String, val nRange: NRange, val mpeTiers: List<MpeTier>)

object RulesConfig {
    // This mocks what would normally be fetched from Firestore
    val rules = mapOf(
        "I" to ClassRules("I", NRange(50000.0, Double.MAX_VALUE), listOf(
            MpeTier(50000.0, 0.5), MpeTier(200000.0, 1.0), MpeTier(Double.MAX_VALUE, 1.5)
        )),
        "II" to ClassRules("II", NRange(100.0, 100000.0), listOf(
            MpeTier(5000.0, 0.5), MpeTier(20000.0, 1.0), MpeTier(Double.MAX_VALUE, 1.5)
        )),
        "III" to ClassRules("III", NRange(100.0, 10000.0), listOf(
            MpeTier(500.0, 0.5), MpeTier(2000.0, 1.0), MpeTier(Double.MAX_VALUE, 1.5)
        )),
        "IIII" to ClassRules("IIII", NRange(100.0, 1000.0), listOf(
            MpeTier(50.0, 0.5), MpeTier(200.0, 1.0), MpeTier(Double.MAX_VALUE, 1.5)
        ))
    )

    fun validateN(className: String, n: Double): Boolean {
        val range = rules[className]?.nRange ?: return false
        return n >= range.min && n <= range.max
    }

    fun getMpe(loadInE: Double, className: String, scaleInterval: Double, isInService: Boolean = false): Double {
        val classRules = rules[className] ?: return 0.0
        val tier = classRules.mpeTiers.find { loadInE <= it.uptoE } ?: classRules.mpeTiers.last()
        val multiplier = if (isInService) 2.0 else 1.0
        return tier.mpeMultiplier * scaleInterval * multiplier
    }
}
