with open('app/src/main/java/com/example/ui/ScaleGalleryScreen.kt', 'w') as f:
    f.write("""package com.example.ui

import androidx.compose.animation.*
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.grid.GridCells
import androidx.compose.foundation.lazy.grid.LazyVerticalGrid
import androidx.compose.foundation.lazy.grid.items
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import com.example.MetroCertViewModel
import com.example.data.InstrumentCatalogItem
import com.example.ui.theme.*

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun ScaleGalleryScreen(viewModel: MetroCertViewModel, onInstrumentSelected: (InstrumentCatalogItem) -> Unit) {
    val catalog by viewModel.instrumentCatalog.collectAsStateWithLifecycle()
    
    var searchQuery by remember { mutableStateOf("") }
    var expandedClass by remember { mutableStateOf<String?>(null) }
    
    val classOptions = listOf("I", "II", "III", "IIII")

    Column(
        modifier = Modifier
            .fillMaxSize()
            .background(MaterialTheme.colorScheme.background)
    ) {
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(horizontal = 24.dp)
        ) {
            Spacer(modifier = Modifier.height(24.dp))
            
            Text(
                "Instrument Catalog", 
                style = MaterialTheme.typography.titleLarge, 
                fontWeight = FontWeight.Bold, 
                color = TextDark
            )
            Spacer(modifier = Modifier.height(16.dp))
            
            // Neumorphic Search Bar
            Box(modifier = Modifier.neoShadow(cornerRadius = 16.dp)) {
                OutlinedTextField(
                    value = searchQuery,
                    onValueChange = { searchQuery = it },
                    modifier = Modifier.fillMaxWidth().defaultMinSize(minHeight = 56.dp),
                    placeholder = { Text("Search manufacturer, model, type...", fontSize = 16.sp, color = TextMuted) },
                    textStyle = LocalTextStyle.current.copy(fontSize = 16.sp),
                    leadingIcon = { Icon(Icons.Default.Search, contentDescription = "Search", tint = NeoAccent) },
                    trailingIcon = {
                        if (searchQuery.isNotEmpty()) {
                            IconButton(onClick = { searchQuery = "" }) {
                                Icon(Icons.Default.Clear, contentDescription = "Clear", tint = TextMuted)
                            }
                        }
                    },
                    shape = RoundedCornerShape(16.dp),
                    colors = TextFieldDefaults.colors(
                        focusedContainerColor = NeoSurface,
                        unfocusedContainerColor = NeoSurface,
                        focusedIndicatorColor = Color.Transparent,
                        unfocusedIndicatorColor = Color.Transparent,
                        focusedTextColor = TextDark,
                        unfocusedTextColor = TextDark
                    ),
                    singleLine = true
                )
            }
            
            Spacer(modifier = Modifier.height(24.dp))
            
            if (searchQuery.isNotBlank()) {
                val searchResults = catalog.filter { item ->
                    item.model.contains(searchQuery, ignoreCase = true) || 
                    item.manufacturer.contains(searchQuery, ignoreCase = true) ||
                    item.type.contains(searchQuery, ignoreCase = true)
                }
                
                Text(
                    text = "Search Results (${searchResults.size})",
                    style = MaterialTheme.typography.labelMedium,
                    color = TextMuted,
                    modifier = Modifier.padding(bottom = 12.dp)
                )
                
                if (searchResults.isEmpty()) {
                    Box(modifier = Modifier.weight(1f).fillMaxWidth(), contentAlignment = Alignment.Center) {
                        Column(horizontalAlignment = Alignment.CenterHorizontally) {
                            Icon(Icons.Default.SearchOff, contentDescription = null, modifier = Modifier.size(64.dp), tint = TextMuted.copy(alpha = 0.5f))
                            Spacer(modifier = Modifier.height(16.dp))
                            Text("No scales found", style = MaterialTheme.typography.titleMedium, color = TextDark)
                            Text("Try adjusting your search query.", style = MaterialTheme.typography.bodyMedium, color = TextMuted)
                        }
                    }
                } else {
                    LazyVerticalGrid(
                        columns = GridCells.Adaptive(minSize = 300.dp),
                        contentPadding = PaddingValues(bottom = 24.dp),
                        horizontalArrangement = Arrangement.spacedBy(16.dp),
                        verticalArrangement = Arrangement.spacedBy(16.dp),
                        modifier = Modifier.fillMaxSize()
                    ) {
                        items(searchResults, key = { it.model }) { item ->
                            ScaleGalleryCard(item) {
                                onInstrumentSelected(item)
                            }
                        }
                    }
                }
            } else {
                LazyColumn(
                    modifier = Modifier.fillMaxSize(),
                    contentPadding = PaddingValues(bottom = 24.dp),
                    verticalArrangement = Arrangement.spacedBy(16.dp)
                ) {
                    classOptions.forEach { accClass ->
                        item {
                            val isExpanded = expandedClass == accClass
                            val classItems = catalog.filter { it.accuracyClass == accClass }
                            
                            Column(
                                modifier = Modifier
                                    .fillMaxWidth()
                                    .neoShadow(cornerRadius = 16.dp)
                                    .background(NeoSurface, RoundedCornerShape(16.dp))
                                    .clickable { 
                                        expandedClass = if (isExpanded) null else accClass 
                                    }
                                    .animateContentSize()
                            ) {
                                Row(
                                    modifier = Modifier.fillMaxWidth().padding(horizontal = 20.dp, vertical = 18.dp),
                                    horizontalArrangement = Arrangement.SpaceBetween,
                                    verticalAlignment = Alignment.CenterVertically
                                ) {
                                    Text(
                                        "Class $accClass Instruments",
                                        style = MaterialTheme.typography.titleMedium,
                                        fontWeight = FontWeight.SemiBold,
                                        color = NeoAccent
                                    )
                                    Icon(
                                        if (isExpanded) Icons.Default.KeyboardArrowUp else Icons.Default.KeyboardArrowDown,
                                        contentDescription = null,
                                        tint = NeoAccent
                                    )
                                }
                                
                                AnimatedVisibility(visible = isExpanded) {
                                    Column(modifier = Modifier.fillMaxWidth().padding(start = 16.dp, end = 16.dp, bottom = 16.dp)) {
                                        HorizontalDivider(color = NeoBackground)
                                        Spacer(modifier = Modifier.height(16.dp))
                                        
                                        if (classItems.isEmpty()) {
                                            Text("No instruments found for this class.", color = TextMuted, modifier = Modifier.padding(bottom = 8.dp, start = 4.dp))
                                        } else {
                                            classItems.forEach { item ->
                                                ScaleGalleryCard(item) {
                                                    onInstrumentSelected(item)
                                                }
                                                if (item != classItems.last()) {
                                                    Spacer(modifier = Modifier.height(16.dp))
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }
}

@Composable
fun ScaleGalleryCard(item: InstrumentCatalogItem, onIssueCert: () -> Unit) {
    val (badgeBg, badgeText) = when (item.accuracyClass) {
        "I" -> Color(0xFFF3E8FF) to Color(0xFF9333EA)
        "II" -> Color(0xFFDBEAFE) to Color(0xFF2563EB)
        "III" -> Color(0xFFD1FAE5) to Color(0xFF059669)
        "IIII" -> Color(0xFFFEF3C7) to Color(0xFFD97706)
        else -> NeoBackground to TextMuted
    }

    Box(
        modifier = Modifier
            .fillMaxWidth()
            .neoShadow(cornerRadius = 16.dp)
            .background(NeoSurface, RoundedCornerShape(16.dp))
            .padding(20.dp)
    ) {
        Column {
            Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween, verticalAlignment = Alignment.Top) {
                Column(modifier = Modifier.weight(1f)) {
                    Text(item.manufacturer, style = MaterialTheme.typography.labelMedium, color = TextMuted)
                    Text(item.model, fontWeight = FontWeight.Bold, color = TextDark, style = MaterialTheme.typography.titleMedium)
                }
                Surface(
                    shape = RoundedCornerShape(8.dp),
                    color = badgeBg,
                    modifier = Modifier.padding(start = 8.dp)
                ) {
                    Text(
                        text = "Class ${item.accuracyClass}",
                        color = badgeText,
                        style = MaterialTheme.typography.labelSmall,
                        fontWeight = FontWeight.Bold,
                        modifier = Modifier.padding(horizontal = 8.dp, vertical = 4.dp)
                    )
                }
            }
            
            Spacer(modifier = Modifier.height(16.dp))
            
            Row(modifier = Modifier.fillMaxWidth()) {
                SpecBox(label = "Max Capacity", value = "${item.maxCapacity} ${item.unit}", modifier = Modifier.weight(1f))
                Spacer(modifier = Modifier.width(8.dp))
                SpecBox(label = "Min Load", value = "${item.minCapacity} ${item.unit}", modifier = Modifier.weight(1f))
            }
            Spacer(modifier = Modifier.height(8.dp))
            Row(modifier = Modifier.fillMaxWidth()) {
                SpecBox(label = "Verification (e)", value = "${item.scaleInterval} ${item.unit}", modifier = Modifier.weight(1f))
                Spacer(modifier = Modifier.width(8.dp))
                SpecBox(label = "Division (d)", value = "${item.d} ${item.unit}", modifier = Modifier.weight(1f))
            }
            
            Spacer(modifier = Modifier.height(20.dp))
            
            HorizontalDivider(color = NeoBackground)
            
            Spacer(modifier = Modifier.height(16.dp))
            
            Button(
                onClick = onIssueCert,
                modifier = Modifier.fillMaxWidth(),
                shape = RoundedCornerShape(12.dp),
                colors = ButtonDefaults.buttonColors(containerColor = NeoAccent),
                contentPadding = PaddingValues(vertical = 12.dp)
            ) {
                Icon(Icons.Default.Verified, contentDescription = null, modifier = Modifier.size(18.dp))
                Spacer(modifier = Modifier.width(8.dp))
                Text("Select & Verify", fontWeight = FontWeight.Bold)
            }
        }
    }
}

@Composable
fun SpecBox(label: String, value: String, modifier: Modifier = Modifier) {
    Column(
        modifier = modifier
            .background(NeoBackground, RoundedCornerShape(8.dp))
            .padding(10.dp)
    ) {
        Text(label, style = MaterialTheme.typography.labelSmall, color = TextMuted)
        Spacer(modifier = Modifier.height(2.dp))
        Text(value, style = MaterialTheme.typography.bodyMedium, fontWeight = FontWeight.SemiBold, color = TextDark)
    }
}
""")
