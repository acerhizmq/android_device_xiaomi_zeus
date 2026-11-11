#!/usr/bin/env -S PYTHONPATH=../../../tools/extract-utils python3
#
# SPDX-FileCopyrightText: 2024 The LineageOS Project
# SPDX-License-Identifier: Apache-2.0
#

import os

from extract_utils.fixups_blob import (
    blob_fixup,
    blob_fixups_user_type,
)
from extract_utils.fixups_lib import (
    lib_fixups,
)
from extract_utils.main import (
    ExtractUtils,
    ExtractUtilsModule,
)
from extract_utils.tools import patchelf_version_path_map
from extract_utils.utils import run_cmd

# libTrueSight's GL/EGL imports, renamed to ts6_* and served by libtsegl6 from
# a private Adreno 0615.95 copy, see vendor/xiaomi/zeus/truesight615.
TS6_RENAME_MAP = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    '../../../vendor/xiaomi/zeus/truesight615/ts6_rename.map',
)


def rename_ts6_imports(ctx, file, file_path, *args, **kwargs):
    run_cmd(
        [
            patchelf_version_path_map['0_18'],
            '--rename-dynamic-symbols',
            TS6_RENAME_MAP,
            file_path,
        ]
    )


namespace_imports = [
    'device/xiaomi/sm8450-common',
    'hardware/qcom-caf/sm8450',
    'hardware/xiaomi',
    'vendor/qcom/opensource/commonsys-intf/display',
    'vendor/xiaomi/sm8450-common',
]

blob_fixups: blob_fixups_user_type = {
    'vendor/lib64/hw/camera.qcom.so': blob_fixup()
        .add_needed('libcamximageformatutils_shim.so')
        .binary_regex_replace(
            b'_ZN4CamX16ImageFormatUtils9GetFormatERNS_17GrallocPropertiesERNS_6FormatE',
            b'_ZN4CamX16ImageFormatUtils9GetXiaomiERNS_17GrallocPropertiesERNS_6FormatE',
        ),
    (
        'vendor/etc/camera/zeus_enhance_motiontuning.xml',
        'vendor/etc/camera/zeus_motiontuning.xml',
    ): blob_fixup().regex_replace('xml=version', 'xml version'),
    (
        'vendor/etc/camera/pureShot_parameter.xml',
        'vendor/etc/camera/pureView_parameter.xml',
    ): blob_fixup().regex_replace(r'=([0-9]+)>', r'="\1">'),
    (
        'vendor/lib64/hw/com.qti.chi.override.so',
        'vendor/lib64/libcamxcommonutils.so',
        'vendor/lib64/libmialgoengine.so',
    ): blob_fixup().add_needed('libprocessgroup_shim.so'),
    (
        'vendor/lib64/libTrueSight.so',
        'vendor/lib64/libmorpho_ubwc.so',
    ): blob_fixup()
    .clear_symbol_version('AHardwareBuffer_allocate')
    .clear_symbol_version('AHardwareBuffer_describe')
    .clear_symbol_version('AHardwareBuffer_isSupported')
    .clear_symbol_version('AHardwareBuffer_lock')
    .clear_symbol_version('AHardwareBuffer_lockPlanes')
    .clear_symbol_version('AHardwareBuffer_release')
    .clear_symbol_version('AHardwareBuffer_unlock'),
    'vendor/lib64/libTrueSight.so': blob_fixup()
    .call(rename_ts6_imports, need_tmp_dir=False)
    .add_needed('libtsegl6.so'),
    'vendor/lib64/libmialgo_pureShot.so': blob_fixup()
    .clear_symbol_version('remote_handle64_close')
    .clear_symbol_version('remote_handle64_invoke')
    .clear_symbol_version('remote_handle64_open')
    .clear_symbol_version('remote_register_buf_attr'),
}

module = ExtractUtilsModule(
    'zeus',
    'xiaomi',
    blob_fixups=blob_fixups,
    lib_fixups=lib_fixups,
    namespace_imports=namespace_imports,
    add_firmware_proprietary_file=True,
)

if __name__ == '__main__':
    utils = ExtractUtils.device_with_common(
        module, 'sm8450-common', module.vendor
    )
    utils.run()
