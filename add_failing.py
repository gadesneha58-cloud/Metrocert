with open("app/src/main/java/com/example/ui/TestingState.kt", "r") as f:
    content = f.read()

failing_data_func = """    fun autoFillFailingData(
        t1Loads: List<Double>,
        t3Load: Double,
        t4BaseLoad: Double,
        t4ExtraLoad: Double,
        e: Double,
        t5Load: Double,
        t6Load: Double,
        t7Load: Double,
        t8Load: Double,
        t9Loads: List<Double>,
        t10Load: Double,
        t11Load: Double,
        t13Load: Double,
        maxCap: Double
    ) {
        t1Loads.forEachIndexed { i, load ->
            if (i < t1Up.size) t1Up[i] = (load + e * 10).toString()
            if (i < t1Down.size) t1Down[i] = (load - e * 10).toString()
        }
        t2Z1.value = "0.0"; t2T1.value = "20.0"
        t2Z2.value = (e * 20).toString(); t2T2.value = "30.0"
        listOf("Center", "Front Left", "Back Left", "Back Right", "Front Right").forEach {
            t3Readings[it] = (t3Load + e * 5).toString()
        }
        t4BaseRead.value = t4BaseLoad.toString()
        t4NewRead.value = (t4BaseLoad + t4ExtraLoad + e * 5).toString()
        for (i in 0 until t5Readings.size) t5Readings[i] = (t5Load + e * i).toString()
        t6ZB.value = "0.0"; t6ZA.value = (e * 10).toString()
        t6C0.value = "0.0"; t6C5.value = (e * 5).toString(); t6C15.value = (e * 10).toString(); t6C30.value = (e * 15).toString()
        for (i in 0 until t7Readings.size) t7Readings[i] = (t7Load + e * i).toString()
        t8Ref.value = t8Load.toString(); t8Tilt.value = (t8Load + e * 10).toString()
        t9Tare.value = "1.0"
        t9Loads.forEachIndexed { i, load ->
            if (i < t9Gross.size) t9Gross[i] = (load + 1.0 + e * 5).toString()
        }
        t10E0.value = (e * 5).toString(); t10E5.value = (e * 5).toString(); t10E15.value = (e * 5).toString(); t10E30.value = (e * 5).toString()
        t11Min.value = (t11Load + e * 5).toString(); t11Nom.value = t11Load.toString(); t11Max.value = (t11Load - e * 5).toString()
        t12Dips.value = false; t12Bursts.value = false; t12Surges.value = false
        t12Esd.value = false; t12Rad.value = false; t12Cond.value = false; t12Veh.value = false
        t13Init.value = t13Load.toString(); t13High.value = (t13Load + e * 10).toString(); t13Final.value = (t13Load - e * 10).toString()
        for (i in 0 until t14Errors.size) t14Errors[i] = (e * 5).toString()
        t15Cycles.value = "100000"
        t15Init.value = maxCap.toString()
        t15Final.value = (maxCap - e * 10).toString()
        t15Dates.value = "2026-08-01 to 2026-08-15"
    }
"""

if "fun autoFillFailingData(" not in content:
    content = content.replace("fun toTestInputs(", failing_data_func + "\n    fun toTestInputs(")
    with open("app/src/main/java/com/example/ui/TestingState.kt", "w") as f:
        f.write(content)
