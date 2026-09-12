with open("app/src/main/java/com/example/data/RulesConfig.kt", "r") as f:
    content = f.read()

old_get_mpe = """    fun getMpe(loadInE: Double, className: String, scaleInterval: Double): Double {
        val classRules = rules[className] ?: return 0.0
        // Find the first tier where loadInE is <= uptoE, else fallback to the highest tier (last one)
        val tier = classRules.mpeTiers.find { loadInE <= it.uptoE } ?: classRules.mpeTiers.last()
        return tier.mpeMultiplier * scaleInterval
    }"""

new_get_mpe = """    fun getMpe(loadInE: Double, className: String, scaleInterval: Double, isInService: Boolean = false): Double {
        val classRules = rules[className] ?: return 0.0
        val tier = classRules.mpeTiers.find { loadInE <= it.uptoE } ?: classRules.mpeTiers.last()
        val multiplier = if (isInService) 2.0 else 1.0
        return tier.mpeMultiplier * scaleInterval * multiplier
    }"""

if old_get_mpe in content:
    content = content.replace(old_get_mpe, new_get_mpe)
    with open("app/src/main/java/com/example/data/RulesConfig.kt", "w") as f:
        f.write(content)
else:
    print("Could not find getMpe to replace")
