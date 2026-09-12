cat << 'INNER_EOF' > app/src/main/java/com/example/util/PdfGenerator.kt
package com.example.util

import android.content.Context
import android.graphics.Canvas
import android.graphics.Color
import android.graphics.Paint
import android.graphics.Typeface
import android.graphics.pdf.PdfDocument
import android.net.Uri
import com.example.data.Report
import java.text.SimpleDateFormat
import java.util.Date
import java.util.Locale

object PdfGenerator {
    fun generatePdf(context: Context, uri: Uri, report: Report) {
        val pdfDocument = PdfDocument()
        val pageInfo = PdfDocument.PageInfo.Builder(595, 842, 1).create()
        val page = pdfDocument.startPage(pageInfo)
        val canvas = page.canvas
        
        val titlePaint = Paint().apply { typeface = Typeface.create(Typeface.DEFAULT, Typeface.BOLD); textSize = 24f; color = Color.parseColor("#0F52BA"); textAlign = Paint.Align.CENTER }
        val headerPaint = Paint().apply { typeface = Typeface.create(Typeface.DEFAULT, Typeface.BOLD); textSize = 14f; color = Color.BLACK }
        val bodyPaint = Paint().apply { typeface = Typeface.create(Typeface.DEFAULT, Typeface.NORMAL); textSize = 12f; color = Color.DKGRAY }
        val passPaint = Paint().apply { typeface = Typeface.create(Typeface.DEFAULT, Typeface.BOLD); textSize = 12f; color = Color.parseColor("#065F46") }
        val failPaint = Paint().apply { typeface = Typeface.create(Typeface.DEFAULT, Typeface.BOLD); textSize = 12f; color = Color.parseColor("#9F1239") }
        val linePaint = Paint().apply { color = Color.GRAY; strokeWidth = 1f }

        var currentY = 50f
        val startX = 50f
        val pageWidth = 595f

        canvas.drawText("MetroCert", pageWidth / 2, currentY, titlePaint)
        currentY += 25f
        titlePaint.textSize = 16f
        titlePaint.color = Color.BLACK
        canvas.drawText("OIML R-76 Verification Report", pageWidth / 2, currentY, titlePaint)
        currentY += 40f
        
        canvas.drawLine(startX, currentY, pageWidth - startX, currentY, linePaint)
        currentY += 20f

        canvas.drawText("Instrument Details", startX, currentY, headerPaint)
        currentY += 20f
        canvas.drawText("Manufacturer: ${report.manufacturer}", startX, currentY, bodyPaint)
        canvas.drawText("Model: ${report.modelNumber}", startX + 250f, currentY, bodyPaint)
        currentY += 20f
        canvas.drawText("Serial Number: ${report.serialNumber}", startX, currentY, bodyPaint)
        canvas.drawText("Certificate No: ${report.certificateNo}", startX + 250f, currentY, bodyPaint)
        currentY += 20f
        canvas.drawText("Class: ${report.accuracyClass} | Max: ${report.maxCapacity} | e: ${report.e}", startX, currentY, bodyPaint)
        currentY += 30f
        
        canvas.drawLine(startX, currentY, pageWidth - startX, currentY, linePaint)
        currentY += 20f

        canvas.drawText("Test Results Summary", startX, currentY, headerPaint)
        currentY += 20f

        val results = listOf(
            "1. Weighing Performance" to (report.weighingResults.isNotEmpty() && report.weighingResults.all { it.isPass }),
            "2. Temp Effect" to (report.tempEffectResult?.isPass == true),
            "3. Eccentricity" to (report.eccentricityResult?.isPass == true),
            "4. Discrimination" to (report.discriminationResult?.isPass == true),
            "5. Repeatability" to (report.repeatabilityResult?.isPass == true),
            "6. Time-Dependence" to (report.timeDependenceResult?.isPass == true),
            "7. Stability" to (report.stabilityResult?.isPass == true),
            "8. Tilting" to (report.tiltingResult?.isPass == true),
            "9. Tare" to (report.tareResult?.isPass == true),
            "10. Warm-up" to (report.warmUpResult?.isPass == true),
            "11. Voltage" to (report.voltageResult?.isPass == true),
            "12. EMC" to (report.emcResult?.isPass == true),
            "13. Damp Heat" to (report.dampHeatResult?.isPass == true),
            "14. Span Stability" to (report.spanStabilityResult?.isPass == true),
            "15. Endurance" to (report.enduranceResult?.isPass == true)
        )

        var colX = startX
        results.forEachIndexed { index, (name, pass) ->
            if (index == 8) {
                colX = startX + 250f
                currentY -= (20f * 8)
            }
            canvas.drawText(name, colX, currentY, bodyPaint)
            val pPaint = if (pass) passPaint else failPaint
            canvas.drawText(if (pass) "PASS" else "FAIL", colX + 180f, currentY, pPaint)
            currentY += 20f
        }
        
        if (results.size > 8) currentY += 20f

        currentY += 20f
        canvas.drawLine(startX, currentY, pageWidth - startX, currentY, linePaint)
        currentY += 30f
        
        canvas.drawText("OVERALL VERDICT:", startX, currentY, headerPaint)
        val verdictPaint = if (report.status == "Pass") passPaint else failPaint
        verdictPaint.textSize = 16f
        canvas.drawText(report.status.uppercase(), startX + 150f, currentY, verdictPaint)

        currentY = 700f
        canvas.drawLine(startX, currentY, startX + 200f, currentY, linePaint)
        canvas.drawText("Auditor Signature", startX, currentY + 15f, bodyPaint)
        
        val dateStr = SimpleDateFormat("yyyy-MM-dd", Locale.getDefault()).format(Date(report.date))
        canvas.drawText("Date: $dateStr", startX, currentY + 35f, bodyPaint)

        pdfDocument.finishPage(page)
        try {
            context.contentResolver.openOutputStream(uri)?.use { outputStream ->
                pdfDocument.writeTo(outputStream)
            }
        } catch (e: Exception) {
            e.printStackTrace()
        } finally {
            pdfDocument.close()
        }
    }
}
INNER_EOF
chmod +x setup_pdf.sh
./setup_pdf.sh
