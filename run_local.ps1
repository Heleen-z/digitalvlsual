$ErrorActionPreference = "Stop"

$Python = "python"
$Node = "node"

$BundledPython = "C:\Users\HBZuo\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe"
$BundledNode = "C:\Users\HBZuo\.cache\codex-runtimes\codex-primary-runtime\dependencies\node\bin\node.exe"
$BundledNodeModules = "C:\Users\HBZuo\.cache\codex-runtimes\codex-primary-runtime\dependencies\node\node_modules"

if (Test-Path $BundledPython) {
  $Python = $BundledPython
}

if (Test-Path $BundledNode) {
  $Node = $BundledNode
}

if (Test-Path $BundledNodeModules) {
  $env:NODE_PATH = $BundledNodeModules
}

Write-Host "1/4 生成教学样例数据..."
& $Python "scripts/generate_sample_data.py"

Write-Host "2/4 清洗数据并生成中文可视化图片..."
& $Python "scripts/process_and_visualize.py"

Write-Host "3/4 生成中文课堂展示 PPT..."
& $Node "presentation/build_ppt.js"

Write-Host "4/4 启动本地服务：http://localhost:8000/dashboard/"
& $Python -m http.server 8000

