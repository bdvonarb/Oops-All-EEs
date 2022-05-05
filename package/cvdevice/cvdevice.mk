################################################################################
#
# CV Device
#
################################################################################

CVDEVICE_VERSION = 0.0.1
CVDEVICE_SITE = $(BR2_EXTERNAL_OOPSALLEES_PATH)/package/cvdevice
CVDEVICE_SITE_METHOD = local
#CVDEVICE_LICENSE = GPL-3.0+
#CVDEVICE_LICENSE_FILES = COPYING
#CVDEVICE_INSTALL_STAGING = YES
CVDEVICE_INSTALL_TARGET = YES
#CVDEVICE_CONFIG_SCRIPTS = libfoo-config
#CVDEVICE_DEPENDENCIES = host-libaaa libbbb

define CVDEVICE_BUILD_CMDS
    $(MAKE) $(TARGET_CONFIGURE_OPTS) -C $(@D) all
endef
define CVDEVICE_INSTALL_STAGING_CMDS
    
endef
define CVDEVICE_INSTALL_TARGET_CMDS
    $(INSTALL) -D -m 0755 $(@D)/files/interfaces $(TARGET_DIR)/etc/network/
	$(INSTALL) -D -m 0755 $(@D)/files/wpa_supplicant.conf $(TARGET_DIR)/etc/
    $(INSTALL) -D -m 0755 $(@D)/scripts/S99startOAEE $(TARGET_DIR)/etc/init.d/
    $(INSTALL) -D -m 0755 $(@D)/files/80-movidius.rules $(TARGET_DIR)/etc/udev/rules.d/
    $(INSTALL) -d -m 0755 $(TARGET_DIR)/etc/X11/xorg.conf.d
    $(INSTALL) -D -m 0755 $(@D)/files/10-modules.conf $(TARGET_DIR)/etc/X11/xorg.conf.d/
    $(INSTALL) -D -m 0755 $(@D)/files/20-devices.conf $(TARGET_DIR)/etc/X11/xorg.conf.d/
    $(INSTALL) -D -m 0755 $(@D)/scripts/xinitrc $(TARGET_DIR)/etc/X11/xinit/
    $(INSTALL) -D -m 0755 $(@D)/src/main.py $(TARGET_DIR)/root/
    $(INSTALL) -D -m 0755 $(@D)/src/cv.py $(TARGET_DIR)/root/
    $(INSTALL) -D -m 0755 $(@D)/src/bt.py $(TARGET_DIR)/root/
    $(INSTALL) -D -m 0755 $(@D)/src/settings.py $(TARGET_DIR)/root/
    cp -r $(@D)/src/web/ $(TARGET_DIR)/root/
endef

define CVDEVICE_USERS
    
endef
define CVDEVICE_DEVICES
    
endef
define CVDEVICE_PERMISSIONS
    
endef

$(eval $(generic-package))