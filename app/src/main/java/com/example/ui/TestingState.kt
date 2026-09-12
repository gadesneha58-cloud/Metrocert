package com.example.ui

import androidx.compose.runtime.mutableStateListOf
import androidx.compose.runtime.mutableStateMapOf
import androidx.compose.runtime.mutableStateOf
import com.example.data.TestInputs

class TestingState {
    val t1Up = mutableStateListOf("", "", "", "", "")
    val t1Down = mutableStateListOf("", "", "", "", "")
    
    var t2Z1 = mutableStateOf("")
    var t2T1 = mutableStateOf("")
    var t2Z2 = mutableStateOf("")
    var t2T2 = mutableStateOf("")
    
    val t3Readings = mutableStateMapOf("Center" to "", "Front Left" to "", "Back Left" to "", "Back Right" to "", "Front Right" to "")
    
    var t4BaseRead = mutableStateOf("")
    var t4NewRead = mutableStateOf("")
    
    val t5Readings = mutableStateListOf("", "", "", "", "", "", "", "", "", "")
    
    var t6ZB = mutableStateOf("")
    var t6ZA = mutableStateOf("")
    var t6C0 = mutableStateOf("")
    var t6C5 = mutableStateOf("")
    var t6C15 = mutableStateOf("")
    var t6C30 = mutableStateOf("")
    
    val t7Readings = mutableStateListOf("", "", "", "", "")
    
    var t8Ref = mutableStateOf("")
    var t8Tilt = mutableStateOf("")
    
    var t9Tare = mutableStateOf("")
    val t9Gross = mutableStateListOf("", "", "")
    
    var t10E0 = mutableStateOf("")
    var t10E5 = mutableStateOf("")
    var t10E15 = mutableStateOf("")
    var t10E30 = mutableStateOf("")
    
    var t11Min = mutableStateOf("")
    var t11Nom = mutableStateOf("")
    var t11Max = mutableStateOf("")
    
    var t12Dips = mutableStateOf(false)
    var t12Bursts = mutableStateOf(false)
    var t12Surges = mutableStateOf(false)
    var t12Esd = mutableStateOf(false)
    var t12Rad = mutableStateOf(false)
    var t12Cond = mutableStateOf(false)
    var t12Veh = mutableStateOf(false)
    
    var t13Init = mutableStateOf("")
    var t13High = mutableStateOf("")
    var t13Final = mutableStateOf("")
    
    val t14Errors = mutableStateListOf("", "", "", "", "")
    
    var t15Cycles = mutableStateOf("")
    var t15Init = mutableStateOf("")
    var t15Final = mutableStateOf("")
    var t15Dates = mutableStateOf("")

    var signature = mutableStateOf("")
    var photoAttached = mutableStateOf(false)

    fun autoFillPassingData(
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
            if (i < t1Up.size) t1Up[i] = load.toString()
            if (i < t1Down.size) t1Down[i] = load.toString()
        }
        t2Z1.value = "0.0"; t2T1.value = "20.0"
        t2Z2.value = "0.0"; t2T2.value = "30.0"
        listOf("Center", "Front Left", "Back Left", "Back Right", "Front Right").forEach {
            t3Readings[it] = t3Load.toString()
        }
        t4BaseRead.value = t4BaseLoad.toString()
        t4NewRead.value = (t4BaseLoad + t4ExtraLoad + e).toString()
        for (i in 0 until t5Readings.size) t5Readings[i] = t5Load.toString()
        t6ZB.value = "0.0"; t6ZA.value = "0.0"
        t6C0.value = "0.0"; t6C5.value = "0.0"; t6C15.value = "0.0"; t6C30.value = "0.0"
        for (i in 0 until t7Readings.size) t7Readings[i] = t7Load.toString()
        t8Ref.value = t8Load.toString(); t8Tilt.value = t8Load.toString()
        t9Tare.value = "1.0"
        t9Loads.forEachIndexed { i, load ->
            if (i < t9Gross.size) t9Gross[i] = (load + 1.0).toString()
        }
        t10E0.value = "0.0"; t10E5.value = "0.0"; t10E15.value = "0.0"; t10E30.value = "0.0"
        t11Min.value = t11Load.toString(); t11Nom.value = t11Load.toString(); t11Max.value = t11Load.toString()
        t12Dips.value = false; t12Bursts.value = false; t12Surges.value = false
        t12Esd.value = false; t12Rad.value = false; t12Cond.value = false; t12Veh.value = false
        t13Init.value = t13Load.toString(); t13High.value = t13Load.toString(); t13Final.value = t13Load.toString()
        for (i in 0 until t14Errors.size) t14Errors[i] = "0.0"
        t15Cycles.value = "100000"
        t15Init.value = maxCap.toString()
        t15Final.value = maxCap.toString()
        t15Dates.value = "2026-08-01 to 2026-08-15"
    }

        fun autoFillFailingData(
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

    fun toTestInputs(
        t1Loads: List<Double>, t3Load: Double, t4BaseLoad: Double, t4ExtraLoad: Double,
        t5Load: Double, t6Load: Double, t7Load: Double, t8Load: Double,
        t9Loads: List<Double>, t10Load: Double, t11Load: Double, t13Load: Double, t14Load: Double
    ): TestInputs {
        return TestInputs(
            t1Loads, t1Up.toList(), t1Down.toList(),
            t2Z1.value, t2T1.value, t2Z2.value, t2T2.value,
            t3Load, t3Readings.toMap(),
            t4BaseLoad, t4BaseRead.value, t4ExtraLoad, t4NewRead.value,
            t5Load, t5Readings.toList(),
            t6Load, t6ZB.value, t6ZA.value, t6C0.value, t6C5.value, t6C15.value, t6C30.value,
            t7Load, t7Readings.toList(),
            t8Load, t8Ref.value, t8Tilt.value,
            t9Tare.value, t9Loads, t9Gross.toList(),
            t10Load, t10E0.value, t10E5.value, t10E15.value, t10E30.value,
            t11Load, t11Min.value, t11Nom.value, t11Max.value,
            t12Dips.value, t12Bursts.value, t12Surges.value, t12Esd.value, t12Rad.value, t12Cond.value, t12Veh.value,
            t13Load, t13Init.value, t13High.value, t13Final.value,
            t14Load, t14Errors.toList(),
            t15Cycles.value, t15Init.value, t15Final.value, t15Dates.value,
            signature.value, photoAttached.value
        )
    }
fun toMap(): Map<String, Any> {
    return mapOf(
        "t1Up" to t1Up.toList(),
        "t1Down" to t1Down.toList(),
        "t2Z1" to t2Z1.value,
        "t2T1" to t2T1.value,
        "t2Z2" to t2Z2.value,
        "t2T2" to t2T2.value,
        "t3Readings" to t3Readings.toMap(),
        "t4BaseRead" to t4BaseRead.value,
        "t4NewRead" to t4NewRead.value,
        "t5Readings" to t5Readings.toList(),
        "t6ZB" to t6ZB.value,
        "t6ZA" to t6ZA.value,
        "t6C0" to t6C0.value,
        "t6C5" to t6C5.value,
        "t6C15" to t6C15.value,
        "t6C30" to t6C30.value,
        "t7Readings" to t7Readings.toList(),
        "t8Ref" to t8Ref.value,
        "t8Tilt" to t8Tilt.value,
        "t9Tare" to t9Tare.value,
        "t9Gross" to t9Gross.toList(),
        "t10E0" to t10E0.value,
        "t10E5" to t10E5.value,
        "t10E15" to t10E15.value,
        "t10E30" to t10E30.value,
        "t11Min" to t11Min.value,
        "t11Nom" to t11Nom.value,
        "t11Max" to t11Max.value,
        "t12Dips" to t12Dips.value,
        "t12Bursts" to t12Bursts.value,
        "t12Surges" to t12Surges.value,
        "t12Esd" to t12Esd.value,
        "t12Rad" to t12Rad.value,
        "t12Cond" to t12Cond.value,
        "t12Veh" to t12Veh.value,
        "t13Init" to t13Init.value,
        "t13High" to t13High.value,
        "t13Final" to t13Final.value,
        "t14Errors" to t14Errors.toList(),
        "t15Cycles" to t15Cycles.value,
        "t15Init" to t15Init.value,
        "t15Final" to t15Final.value,
        "t15Dates" to t15Dates.value
    )
}
fun fromMap(map: Map<String, Any>) {
    (map["t1Up"] as? List<String>)?.let { t1Up.clear(); t1Up.addAll(it) }
    (map["t1Down"] as? List<String>)?.let { t1Down.clear(); t1Down.addAll(it) }
    (map["t2Z1"] as? String)?.let { t2Z1.value = it }
    (map["t2T1"] as? String)?.let { t2T1.value = it }
    (map["t2Z2"] as? String)?.let { t2Z2.value = it }
    (map["t2T2"] as? String)?.let { t2T2.value = it }
    (map["t3Readings"] as? Map<String, String>)?.let { t3Readings.clear(); t3Readings.putAll(it) }
    (map["t4BaseRead"] as? String)?.let { t4BaseRead.value = it }
    (map["t4NewRead"] as? String)?.let { t4NewRead.value = it }
    (map["t5Readings"] as? List<String>)?.let { t5Readings.clear(); t5Readings.addAll(it) }
    (map["t6ZB"] as? String)?.let { t6ZB.value = it }
    (map["t6ZA"] as? String)?.let { t6ZA.value = it }
    (map["t6C0"] as? String)?.let { t6C0.value = it }
    (map["t6C5"] as? String)?.let { t6C5.value = it }
    (map["t6C15"] as? String)?.let { t6C15.value = it }
    (map["t6C30"] as? String)?.let { t6C30.value = it }
    (map["t7Readings"] as? List<String>)?.let { t7Readings.clear(); t7Readings.addAll(it) }
    (map["t8Ref"] as? String)?.let { t8Ref.value = it }
    (map["t8Tilt"] as? String)?.let { t8Tilt.value = it }
    (map["t9Tare"] as? String)?.let { t9Tare.value = it }
    (map["t9Gross"] as? List<String>)?.let { t9Gross.clear(); t9Gross.addAll(it) }
    (map["t10E0"] as? String)?.let { t10E0.value = it }
    (map["t10E5"] as? String)?.let { t10E5.value = it }
    (map["t10E15"] as? String)?.let { t10E15.value = it }
    (map["t10E30"] as? String)?.let { t10E30.value = it }
    (map["t11Min"] as? String)?.let { t11Min.value = it }
    (map["t11Nom"] as? String)?.let { t11Nom.value = it }
    (map["t11Max"] as? String)?.let { t11Max.value = it }
    (map["t12Dips"] as? Boolean)?.let { t12Dips.value = it }
    (map["t12Bursts"] as? Boolean)?.let { t12Bursts.value = it }
    (map["t12Surges"] as? Boolean)?.let { t12Surges.value = it }
    (map["t12Esd"] as? Boolean)?.let { t12Esd.value = it }
    (map["t12Rad"] as? Boolean)?.let { t12Rad.value = it }
    (map["t12Cond"] as? Boolean)?.let { t12Cond.value = it }
    (map["t12Veh"] as? Boolean)?.let { t12Veh.value = it }
    (map["t13Init"] as? String)?.let { t13Init.value = it }
    (map["t13High"] as? String)?.let { t13High.value = it }
    (map["t13Final"] as? String)?.let { t13Final.value = it }
    (map["t14Errors"] as? List<String>)?.let { t14Errors.clear(); t14Errors.addAll(it) }
    (map["t15Cycles"] as? String)?.let { t15Cycles.value = it }
    (map["t15Init"] as? String)?.let { t15Init.value = it }
    (map["t15Final"] as? String)?.let { t15Final.value = it }
    (map["t15Dates"] as? String)?.let { t15Dates.value = it }
}
}
