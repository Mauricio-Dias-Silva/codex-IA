
lines = open("build_exe.bat").readlines()
# Filter out pause
lines = [l for l in lines if "pause" not in l.lower()]
with open("build_auto.bat", "w") as f:
    f.writelines(lines)
print("Created build_auto.bat")
