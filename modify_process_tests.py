import re

with open("app/src/main/java/com/example/MetroCertViewModel.kt", "r") as f:
    content = f.read()

# Add a save step at the end of processTests
old_end = """                enduranceResult = enduranceResult,
                digitalSignature = inputs.signature,
                photoAttached = inputs.photoAttached
            )
        }
    }

}"""

new_end = """                enduranceResult = enduranceResult,
                digitalSignature = inputs.signature,
                photoAttached = inputs.photoAttached
            )
        }
        viewModelScope.launch {
            reportDao.insertReport(_activeReports.value[_currentIndex.value])
        }
    }

}"""

if old_end in content:
    content = content.replace(old_end, new_end)
    with open("app/src/main/java/com/example/MetroCertViewModel.kt", "w") as f:
        f.write(content)
else:
    print("Could not find the end of processTests")

