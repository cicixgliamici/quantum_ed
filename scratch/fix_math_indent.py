import re

files = [
    'docs/00-intro/README.md',
    'docs/05-circuits-and-gates/README.md',
    'docs/06-density-matrices/README.md',
    'docs/07-noise-and-channels/README.md',
    'docs/08-hardware/README.md',
    'docs/10-quantum-algorithms/README.md',
    'docs/10-quantum-algorithms/quantum-phase-estimation.md',
]

for filepath in files:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    lines = content.splitlines()
    new_lines = []
    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()
        if stripped == '$$':
            # Found opening of a math block
            # Ensure blank line before opening $$
            if new_lines and new_lines[-1].strip() != '':
                new_lines.append('')
            new_lines.append('$$')
            i += 1
            # Collect lines until closing $$
            math_lines = []
            while i < len(lines) and lines[i].strip() != '$$':
                math_lines.append(lines[i].strip())
                i += 1
            # Append math lines flush-left (or standard indent)
            for m in math_lines:
                new_lines.append(m)
            # Append closing $$
            if i < len(lines) and lines[i].strip() == '$$':
                new_lines.append('$$')
                # Ensure blank line after closing $$
                if i + 1 < len(lines) and lines[i+1].strip() != '':
                    new_lines.append('')
                i += 1
        else:
            new_lines.append(line)
            i += 1

    result = '\n'.join(new_lines) + '\n'
    # Also clean up any accidental 3-spaces indented code blocks in 05
    result = result.replace('   ```python\n   import numpy as np\n   from quantum_ed.gates import CNOT, H, I, SWAP, kron_n\n\n   H2 = kron_n(H, H)\n   cnot_rev = H2 @ CNOT @ H2  # CNOT with control=1, target=0\n   swap_synth = CNOT @ cnot_rev @ CNOT\n\n   assert np.allclose(swap_synth, SWAP)\n   ```',
                            '```python\nimport numpy as np\nfrom quantum_ed.gates import CNOT, H, I, SWAP, kron_n\n\nH2 = kron_n(H, H)\ncnot_rev = H2 @ CNOT @ H2  # CNOT with control=1, target=0\nswap_synth = CNOT @ cnot_rev @ CNOT\n\nassert np.allclose(swap_synth, SWAP)\n```')
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(result)

print("Finished unindenting math blocks and ensuring blank lines.")
