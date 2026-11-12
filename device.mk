#
# Copyright (C) 2022-2023 The LineageOS Project
#
# SPDX-License-Identifier: Apache-2.0
#

# Inherit from xiaomi sm8450-common
TARGET_HAS_UDFPS := true
$(call inherit-product, device/xiaomi/sm8450-common/common.mk)

# Inherit from the proprietary version
$(call inherit-product, vendor/xiaomi/zeus/zeus-vendor.mk)

# ADB: on from first boot without authorization, for devices without a
# working screen. init lifts its SafetyNet ro.debuggable/ro.adb.secure spoof
# and adds adb to the USB config when this is set.
PRODUCT_PRODUCT_PROPERTIES += \
    persist.sys.evox_debug_enabled=1

# Audio
PRODUCT_COPY_FILES += \
    $(LOCAL_PATH)/audio/mixer_paths_waipio_mtp.xml:$(TARGET_COPY_OUT_VENDOR)/etc/audio/sku_taro/mixer_paths_waipio_mtp.xml \
    $(LOCAL_PATH)/audio/resourcemanager_waipio_mtp.xml:$(TARGET_COPY_OUT_VENDOR)/etc/audio/sku_taro/resourcemanager_waipio_mtp.xml \
    $(LOCAL_PATH)/audio/usecaseKvManager.xml:$(TARGET_COPY_OUT_VENDOR)/etc/usecaseKvManager.xml

# Camera: torch strength through the camera service extension
$(call soong_config_set,libcameraservice,ext_lib,//device/xiaomi/zeus/camera:libcameraservice_extension.zeus)

# Display: DisplayDeviceConfig is looked up by the panel's display ID, which is
# ...257 (port 129) on 5.10 and ...258 (port 130, the stock name) on 6.6
PRODUCT_COPY_FILES += \
    vendor/xiaomi/zeus/proprietary/vendor/etc/displayconfig/display_id_4630947134992368257.xml:$(TARGET_COPY_OUT_VENDOR)/etc/displayconfig/display_id_4630947134992368258.xml

# Overlay
PRODUCT_PACKAGES += \
    ApertureResZeus \
    FrameworksResZeus \
    LineageResZeus \
    NfcResZeus \
    SettingsProviderResZeus \
    SettingsResZeus \
    SystemUIResZeus \
    WifiResZeus

# Powershare
PRODUCT_PACKAGES += \
    vendor.lineage.powershare-service.default

# Sensors
PRODUCT_COPY_FILES += \
    frameworks/native/data/etc/android.hardware.sensor.barometer.xml:$(TARGET_COPY_OUT_VENDOR)/etc/permissions/sku_taro/android.hardware.sensor.barometer.xml \
    frameworks/native/data/etc/android.hardware.sensor.hifi_sensors.xml:$(TARGET_COPY_OUT_VENDOR)/etc/permissions/sku_taro/android.hardware.sensor.hifi_sensors.xml

# Soong namespaces
PRODUCT_SOONG_NAMESPACES += \
    $(LOCAL_PATH)

# Miui Camera, when the tree has it
$(call inherit-product-if-exists, device/xiaomi/miuicamera-cupid/device.mk)
