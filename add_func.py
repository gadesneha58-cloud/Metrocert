with open("app/src/main/java/com/example/ui/TestingScreen.kt", "r") as f:
    content = f.read()

autofill_func_end = """        state.t15Cycles.value = "100000"; state.t15Init.value = maxCap.toString(); state.t15Final.value = maxCap.toString(); state.t15Dates.value = "2026-08-01 to 2026-08-15"
    }"""

new_autofill_funcs = """        state.t15Cycles.value = "100000"; state.t15Init.value = maxCap.toString(); state.t15Final.value = maxCap.toString(); state.t15Dates.value = "2026-08-01 to 2026-08-15"
    }

    fun autoFillFailing() {
        t1Loads.forEachIndexed { i, load -> state.t1Up[i] = (load + e * 10).toString(); state.t1Down[i] = (load - e * 10).toString() }
        state.t2Z1.value = "0.0"; state.t2T1.value = "20.0"
        state.t2Z2.value = (e * 20).toString(); state.t2T2.value = "30.0"
        listOf("Center", "Front Left", "Back Left", "Back Right", "Front Right").forEach { state.t3Readings[it] = (t3Load + e * 5).toString() }
        state.t4BaseRead.value = t4BaseLoad.toString()
        state.t4NewRead.value = (t4BaseLoad + t4ExtraLoad + e * 5).toString()
        for (i in 0 until 10) state.t5Readings[i] = (t5Load + e * i).toString()
        state.t6ZB.value = "0.0"; state.t6ZA.value = (e * 10).toString()
        state.t6C0.value = "0.0"; state.t6C5.value = (e * 5).toString(); state.t6C15.value = (e * 10).toString(); state.t6C30.value = (e * 15).toString()
        for (i in 0 until 5) state.t7Readings[i] = (t7Load + e * i).toString()
        state.t8Ref.value = t8Load.toString(); state.t8Tilt.value = (t8Load + e * 10).toString()
        state.t9Tare.value = "1.0"
        t9Loads.forEachIndexed { i, load -> state.t9Gross[i] = (load + 1.0 + e * 5).toString() }
        state.t10E0.value = (e * 5).toString(); state.t10E5.value = (e * 5).toString(); state.t10E15.value = (e * 5).toString(); state.t10E30.value = (e * 5).toString()
        state.t11Min.value = (t11Load + e * 5).toString(); state.t11Nom.value = t11Load.toString(); state.t11Max.value = (t11Load - e * 5).toString()
        state.t13Init.value = t13Load.toString(); state.t13High.value = (t13Load + e * 10).toString(); state.t13Final.value = (t13Load - e * 10).toString()
        for (i in 0 until 5) state.t14Errors[i] = (e * 5).toString()
        state.t15Cycles.value = "100000"; state.t15Init.value = maxCap.toString(); state.t15Final.value = (maxCap - e * 10).toString(); state.t15Dates.value = "2026-08-01 to 2026-08-15"
    }"""

content = content.replace(autofill_func_end, new_autofill_funcs)

with open("app/src/main/java/com/example/ui/TestingScreen.kt", "w") as f:
    f.write(content)
