import platform, subprocess, sys
PS = r'''
\$k = "Registry::HKEY_CLASSES_ROOT\\CLSID\\{0823B6F8-F499-4d5e-B885-EA9CB4F43B24}"
New-Item -Path \$k -Force | Out-Null
Set-ItemProperty -Path \$k -Name "(default)" -Value "Broken COM Object"
Set-ItemProperty -Path \$k -Name "AppID" -Value "{00000000-0000-0000-0000-000000000000}"
New-Item -Path (\$k + "\\LocalServer32") -Force | Out-Null
Set-ItemProperty -Path (\$k + "\\LocalServer32") -Name "(default)" -Value "C:\\Windows\\\\System32\\\\broken_tiworker.dll"
Write-Output "CLSID broken state ready"
'''
if platform.system() != 'Windows':
    print('SKIP: 需要真实 Windows')
    sys.exit(1)
r = subprocess.run(['powershell', '-NoProfile', '-ExecutionPolicy', 'Bypass', '-Command', PS], capture_output=True, text=True)
print(r.stdout, r.stderr)
sys.exit(0 if r.returncode == 0 else 1)
