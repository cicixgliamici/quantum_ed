import os

for root, dirs, files in os.walk('docs'):
    for f in files:
        if f.endswith('.md'):
            p = os.path.join(root, f)
            with open(p, 'r', encoding='utf-8') as fp:
                lines = fp.readlines()
            for idx, line in enumerate(lines):
                stripped = line.strip()
                if stripped == '$$' and (line.startswith(' ') or line.startswith('\t')):
                    print(f"{p}:{idx+1}: indented $$: {repr(line)}")
