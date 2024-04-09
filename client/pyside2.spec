# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['pyside2.py'],
    pathex=['D:\\Anaconda3\\anaconda\\envs\\py38\\Lib\\site-packages', 'main_ui.py'],
    binaries=[],
    datas=[],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [('D:\\Anaconda3\\anaconda\\envs\\py38\\python.exe', None, 'OPTION')],
    name='pyside2',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
