################################################################################
#
# Panel Device
#
################################################################################

PANELDEVICE_VERSION = 0.0.1
PANELDEVICE_SITE = $(BR2_EXTERNAL_OOPSALLEES_PATH)/package/paneldevice
PANELDEVICE_SITE_METHOD = local
#PANELDEVICE_LICENSE = GPL-3.0+
#PANELDEVICE_LICENSE_FILES = COPYING
#PANELDEVICE_INSTALL_STAGING = YES
PANELDEVICE_INSTALL_TARGET = YES
#PANELDEVICE_CONFIG_SCRIPTS = libfoo-config
#PANELDEVICE_DEPENDENCIES = host-libaaa libbbb

define PANELDEVICE_BUILD_CMDS
    $(MAKE) $(TARGET_CONFIGURE_OPTS) -C $(@D) all
endef

define PANELDEVICE_INSTALL_STAGING_CMDS
    
endef

define PANELDEVICE_INSTALL_TARGET_CMDS
    $(INSTALL) -D -m 0755 $(@D)/files/interfaces $(TARGET_DIR)/etc/network/
	$(INSTALL) -D -m 0755 $(@D)/files/wpa_supplicant.conf $(TARGET_DIR)/etc/
	$(INSTALL) -D -m 0755 $(@D)/scripts/S99initpanel $(TARGET_DIR)/etc/init.d/
	$(INSTALL) -D -m 0755 $(@D)/src/main.py $(TARGET_DIR)/root/
	$(INSTALL) -D -m 0755 $(@D)/bin/paneldevice $(TARGET_DIR)/root/
endef

define PANELDEVICE_USERS
    
endef

define PANELDEVICE_DEVICES
    
endef

define PANELDEVICE_PERMISSIONS
    
endef

$(eval $(generic-package))