################################################################################
#
# Browser
#
################################################################################

BROWSER_VERSION = 0.0.1
BROWSER_SITE = $(BR2_EXTERNAL_OOPSALLEES_PATH)/package/browser
BROWSER_SITE_METHOD = local
#BROWSER_LICENSE = GPL-3.0+
#BROWSER_LICENSE_FILES = COPYING
#BROWSER_INSTALL_STAGING = YES
BROWSER_INSTALL_TARGET = YES
#BROWSER_CONFIG_SCRIPTS = libfoo-config
#BROWSER_DEPENDENCIES = host-libaaa libbbb

define BROWSER_BUILD_CMDS
    $(MAKE) $(TARGET_CONFIGURE_OPTS) -C $(@D) all
endef
define BROWSER_INSTALL_STAGING_CMDS
    
endef
define BROWSER_INSTALL_TARGET_CMDS
    $(INSTALL) -D -m 0755 $(@D)/browser $(TARGET_DIR)/root/
endef

define BROWSER_USERS
    
endef
define BROWSER_DEVICES
    
endef
define BROWSER_PERMISSIONS
    
endef

$(eval $(generic-package))