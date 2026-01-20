import os

file_path = "requirements.txt"
content = ""

# Try reading with different encodings
encodings = ['utf-8', 'utf-16le', 'utf-16be', 'latin-1']
for enc in encodings:
    try:
        with open(file_path, 'r', encoding=enc) as f:
            content = f.read()
        print(f"Successfully read with {enc}")
        break
    except Exception as e:
        print(f"Failed with {enc}: {e}")

if content:
    # Remove null bytes if any (common artifact of bad encoding writes)
    content = content.replace('\x00', '')
    # Write back as utf-8
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Converted to UTF-8")
else:
    print("Could not read content.")
