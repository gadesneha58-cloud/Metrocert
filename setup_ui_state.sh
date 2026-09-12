cat << 'INNER_EOF' > app/src/main/java/com/example/ui/TestingState.kt
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
            t15Cycles.value, t15Init.value, t15Final.value, t15Dates.value
        )
    }
}
INNER_EOF
chmod +x setup_ui_state.sh
./setup_ui_state.sh
