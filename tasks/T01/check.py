import platform, subprocess, sys
PS = r'''
\$k = "Registry::HKEY_CLASSES_ROOT\\CLSID\\{0823B6F8-F499-4d5e-B885-EA9CB4F43B24}"
\$ok = \$true
\$item = Get-Item -Path \$k
if (\$item.GetValue("") -ne "Component Based Servicing Worker") { Write-Output "BAD default"; \$ok = \$false }
if (\$item.GetValue("AppID") -ne "{8D15A4F3-1BE5-4120-8A4D-2EF92A5DD58D}") { Write-Output "BAD AppID"; \$ok = \$false }
\$ls = Get-Item -Path (\$k + "\\LocalServer32") -ErrorAction SilentlyContinue
if (\$null -eq \$ls) { Write-Output "BAD no LocalServer32"; \$ok = \$false } else {
  \$v = \$ls.GetValue("")
  if (-not (\$v -like "C:\\Windows\\winsxs\\*TiWorker.exe")) { Write-Output "BAD LocalServer32: \$v"; \$ok = \$false }
}
if (\$ok) { Write-Output "PASS: CLSID 修复正确" } else { Write-Output "FAIL" }
'''
if platform.system() != 'Windows':
    print('SKIP: 需要真实 Windows')
    sys.exit(1)
r = subprocess.run(['powershell', '-NoProfile', '-ExecutionPolicy', 'Bypass', '-Command', PS], capture_output=True, text=True)
print(r.stdout, r.stderr)
sys.exit(0 if 'PASS' in r.stdout else 1)
