package com.example.ui

import androidx.compose.animation.core.animateFloat
import androidx.compose.animation.core.infiniteRepeatable
import androidx.compose.animation.core.rememberInfiniteTransition
import androidx.compose.animation.core.tween
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Add
import androidx.compose.material.icons.filled.CheckCircle
import androidx.compose.material.icons.filled.Description
import androidx.compose.material.icons.filled.MoreVert
import androidx.compose.material.icons.filled.Search
import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.graphicsLayer
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import com.example.MetroCertViewModel
import com.example.data.Report
import com.example.ui.theme.*
import java.text.SimpleDateFormat
import java.util.Date
import java.util.Locale

@Composable
fun DashboardScreen(viewModel: MetroCertViewModel, onNavigateToSetup: () -> Unit) {
    val savedReports by viewModel.savedReports.collectAsState()
    val totalReports = savedReports.size
    val passCount = savedReports.count { it.status == "Pass" }
    
    Column(
        modifier = Modifier
            .fillMaxSize()
            .background(MaterialTheme.colorScheme.background)
    ) {
        Column(modifier = Modifier.padding(top = 32.dp, start = 24.dp, end = 24.dp, bottom = 16.dp)) {
            Row(verticalAlignment = Alignment.CenterVertically) {
                Box(
                    modifier = Modifier
                        .size(48.dp)
                        .neoShadow(cornerRadius = 24.dp)
                        .background(NeoSurface, CircleShape),
                    contentAlignment = Alignment.Center
                ) {
                    Icon(
                        imageVector = Icons.Default.Search,
                        contentDescription = "Logo",
                        tint = NeoAccent,
                        modifier = Modifier.size(24.dp)
                    )
                }
                Spacer(modifier = Modifier.width(16.dp))
                Column {
                    Text("Hi Admin", style = MaterialTheme.typography.bodyMedium, color = TextMuted)
                    Text("Welcome Back", style = MaterialTheme.typography.titleLarge, fontWeight = FontWeight.Bold, color = TextDark)
                }
            }
            
            Spacer(modifier = Modifier.height(32.dp))
            
            // Neumorphic Stats Card
            val passRate = if (totalReports > 0) ((passCount.toFloat() / totalReports) * 100).toInt() else 0
            Box(
                modifier = Modifier
                    .fillMaxWidth()
                    .neoShadow(cornerRadius = 24.dp)
                    .background(NeoSurface, RoundedCornerShape(24.dp))
                    .padding(24.dp)
            ) {
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.SpaceBetween,
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Column {
                        Text("$totalReports Tests", style = MaterialTheme.typography.headlineMedium, fontWeight = FontWeight.Bold, color = TextDark)
                        Text("$passRate% Pass Rate", style = MaterialTheme.typography.bodyLarge, color = TextMuted)
                    }
                    
                    Button(
                        onClick = onNavigateToSetup,
                        colors = ButtonDefaults.buttonColors(containerColor = NeoSurface),
                        shape = CircleShape,
                        contentPadding = PaddingValues(horizontal = 24.dp, vertical = 12.dp),
                        elevation = ButtonDefaults.buttonElevation(0.dp, 0.dp),
                        modifier = Modifier.neoShadow(cornerRadius = 24.dp)
                    ) {
                        Text("NEW TEST", color = NeoAccent, fontWeight = FontWeight.Bold, style = MaterialTheme.typography.labelLarge)
                    }
                }
            }
        }
        
        Spacer(modifier = Modifier.height(16.dp))
        
        Row(
            modifier = Modifier.fillMaxWidth().padding(horizontal = 24.dp, vertical = 16.dp),
            horizontalArrangement = Arrangement.SpaceBetween,
            verticalAlignment = Alignment.CenterVertically
        ) {
            Text("Recent Reports", style = MaterialTheme.typography.titleLarge, fontWeight = FontWeight.Bold, color = TextDark)
            Text("View all", style = MaterialTheme.typography.bodyMedium, color = NeoAccent, fontWeight = FontWeight.SemiBold)
        }
        
        LazyColumn(
            modifier = Modifier.fillMaxWidth(),
            contentPadding = PaddingValues(bottom = 24.dp, start = 24.dp, end = 24.dp),
            verticalArrangement = Arrangement.spacedBy(16.dp)
        ) {
            items(savedReports) { report ->
                ReportListItem(report)
            }
        }
    }
}

@Composable
fun ReportListItem(report: Report) {
    Box(
        modifier = Modifier
            .fillMaxWidth()
            .neoShadow(cornerRadius = 20.dp)
            .background(NeoSurface, RoundedCornerShape(20.dp))
            .padding(16.dp)
    ) {
        Row(
            modifier = Modifier.fillMaxWidth(),
            verticalAlignment = Alignment.CenterVertically
        ) {
            Box(
                modifier = Modifier
                    .size(52.dp)
                    .neoShadow(cornerRadius = 26.dp, isPressed = true)
                    .background(NeoSurface, CircleShape),
                contentAlignment = Alignment.Center
            ) {
                Icon(Icons.Default.Description, contentDescription = null, tint = NeoAccent, modifier = Modifier.size(24.dp))
            }
            
            Spacer(modifier = Modifier.width(16.dp))
            
            Column(modifier = Modifier.weight(1f)) {
                Text(report.certificateNo.ifEmpty { "Uncertified" }, fontWeight = FontWeight.Bold, color = TextDark, style = MaterialTheme.typography.titleMedium)
                val dateStr = SimpleDateFormat("MMM dd, yyyy", Locale.getDefault()).format(Date(report.date))
                Text("${report.manufacturer} ${report.modelNumber} • $dateStr", style = MaterialTheme.typography.bodySmall, color = TextMuted)
            }
            
            val isPass = report.status == "Pass"
            val bgColor = if (isPass) PassBackground else FailBackground
            val textColor = if (isPass) PassText else FailText
            
            Box(
                modifier = Modifier
                    .background(bgColor, CircleShape)
                    .padding(horizontal = 12.dp, vertical = 6.dp)
            ) {
                Text(
                    text = report.status.uppercase(), 
                    color = textColor, 
                    fontWeight = FontWeight.Bold, 
                    style = MaterialTheme.typography.labelSmall
                )
            }
        }
    }
}
