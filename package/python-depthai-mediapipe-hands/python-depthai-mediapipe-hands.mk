################################################################################
#
# python-depthai-mediapipe-hands
#
################################################################################

PYTHON_DEPTHAI_MEDIAPIPE_HANDS_VERSION = 0.0.1
PYTHON_DEPTHAI_MEDIAPIPE_HANDS_SITE = ${BR2_EXTERNAL_OOPSALLEES_PATH}/package/python-depthai-mediapipe-hands
PYTHON_DEPTHAI_MEDIAPIPE_HANDS_SITE_METHOD = local
PYTHON_DEPTHAI_MEDIAPIPE_HANDS_INSTALL_TARGET = YES

define PYTHON_DEPTHAI_MEDIAPIPE_HANDS_BUILD_CMDS

endef

define PYTHON_DEPTHAI_MEDIAPIPE_HANDS_INSTALL_STAGING_CMDS
    
endef

define PYTHON_DEPTHAI_MEDIAPIPE_HANDS_INSTALL_TARGET_CMDS
	$(INSTALL) -d -m 0755 $(TARGET_DIR)/root/handtracker
    $(INSTALL) -D -m 0755 $(@D)/src/*.py $(TARGET_DIR)/root/handtracker/
	$(INSTALL) -d -m 0755 $(TARGET_DIR)/root/handtracker/custom_models
	$(INSTALL) -D -m 0755 $(@D)/src/custom_models/convert_model.sh $(TARGET_DIR)/root/handtracker/custom_models/
	$(INSTALL) -D -m 0755 $(@D)/src/custom_models/generate_postproc_onnx.py $(TARGET_DIR)/root/handtracker/custom_models/
	$(INSTALL) -D -m 0755 $(@D)/src/custom_models/PDPostProcessing_top2_sh1.blob $(TARGET_DIR)/root/handtracker/custom_models/
	$(INSTALL) -d -m 0755 $(TARGET_DIR)/root/handtracker/models
	$(INSTALL) -D -m 0755 $(@D)/src/models/*.blob $(TARGET_DIR)/root/handtracker/models/
	$(INSTALL) -D -m 0755 $(@D)/src/models/*.sh $(TARGET_DIR)/root/handtracker/models/

endef

define PYTHON_DEPTHAI_MEDIAPIPE_HANDS_USERS
    
endef
define PYTHON_DEPTHAI_MEDIAPIPE_HANDS_DEVICES
    
endef
define PYTHON_DEPTHAI_MEDIAPIPE_HANDS_PERMISSIONS
    
endef

$(eval $(generic-package))