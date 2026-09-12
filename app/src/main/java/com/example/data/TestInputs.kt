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
    val t15Cycles: String, val t15Init: String, val t15Final: String, val t15Dates: String,
    val signature: String, val photoAttached: Boolean
)
