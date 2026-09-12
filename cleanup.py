with open("app/src/main/java/com/example/ui/TestingScreen.kt", "r") as f:
    content = f.read()

import re

# Remove the second autoFillFailing definition
pattern = re.compile(r'    fun autoFillFailing\(\) \{.*?    \}\n\n    fun autoFillFailing\(\) \{.*?    \}', re.DOTALL)
match = pattern.search(content)
if match:
    # Just keep the first one
    first_func = re.search(r'    fun autoFillFailing\(\) \{.*?    \}', match.group(0), re.DOTALL).group(0)
    content = content.replace(match.group(0), first_func)

# Fix the brace issue at the end
# Check if it ends properly
if content.strip().endswith('}'):
    # Let's count open and close braces
    open_braces = content.count('{')
    close_braces = content.count('}')
    print(f"Open braces: {open_braces}, Close braces: {close_braces}")
    
    if open_braces > close_braces:
        content += '\n' + '}' * (open_braces - close_braces)
    elif close_braces > open_braces:
        # Too many close braces?
        pass

with open("app/src/main/java/com/example/ui/TestingScreen.kt", "w") as f:
    f.write(content)
