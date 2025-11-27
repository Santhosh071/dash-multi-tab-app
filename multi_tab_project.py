import os

project = "multi_tab_project"

folders = [
    f"{project}/assets",
    f"{project}/pages",
    f"{project}/helpers",
    f"{project}/data",
    f"{project}/models"
]

files = {
    f"{project}/app.py": "",
    f"{project}/index.py": "",
    f"{project}/assets/style.css": "/* Custom CSS */",
    f"{project}/pages/data_explorer.py": "",
    f"{project}/pages/house_price.py": "",
    f"{project}/pages/matrix_lab.py": "",
    f"{project}/helpers/eda_utils.py": "",
    f"{project}/helpers/model_utils.py": "",
    f"{project}/helpers/matrix_utils.py": "",
    f"{project}/data/sample.csv": "id,value\n1,100\n2,200",
    f"{project}/models/house_price.pkl": ""
}

# Create folders
for folder in folders:
    os.makedirs(folder, exist_ok=True)

# Create files
for path, content in files.items():
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


print("Project folder 'multi_tab_project' created successfully.")
