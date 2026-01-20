# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['codex_gui.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=['codex_ia', 'codex_ia.neural_link', 'codex_ia.core'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='CodexIA_Triad',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    version='C:\\Users\\Mauricio\\AppData\\Local\\Temp\\e63ae109-2ae3-4811-a09b-a225c6946554',
)
