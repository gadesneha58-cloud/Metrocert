package com.example.ui

import androidx.compose.foundation.clickable
import androidx.compose.foundation.lazy.items
import androidx.compose.material.icons.filled.Add
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.ui.draw.clip
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.AutoAwesome
import androidx.compose.material.icons.filled.Home
import androidx.compose.material.icons.filled.Build
import androidx.compose.material.icons.filled.CheckCircle
import androidx.compose.material.icons.automirrored.filled.List
import androidx.compose.material.icons.filled.Search
import androidx.compose.material.icons.filled.MoreVert
import androidx.compose.material.icons.filled.Settings
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.input.pointer.pointerInput
import androidx.compose.foundation.gestures.detectVerticalDragGestures
import androidx.compose.ui.unit.IntOffset
import kotlin.math.roundToInt
import kotlin.math.abs
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.unit.dp
import androidx.lifecycle.viewmodel.compose.viewModel
import androidx.navigation.NavHostController
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import androidx.navigation.compose.currentBackStackEntryAsState
import androidx.navigation.compose.rememberNavController
import com.example.MetroCertViewModel
import com.example.ui.theme.*

enum class MetroCertRoute(val title: String, val icon: ImageVector) {
    Gallery("Gallery", Icons.Default.Search),
    Dashboard("Dashboard", Icons.Default.Home),
    Setup("Setup", Icons.Default.Build),
    Testing("Testing", Icons.AutoMirrored.Filled.List),
    Preview("Preview", Icons.Default.CheckCircle),
    Config("Config", Icons.Default.Settings)
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun MetroCertApp(
    viewModel: MetroCertViewModel = viewModel(),
    onSignOut: () -> Unit
) {
    val navController = rememberNavController()
    val navBackStackEntry by navController.currentBackStackEntryAsState()
    val currentRoute = navBackStackEntry?.destination?.route ?: MetroCertRoute.Dashboard.name
    val tabs = listOf(MetroCertRoute.Dashboard, MetroCertRoute.Config)

    Scaffold(
        topBar = {
            TopAppBar(
                title = { 
                    Row(verticalAlignment = androidx.compose.ui.Alignment.CenterVertically) {
                        Text(
                            text = "Metro",
                            style = MaterialTheme.typography.titleLarge,
                            fontWeight = androidx.compose.ui.text.font.FontWeight.Bold,
                            color = TextDark
                        )
                        Text(
                            text = "Cert",
                            style = MaterialTheme.typography.titleLarge,
                            fontWeight = androidx.compose.ui.text.font.FontWeight.Bold,
                            color = NeoAccent
                        )
                        Spacer(modifier = Modifier.width(6.dp))
                        Box(
                            modifier = Modifier
                                .size(24.dp)
                                .clip(androidx.compose.foundation.shape.CircleShape)
                                .background(NeoAccent),
                            contentAlignment = androidx.compose.ui.Alignment.Center
                        ) {
                            Icon(
                                imageVector = Icons.Default.CheckCircle,
                                contentDescription = "Check",
                                tint = androidx.compose.ui.graphics.Color.White,
                                modifier = Modifier.size(14.dp)
                            )
                        }
                    }
                },
                actions = {
                    var menuExpanded by remember { mutableStateOf(false) }
                    IconButton(onClick = { menuExpanded = true }) {
                        Icon(Icons.Default.MoreVert, contentDescription = "Settings", tint = TextDark)
                    }
                    DropdownMenu(
                        expanded = menuExpanded,
                        onDismissRequest = { menuExpanded = false },
                        modifier = Modifier.background(NeoSurface)
                    ) {
                        DropdownMenuItem(
                            text = { Text("Logout", color = TextDark) },
                            onClick = { 
                                menuExpanded = false
                                onSignOut()
                            }
                        )
                    }
                },
                colors = TopAppBarDefaults.topAppBarColors(
                    containerColor = NeoBackground,
                    titleContentColor = TextDark
                )
            )
        },
        bottomBar = {
            if (currentRoute in listOf(MetroCertRoute.Dashboard.name, MetroCertRoute.Config.name)) {
                Box(
                    modifier = Modifier
                        .background(NeoBackground)
                        .padding(horizontal = 16.dp, vertical = 8.dp)
                        .neoShadow(cornerRadius = 24.dp)
                        .clip(RoundedCornerShape(24.dp))
                ) {
                    NavigationBar(
                        containerColor = NeoSurface,
                        tonalElevation = 0.dp
                    ) {
                        tabs.forEach { route ->
                            NavigationBarItem(
                                icon = { Icon(route.icon, contentDescription = route.title) },
                                label = { Text(route.title, style = MaterialTheme.typography.labelSmall) },
                                selected = currentRoute == route.name,
                                colors = NavigationBarItemDefaults.colors(
                                    selectedIconColor = NeoAccent,
                                    unselectedIconColor = TextMuted,
                                    selectedTextColor = NeoAccent,
                                    unselectedTextColor = TextMuted,
                                    indicatorColor = NeoSurface
                                ),
                                onClick = {
                                    navController.navigate(route.name) {
                                        popUpTo(navController.graph.startDestinationId) { saveState = true }
                                        launchSingleTop = true
                                        restoreState = true
                                    }
                                }
                            )
                        }
                    }
                }
            }
        }
    ) { innerPadding ->
        Column(modifier = Modifier.padding(innerPadding).fillMaxSize().background(NeoBackground)) {
            if (currentRoute == MetroCertRoute.Setup.name || currentRoute == MetroCertRoute.Testing.name || currentRoute == MetroCertRoute.Preview.name) {
                val activeReports by viewModel.activeReports.collectAsStateWithLifecycle()
                val currentIndex by viewModel.currentIndex.collectAsStateWithLifecycle()
                
                androidx.compose.foundation.lazy.LazyRow(
                    modifier = Modifier.fillMaxWidth().padding(horizontal = 16.dp, vertical = 8.dp),
                    horizontalArrangement = Arrangement.spacedBy(8.dp)
                ) {
                    items(activeReports.size) { index ->
                        val isSelected = index == currentIndex
                        var offsetY by remember { mutableStateOf(0f) }
                        
                        Box(
                            modifier = Modifier
                                .offset { IntOffset(0, offsetY.roundToInt()) }
                                .neoShadow(cornerRadius = 16.dp, isPressed = isSelected)
                                .clip(RoundedCornerShape(16.dp))
                                .background(if (isSelected) NeoAccent else NeoSurface)
                                .pointerInput(Unit) {
                                    detectVerticalDragGestures(
                                        onDragEnd = {
                                            if (abs(offsetY) > 150f) {
                                                viewModel.deleteMachine(index)
                                            }
                                            offsetY = 0f
                                        },
                                        onDragCancel = {
                                            offsetY = 0f
                                        },
                                        onVerticalDrag = { change, dragAmount ->
                                            change.consume()
                                            offsetY += dragAmount
                                        }
                                    )
                                }
                                .clickable { viewModel.switchMachine(index) }
                                .padding(horizontal = 16.dp, vertical = 8.dp)
                        ) {
                            Text(
                                "Machine ${index + 1}",
                                color = if (isSelected) androidx.compose.ui.graphics.Color.White else TextDark,
                                fontWeight = androidx.compose.ui.text.font.FontWeight.Bold
                            )
                        }
                    }
                    item {
                        Box(
                            modifier = Modifier
                                .neoShadow(cornerRadius = 16.dp)
                                .clip(RoundedCornerShape(16.dp))
                                .background(NeoSurface)
                                .clickable { navController.navigate(MetroCertRoute.Gallery.name) }
                                .padding(horizontal = 16.dp, vertical = 8.dp)
                        ) {
                            Icon(
                                imageVector = androidx.compose.material.icons.Icons.Default.Add,
                                contentDescription = "Add Machine",
                                tint = NeoAccent
                            )
                        }
                    }
                }
            }
            Box(modifier = Modifier.weight(1f).fillMaxWidth()) {
                NavHost(
                    navController = navController, 
                    startDestination = MetroCertRoute.Dashboard.name,
                    enterTransition = { androidx.compose.animation.fadeIn(animationSpec = androidx.compose.animation.core.tween(150)) },
                    exitTransition = { androidx.compose.animation.fadeOut(animationSpec = androidx.compose.animation.core.tween(150)) }
                ) {
                    composable(MetroCertRoute.Dashboard.name) {
                        DashboardScreen(viewModel, onNavigateToSetup = {
                            navController.navigate(MetroCertRoute.Gallery.name)
                        })
                    }
                    composable(MetroCertRoute.Gallery.name) {
                        ScaleGalleryScreen(
                            viewModel = viewModel, 
                            onInstrumentSelected = { item ->
                                viewModel.startNewInspectionWithInstrument(item)
                                navController.navigate(MetroCertRoute.Setup.name)
                            },
                            onManualEntry = {
                                viewModel.startNewInspection()
                                navController.navigate(MetroCertRoute.Setup.name)
                            }
                        )
                    }
                    composable(MetroCertRoute.Setup.name) {
                        SetupScreen(viewModel, onNext = {
                            navController.navigate(MetroCertRoute.Testing.name)
                        })
                    }
                    composable(MetroCertRoute.Testing.name) {
                        TestingScreen(viewModel, onNext = {
                            navController.navigate(MetroCertRoute.Preview.name)
                        })
                    }
                    composable(MetroCertRoute.Preview.name) {
                        val context = androidx.compose.ui.platform.LocalContext.current
                        PreviewScreen(
                            viewModel = viewModel,
                            onBack = { navController.popBackStack() },
                            onExportPdf = { 
                                try {
                                    val pdfsDir = java.io.File(context.cacheDir, "pdfs")
                                    pdfsDir.mkdirs()
                                    val report = viewModel.currentReport.value
                                    val file = java.io.File(pdfsDir, "MetroCert_Report_${report.certificateNo}.pdf")
                                    val uri = androidx.core.content.FileProvider.getUriForFile(
                                        context, 
                                        "${context.packageName}.fileprovider", 
                                        file
                                    )
                                    com.example.util.PdfGenerator.generatePdf(context, uri, report)
                                    
                                    val intent = android.content.Intent(android.content.Intent.ACTION_SEND).apply {
                                        type = "application/pdf"
                                        putExtra(android.content.Intent.EXTRA_STREAM, uri)
                                        addFlags(android.content.Intent.FLAG_GRANT_READ_URI_PERMISSION)
                                    }
                                    context.startActivity(android.content.Intent.createChooser(intent, "Share PDF Report"))
                                } catch (e: Exception) {
                                    e.printStackTrace()
                                }
                            },
                            onExportConsolidatedPdf = {
                                try {
                                    val pdfsDir = java.io.File(context.cacheDir, "pdfs")
                                    pdfsDir.mkdirs()
                                    val reports = viewModel.activeReports.value
                                    val timestamp = System.currentTimeMillis()
                                    val file = java.io.File(pdfsDir, "MetroCert_Consolidated_$timestamp.pdf")
                                    val uri = androidx.core.content.FileProvider.getUriForFile(
                                        context,
                                        "${context.packageName}.fileprovider",
                                        file
                                    )
                                    com.example.util.PdfGenerator.generateConsolidatedPdf(context, uri, reports)
                                    
                                    val intent = android.content.Intent(android.content.Intent.ACTION_SEND).apply {
                                        type = "application/pdf"
                                        putExtra(android.content.Intent.EXTRA_STREAM, uri)
                                        addFlags(android.content.Intent.FLAG_GRANT_READ_URI_PERMISSION)
                                    }
                                    context.startActivity(android.content.Intent.createChooser(intent, "Share Consolidated PDF Report"))
                                } catch (e: Exception) {
                                    e.printStackTrace()
                                }
                            }
                        )
                    }
                    composable(MetroCertRoute.Config.name) {
                        ConfigScreen()
                    }
                }
            }
        }
    }
}
