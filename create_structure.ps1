# Create directories
New-Item -ItemType Directory -Path "app","app\controllers","app\models","app\views","app\views\main","app\views\auth","app\templates","app\static","migrations","tests"

# Create empty files
@"
app\controllers\__init__.py
app\models\__init__.py
app\views\main\__init__.py
app\views\auth\__init__.py
app\extensions.py
app\config.py
app\__init__.py
requirements.txt
run.py
.env
app\views\main\routes.py
app\views\auth\routes.py
app\controllers\main_controller.py
app\controllers\auth_controller.py
app\templates\index.html
app\templates\about.html
app\templates\content\show.html
app\templates\content\create.html
"@ | ForEach-Object { New-Item -ItemType File -Path $_ }

Write-Host "Structure created successfully!"