with open('app/src/main/java/com/example/MetroCertViewModel.kt', 'r') as f:
    lines = f.readlines()

new_lines = []
in_seed = False
for i, line in enumerate(lines):
    if "val seedData = listOf(" in line:
        in_seed = True
        new_lines.append(line)
        continue
    if in_seed:
        if line.strip() == ")" or line.strip() == ");" or line.strip() == "val db = firestore" or "val db = firestore" in line:
            if "val db = firestore" in line:
                # we've gone too far, but wait, the old code had an extra `)`
                pass
        
        # just skip all lines until we hit `val db = firestore`
        if "val db = firestore" in line:
            in_seed = False
            new_lines.append("        \n")
            new_lines.append(line)
    else:
        new_lines.append(line)

with open('app/src/main/java/com/example/MetroCertViewModel.kt', 'w') as f:
    f.writelines(new_lines)
