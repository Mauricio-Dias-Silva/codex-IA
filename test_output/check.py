import sys
with open("test_output/target.py") as f: c=f.read()
if "HELLO WORLD" not in c: sys.exit(1)
print("Found it!")