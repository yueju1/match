// generated from rosidl_typesupport_introspection_c/resource/idl__type_support.c.em
// with input from interface:msg/Led.idl
// generated code does not contain a copyright notice

#include <stddef.h>
#include "interface/msg/detail/led__rosidl_typesupport_introspection_c.h"
#include "interface/msg/rosidl_typesupport_introspection_c__visibility_control.h"
#include "rosidl_typesupport_introspection_c/field_types.h"
#include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/message_introspection.h"
#include "interface/msg/detail/led__functions.h"
#include "interface/msg/detail/led__struct.h"


#ifdef __cplusplus
extern "C"
{
#endif

void interface__msg__Led__rosidl_typesupport_introspection_c__Led_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  interface__msg__Led__init(message_memory);
}

void interface__msg__Led__rosidl_typesupport_introspection_c__Led_fini_function(void * message_memory)
{
  interface__msg__Led__fini(message_memory);
}

static rosidl_typesupport_introspection_c__MessageMember interface__msg__Led__rosidl_typesupport_introspection_c__Led_message_member_array[3] = {
  {
    "led_1",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_BOOLEAN,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(interface__msg__Led, led_1),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "led_2",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_BOOLEAN,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(interface__msg__Led, led_2),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "led_3",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_BOOLEAN,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(interface__msg__Led, led_3),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers interface__msg__Led__rosidl_typesupport_introspection_c__Led_message_members = {
  "interface__msg",  // message namespace
  "Led",  // message name
  3,  // number of fields
  sizeof(interface__msg__Led),
  interface__msg__Led__rosidl_typesupport_introspection_c__Led_message_member_array,  // message members
  interface__msg__Led__rosidl_typesupport_introspection_c__Led_init_function,  // function to initialize message memory (memory has to be allocated)
  interface__msg__Led__rosidl_typesupport_introspection_c__Led_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t interface__msg__Led__rosidl_typesupport_introspection_c__Led_message_type_support_handle = {
  0,
  &interface__msg__Led__rosidl_typesupport_introspection_c__Led_message_members,
  get_message_typesupport_handle_function,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_interface
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, interface, msg, Led)() {
  if (!interface__msg__Led__rosidl_typesupport_introspection_c__Led_message_type_support_handle.typesupport_identifier) {
    interface__msg__Led__rosidl_typesupport_introspection_c__Led_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &interface__msg__Led__rosidl_typesupport_introspection_c__Led_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif
