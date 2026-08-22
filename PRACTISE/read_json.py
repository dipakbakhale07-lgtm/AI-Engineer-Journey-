import json

with open("practise/api_data.json", "r", encoding="utf-8") as file:
    data = json.load(file)

print("Name:", data["name"])
print("Role:", data["role"])
print("Day:", data["day"])
print("Skills:", ", ".join(data["skills"]))
