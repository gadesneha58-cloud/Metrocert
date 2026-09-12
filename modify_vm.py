import re

with open("app/src/main/java/com/example/MetroCertViewModel.kt", "r") as f:
    content = f.read()

pattern = re.compile(r'    fun autoPopulateDemoTests\(.*?\}.*?\}', re.DOTALL)
match = pattern.search(content)

old_code = """    fun autoPopulateDemoTests(index: Int = _currentIndex.value) {
        val currentList = _activeReports.value
        val report = if (index in currentList.indices) currentList[index] else Report()
        val maxCap = if (report.maxCapacity > 0.0) report.maxCapacity else 30.0
        val e = if (report.e > 0.0) report.e else 0.005
        val minCap = if (report.minCapacity > 0.0) report.minCapacity else 0.1

        val t1Loads = listOf(minCap, maxCap * 0.25, maxCap * 0.5, maxCap * 0.75, maxCap)
        val t3Load = maxCap / 3
        val t4BaseLoad = minCap
        val t4ExtraLoad = 1.4 * e
        val t5Load = maxCap * 0.8
        val t6Load = maxCap * 0.5
        val t7Load = maxCap * 0.5
        val t8Load = maxCap
        val t9Loads = listOf(minCap, maxCap * 0.5, maxCap * 0.9)
        val t10Load = maxCap * 0.5
        val t11Load = maxCap * 0.5
        val t13Load = maxCap * 0.5

        val state = getTestingState(index)
        state.autoFillPassingData(
            t1Loads = t1Loads,
            t3Load = t3Load,
            t4BaseLoad = t4BaseLoad,
            t4ExtraLoad = t4ExtraLoad,
            e = e,
            t5Load = t5Load,
            t6Load = t6Load,
            t7Load = t7Load,
            t8Load = t8Load,
            t9Loads = t9Loads,
            t10Load = t10Load,
            t11Load = t11Load,
            t13Load = t13Load,
            maxCap = maxCap
        )
    }

    fun autoPopulateFullDemo(index: Int = _currentIndex.value) {
        autoPopulateDemoSetup(index)
        autoPopulateDemoTests(index)
    }"""

new_code = """    fun autoPopulateDemoTests(index: Int = _currentIndex.value, pass: Boolean = true) {
        val currentList = _activeReports.value
        val report = if (index in currentList.indices) currentList[index] else Report()
        val maxCap = if (report.maxCapacity > 0.0) report.maxCapacity else 30.0
        val e = if (report.e > 0.0) report.e else 0.005
        val minCap = if (report.minCapacity > 0.0) report.minCapacity else 0.1

        val t1Loads = listOf(minCap, maxCap * 0.25, maxCap * 0.5, maxCap * 0.75, maxCap)
        val t3Load = maxCap / 3
        val t4BaseLoad = minCap
        val t4ExtraLoad = 1.4 * e
        val t5Load = maxCap * 0.8
        val t6Load = maxCap * 0.5
        val t7Load = maxCap * 0.5
        val t8Load = maxCap
        val t9Loads = listOf(minCap, maxCap * 0.5, maxCap * 0.9)
        val t10Load = maxCap * 0.5
        val t11Load = maxCap * 0.5
        val t13Load = maxCap * 0.5

        val state = getTestingState(index)
        if (pass) {
            state.autoFillPassingData(
                t1Loads = t1Loads, t3Load = t3Load, t4BaseLoad = t4BaseLoad, t4ExtraLoad = t4ExtraLoad,
                e = e, t5Load = t5Load, t6Load = t6Load, t7Load = t7Load, t8Load = t8Load,
                t9Loads = t9Loads, t10Load = t10Load, t11Load = t11Load, t13Load = t13Load, maxCap = maxCap
            )
        } else {
            state.autoFillFailingData(
                t1Loads = t1Loads, t3Load = t3Load, t4BaseLoad = t4BaseLoad, t4ExtraLoad = t4ExtraLoad,
                e = e, t5Load = t5Load, t6Load = t6Load, t7Load = t7Load, t8Load = t8Load,
                t9Loads = t9Loads, t10Load = t10Load, t11Load = t11Load, t13Load = t13Load, maxCap = maxCap
            )
        }
    }

    fun autoPopulateFullDemo(index: Int = _currentIndex.value, pass: Boolean = true) {
        autoPopulateDemoSetup(index)
        autoPopulateDemoTests(index, pass)
    }"""

if old_code in content:
    content = content.replace(old_code, new_code)
    with open("app/src/main/java/com/example/MetroCertViewModel.kt", "w") as f:
        f.write(content)
else:
    print("Could not find exact block to replace")

