package com.example.data

data class InstrumentCatalogItem(
    val manufacturer: String = "",
    val model: String = "",
    val type: String = "",
    val accuracyClass: String = "",
    val maxCapacity: Double = 0.0,
    val minCapacity: Double = 0.0,
    val unit: String = "",
    val scaleInterval: Double = 0.0,
    val d: Double = 0.0
)
