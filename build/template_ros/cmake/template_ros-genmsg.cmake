# generated from genmsg/cmake/pkg-genmsg.cmake.em

message(STATUS "template_ros: 1 messages, 1 services")

set(MSG_I_FLAGS "-Itemplate_ros:/home/itx1/wip_ws/src/template_ros/msg;-Istd_msgs:/opt/ros/indigo/share/std_msgs/cmake/../msg")

# Find all generators
find_package(gencpp REQUIRED)
find_package(geneus REQUIRED)
find_package(genlisp REQUIRED)
find_package(genpy REQUIRED)

add_custom_target(template_ros_generate_messages ALL)

# verify that message/service dependencies have not changed since configure



get_filename_component(_filename "/home/itx1/wip_ws/src/template_ros/srv/AddTwoInts.srv" NAME_WE)
add_custom_target(_template_ros_generate_messages_check_deps_${_filename}
  COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENMSG_CHECK_DEPS_SCRIPT} "template_ros" "/home/itx1/wip_ws/src/template_ros/srv/AddTwoInts.srv" ""
)

get_filename_component(_filename "/home/itx1/wip_ws/src/template_ros/msg/Num.msg" NAME_WE)
add_custom_target(_template_ros_generate_messages_check_deps_${_filename}
  COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENMSG_CHECK_DEPS_SCRIPT} "template_ros" "/home/itx1/wip_ws/src/template_ros/msg/Num.msg" ""
)

#
#  langs = gencpp;geneus;genlisp;genpy
#

### Section generating for lang: gencpp
### Generating Messages
_generate_msg_cpp(template_ros
  "/home/itx1/wip_ws/src/template_ros/msg/Num.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/template_ros
)

### Generating Services
_generate_srv_cpp(template_ros
  "/home/itx1/wip_ws/src/template_ros/srv/AddTwoInts.srv"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/template_ros
)

### Generating Module File
_generate_module_cpp(template_ros
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/template_ros
  "${ALL_GEN_OUTPUT_FILES_cpp}"
)

add_custom_target(template_ros_generate_messages_cpp
  DEPENDS ${ALL_GEN_OUTPUT_FILES_cpp}
)
add_dependencies(template_ros_generate_messages template_ros_generate_messages_cpp)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/itx1/wip_ws/src/template_ros/srv/AddTwoInts.srv" NAME_WE)
add_dependencies(template_ros_generate_messages_cpp _template_ros_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/itx1/wip_ws/src/template_ros/msg/Num.msg" NAME_WE)
add_dependencies(template_ros_generate_messages_cpp _template_ros_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(template_ros_gencpp)
add_dependencies(template_ros_gencpp template_ros_generate_messages_cpp)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS template_ros_generate_messages_cpp)

### Section generating for lang: geneus
### Generating Messages
_generate_msg_eus(template_ros
  "/home/itx1/wip_ws/src/template_ros/msg/Num.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/template_ros
)

### Generating Services
_generate_srv_eus(template_ros
  "/home/itx1/wip_ws/src/template_ros/srv/AddTwoInts.srv"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/template_ros
)

### Generating Module File
_generate_module_eus(template_ros
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/template_ros
  "${ALL_GEN_OUTPUT_FILES_eus}"
)

add_custom_target(template_ros_generate_messages_eus
  DEPENDS ${ALL_GEN_OUTPUT_FILES_eus}
)
add_dependencies(template_ros_generate_messages template_ros_generate_messages_eus)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/itx1/wip_ws/src/template_ros/srv/AddTwoInts.srv" NAME_WE)
add_dependencies(template_ros_generate_messages_eus _template_ros_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/itx1/wip_ws/src/template_ros/msg/Num.msg" NAME_WE)
add_dependencies(template_ros_generate_messages_eus _template_ros_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(template_ros_geneus)
add_dependencies(template_ros_geneus template_ros_generate_messages_eus)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS template_ros_generate_messages_eus)

### Section generating for lang: genlisp
### Generating Messages
_generate_msg_lisp(template_ros
  "/home/itx1/wip_ws/src/template_ros/msg/Num.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/template_ros
)

### Generating Services
_generate_srv_lisp(template_ros
  "/home/itx1/wip_ws/src/template_ros/srv/AddTwoInts.srv"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/template_ros
)

### Generating Module File
_generate_module_lisp(template_ros
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/template_ros
  "${ALL_GEN_OUTPUT_FILES_lisp}"
)

add_custom_target(template_ros_generate_messages_lisp
  DEPENDS ${ALL_GEN_OUTPUT_FILES_lisp}
)
add_dependencies(template_ros_generate_messages template_ros_generate_messages_lisp)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/itx1/wip_ws/src/template_ros/srv/AddTwoInts.srv" NAME_WE)
add_dependencies(template_ros_generate_messages_lisp _template_ros_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/itx1/wip_ws/src/template_ros/msg/Num.msg" NAME_WE)
add_dependencies(template_ros_generate_messages_lisp _template_ros_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(template_ros_genlisp)
add_dependencies(template_ros_genlisp template_ros_generate_messages_lisp)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS template_ros_generate_messages_lisp)

### Section generating for lang: genpy
### Generating Messages
_generate_msg_py(template_ros
  "/home/itx1/wip_ws/src/template_ros/msg/Num.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/template_ros
)

### Generating Services
_generate_srv_py(template_ros
  "/home/itx1/wip_ws/src/template_ros/srv/AddTwoInts.srv"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/template_ros
)

### Generating Module File
_generate_module_py(template_ros
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/template_ros
  "${ALL_GEN_OUTPUT_FILES_py}"
)

add_custom_target(template_ros_generate_messages_py
  DEPENDS ${ALL_GEN_OUTPUT_FILES_py}
)
add_dependencies(template_ros_generate_messages template_ros_generate_messages_py)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/itx1/wip_ws/src/template_ros/srv/AddTwoInts.srv" NAME_WE)
add_dependencies(template_ros_generate_messages_py _template_ros_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/itx1/wip_ws/src/template_ros/msg/Num.msg" NAME_WE)
add_dependencies(template_ros_generate_messages_py _template_ros_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(template_ros_genpy)
add_dependencies(template_ros_genpy template_ros_generate_messages_py)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS template_ros_generate_messages_py)



if(gencpp_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/template_ros)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/template_ros
    DESTINATION ${gencpp_INSTALL_DIR}
  )
endif()
add_dependencies(template_ros_generate_messages_cpp std_msgs_generate_messages_cpp)

if(geneus_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/template_ros)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/template_ros
    DESTINATION ${geneus_INSTALL_DIR}
  )
endif()
add_dependencies(template_ros_generate_messages_eus std_msgs_generate_messages_eus)

if(genlisp_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/template_ros)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/template_ros
    DESTINATION ${genlisp_INSTALL_DIR}
  )
endif()
add_dependencies(template_ros_generate_messages_lisp std_msgs_generate_messages_lisp)

if(genpy_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/template_ros)
  install(CODE "execute_process(COMMAND \"/usr/bin/python\" -m compileall \"${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/template_ros\")")
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/template_ros
    DESTINATION ${genpy_INSTALL_DIR}
  )
endif()
add_dependencies(template_ros_generate_messages_py std_msgs_generate_messages_py)
