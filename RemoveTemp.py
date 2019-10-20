import os, sys
# path = os.path
print("Removed These File(s) : ")
for file in os.listdir("./uploads"):
    if "temp" in file:
        print(file)
        os.remove(os.path.join("./uploads", file))
