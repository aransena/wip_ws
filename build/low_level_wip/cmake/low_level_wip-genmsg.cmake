# generated from genmsg/cmake/pkg-genmsg.cmake.em

message(WARNING "Invoking generate_messages() without having added any message or service file before.
You should either add add_message_files() and/or add_service_files() calls or remove the invocation of generate_messages().")
message(STATUS "low_level_wip: 0 messages, 0 services")

set(MSG_I_FLAGS "-Igeometry_msgs:/opt/ros/indigo/share/geometry_msgs/cmake/../msg;-Inav_msgs:/opt/ros/indigo/share/nav_msgs/cmake/../msg;-Istd_msgs:/opt/ros/indigo/share/std_msgs/cmake/../msg;-Itf:/opt/ros/indigo/share/tf/cmake/../msg;-Iactionlib_msgs:/opt/ros/indigo/share/actionlib_msgs/cmake/../msg;-Isensor_msgs:/opt/ros/indigo/share/sensor_msgs/cmake/../msg")

# Find all generators
find_package(gencpp REQUIRED)
find_package(geneus REQUIRED)
find_package(genlisp REQUIRED)
find_package(genpy REQUIRED)

add_custom_target(low_level_wip_generate_messages ALL)

# verify that message/service dependencies have not changed since configure



#
#  langs = gencpp;geneus;genlisp;genpy
#

### Section generating for lang: gencpp
### Generating Messages

### Generating Services

### Generating Module File
_generate_module_cpp(low_level_wip
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/low_level_wip
  "${ALL_GEN_OUTPUT_FILES_cpp}"
)

add_custom_target(low_level_wip_generate_messages_cpp
  DEPENDS ${ALL_GEN_OUTPUT_FILES_cpp}
)
add_dependencies(low_level_wip_generate_messages low_level_wip_generate_messages_cpp)

# add dependencies to all check dependencies targets

# target for backward compatibility
add_custom_target(low_level_wip_gencpp)
add_dependencies(low_level_wip_gencpp low_level_wip_generate_messages_cpp)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS low_level_wip_generate_messages_cpp)

### Section generating for lang: geneus
### Generating Messages

### Generating Services

### Generating Module File
_generate_module_eus(low_level_wip
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/low_level_wip
  "${ALL_GEN_OUTPUT_FILES_eus}"
)

add_custom_target(low_level_wip_generate_messages_eus
  DEPENDS ${ALL_GEN_OUTPUT_FILES_eus}
)
add_dependencies(low_level_wip_generate_messages low_level_wip_generate_messages_eus)

# add dependencies to all check dependencies targets

# target for backward compatibility
add_custom_target(low_level_wip_geneus)
add_dependencies(low_level_wip_geneus low_level_wip_generate_messages_eus)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS low_level_wip_generate_messages_eus)

### Section generating for lang: genlisp
### Generating Messages

### Generating Services

### Generating Module File
_generate_module_lisp(low_level_wip
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/low_level_wip
  "${ALL_GEN_OUTPUT_FILES_lisp}"
)

add_custom_target(low_level_wip_generate_messages_lisp
  DEPENDS ${ALL_GEN_OUTPUT_FILES_lisp}
)
add_dependencies(low_level_wip_generate_messages low_level_wip_generate_messages_lisp)

# add dependencies to all check dependencies targets

# target for backward compatibility
add_custom_target(low_level_wip_genlisp)
add_dependencies(low_level_wip_genlisp low_level_wip_generate_messages_lisp)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS low_level_wip_generate_messages_lisp)

### Section generating for lang: genpy
### Generating Messages

### Generating Services

### Generating Module File
_generate_module_py(low_level_wip
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/low_level_wip
  "${ALL_GEN_OUTPUT_FILES_py}"
)

add_custom_target(low_level_wip_generate_messages_py
  DEPENDS ${ALL_GEN_OUTPUT_FILES_py}
)
add_dependencies(low_level_wip_generate_messages low_level_wip_generate_messages_py)

# add dependencies to all check dependencies targets

# target for backward compatibility
add_custom_target(low_level_wip_genpy)
add_dependencies(low_level_wip_genpy low_level_wip_generate_messages_py)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS low_level_wip_generate_messages_py)



if(gencpp_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/low_level_wip)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/low_level_wip
    DESTINATION ${gencpp_INSTALL_DIR}
  )
endif()
add_dependencies(low_level_wip_generate_messages_cpp geometry_msgs_generate_messages_cpp)
add_dependencies(low_level_wip_generate_messages_cpp nav_msgs_generate_messages_cpp)
add_dependencies(low_level_wip_generate_messages_cpp std_msgs_generate_messages_cpp)
add_dependencies(low_level_wip_generate_messages_cpp tf_generate_messages_cpp)

if(geneus_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/low_level_wip)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/low_level_wip
    DESTINATION ${geneus_INSTALL_DIR}
  )
endif()
add_dependencies(low_level_wip_generate_messages_eus geometry_msgs_generate_messages_eus)
add_dependencies(low_level_wip_generate_messages_eus nav_msgs_generate_messages_eus)
add_dependencies(low_level_wip_generate_messages_eus std_msgs_generate_messages_eus)
add_dependencies(low_level_wip_generate_messages_eus tf_generate_messages_eus)

if(genlisp_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/low_level_wip)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/low_level_wip
    DESTINATION ${genlisp_INSTALL_DIR}
  )
endif()
add_dependencies(low_level_wip_generate_messages_lisp geometry_msgs_generate_messages_lisp)
add_dependencies(low_level_wip_generate_messages_lisp nav_msgs_generate_messages_lisp)
add_dependencies(low_level_wip_generate_messages_lisp std_msgs_generate_messages_lisp)
add_dependencies(low_level_wip_generate_messages_lisp tf_generate_messages_lisp)

if(genpy_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/low_level_wip)
  install(CODE "execute_process(COMMAND \"/usr/bin/python\" -m compileall \"${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/low_level_wip\")")
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/low_level_wip
    DESTINATION ${genpy_INSTALL_DIR}
  )
endif()
add_dependencies(low_level_wip_generate_messages_py geometry_msgs_generate_messages_py)
add_dependencies(low_level_wip_generate_messages_py nav_msgs_generate_messages_py)
add_dependencies(low_level_wip_generate_messages_py std_msgs_generate_messages_py)
add_dependencies(low_level_wip_generate_messages_py tf_generate_messages_py)
