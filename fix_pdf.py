import re
with open('app/src/main/java/com/example/util/PdfGenerator.kt', 'r') as f:
    content = f.read()

# The lint tool incorrectly swapped Color.parseColor("#HEX") with "#HEX".toColorInt()
# without adding the correct android.graphics.Color import or keeping Color.parseColor.
# We will revert those specific changes back to Color.parseColor since they work safely in our environment.

content = re.sub(r'"(#\w+)".toColorInt\(\)', r'Color.parseColor("\1")', content)

with open('app/src/main/java/com/example/util/PdfGenerator.kt', 'w') as f:
    f.write(content)
