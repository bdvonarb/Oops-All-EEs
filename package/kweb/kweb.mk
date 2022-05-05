################################################################################
#
# kweb
#
################################################################################

KWEB_VERSION = 1.7.0
KWEB_SITE = $(BR2_EXTERNAL_OOPSALLEES_PATH)/package/kweb
KWEB_SITE_METHOD = local
#KWEB_LICENSE = GPL-3.0+
#KWEB_LICENSE_FILES = COPYING
#KWEB_INSTALL_STAGING = YES
KWEB_INSTALL_TARGET = YES
#KWEB_CONFIG_SCRIPTS = libfoo-config
#KWEB_DEPENDENCIES = host-libaaa libbbb

define KWEB_BUILD_CMDS
    $(MAKE) $(TARGET_CONFIGURE_OPTS) -C $(@D) kweb3
endef
define KWEB_INSTALL_STAGING_CMDS
    
endef
define KWEB_INSTALL_TARGET_CMDS

endef

define KWEB_USERS
    
endef
define KWEB_DEVICES
    
endef
define KWEB_PERMISSIONS
    
endef

$(eval $(generic-package))