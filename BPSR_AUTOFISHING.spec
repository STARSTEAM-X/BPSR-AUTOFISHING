# -*- mode: python ; coding: utf-8 -*-

from PyInstaller.utils.win32.versioninfo import (
    VSVersionInfo,
    FixedFileInfo,
    StringFileInfo,
    StringTable,
    StringStruct,
    VarFileInfo,
    VarStruct
)

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[('img', 'img')],
    hiddenimports=[],
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
    name='BPSR_AUTOFISHING',
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
    icon='icon.ico',

    version=VSVersionInfo(
        ffi=FixedFileInfo(
            filevers=(1,0,0,0),
            prodvers=(1,0,0,0),
            mask=0x3f,
            flags=0x0,
            OS=0x40004,
            fileType=0x1,
            subtype=0x0,
            date=(0, 0)
        ),
        kids=[
            StringFileInfo([
                StringTable(
                    '040904B0',
                    [
                        StringStruct('CompanyName', 'STARSTEAM_X'),
                        StringStruct('FileDescription', 'BPSR Auto Fishing Bot'),
                        StringStruct('FileVersion', '1.0.0'),
                        StringStruct('InternalName', 'BPSR_AUTOFISHING'),
                        StringStruct('OriginalFilename', 'BPSR_AUTOFISHING.exe'),
                        StringStruct('ProductName', 'BPSR_AUTOFISHING'),
                        StringStruct('ProductVersion', '1.0.0'),
                        StringStruct('LegalCopyright', '© STARSTEAM_X'),
                    ]
                )
            ]),
            VarFileInfo([VarStruct('Translation', [1033, 1200])])
        ]
    )
)