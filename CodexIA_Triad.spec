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
    version='C:\\Users\\Mauricio\\AppData\\Local\\Temp\\36a2448d-348f-41b1-be3f-73a70b27a257',
)
