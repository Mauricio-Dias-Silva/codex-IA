import os

# Create the test_output directory if it doesn't exist
if not os.path.exists("test_output"):
    os.makedirs("test_output")

# Create and write to the target.py file
with open("test_output/target.py", "w") as f:
    f.write("print(\"HELLO WORLD\")")