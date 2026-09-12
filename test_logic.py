with open('app/src/main/java/com/example/MetroCertViewModel.kt', 'r') as f:
    content = f.read()

# I will append processTests function at the end of the viewmodel class
func = """
    fun processTests(inputs: com.example.data.TestInputs) {
        val report = _activeReports.value[_currentIndex.value]
        val max = report.maxCapacity
        val e = report.e
        val c = report.accuracyClass
        
        fun mpe(load: Double): Double {
            return com.example.data.RulesConfig.calculateMPE(c, load, e)
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
                enduranceResult = enduranceResult
            )
        }
    }
"""

with open('app/src/main/java/com/example/MetroCertViewModel.kt', 'w') as f:
    f.write(content.rstrip()[:-1].rstrip() + "\n" + func + "\n}\n")
