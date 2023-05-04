// generated from rosidl_generator_py/resource/_idl_support.c.em
// with input from interface:msg/Led.idl
// generated code does not contain a copyright notice
#define NPY_NO_DEPRECATED_API NPY_1_7_API_VERSION
#include <Python.h>
#include <stdbool.h>
#ifndef _WIN32
# pragma GCC diagnostic push
# pragma GCC diagnostic ignored "-Wunused-function"
#endif
#include "numpy/ndarrayobject.h"
#ifndef _WIN32
# pragma GCC diagnostic pop
#endif
#include "rosidl_runtime_c/visibility_control.h"
#include "interface/msg/detail/led__struct.h"
#include "interface/msg/detail/led__functions.h"


ROSIDL_GENERATOR_C_EXPORT
bool interface__msg__led__convert_from_py(PyObject * _pymsg, void * _ros_message)
{
  // check that the passed message is of the expected Python class
  {
    char full_classname_dest[23];
    {
      char * class_name = NULL;
      char * module_name = NULL;
      {
        PyObject * class_attr = PyObject_GetAttrString(_pymsg, "__class__");
        if (class_attr) {
          PyObject * name_attr = PyObject_GetAttrString(class_attr, "__name__");
          if (name_attr) {
            class_name = (char *)PyUnicode_1BYTE_DATA(name_attr);
            Py_DECREF(name_attr);
          }
          PyObject * module_attr = PyObject_GetAttrString(class_attr, "__module__");
          if (module_attr) {
            module_name = (char *)PyUnicode_1BYTE_DATA(module_attr);
            Py_DECREF(module_attr);
          }
          Py_DECREF(class_attr);
        }
      }
      if (!class_name || !module_name) {
        return false;
      }
      snprintf(full_classname_dest, sizeof(full_classname_dest), "%s.%s", module_name, class_name);
    }
    assert(strncmp("interface.msg._led.Led", full_classname_dest, 22) == 0);
  }
  interface__msg__Led * ros_message = _ros_message;
  {  // led_1
    PyObject * field = PyObject_GetAttrString(_pymsg, "led_1");
    if (!field) {
      return false;
    }
    assert(PyBool_Check(field));
    ros_message->led_1 = (Py_True == field);
    Py_DECREF(field);
  }
  {  // led_2
    PyObject * field = PyObject_GetAttrString(_pymsg, "led_2");
    if (!field) {
      return false;
    }
    assert(PyBool_Check(field));
    ros_message->led_2 = (Py_True == field);
    Py_DECREF(field);
  }
  {  // led_3
    PyObject * field = PyObject_GetAttrString(_pymsg, "led_3");
    if (!field) {
      return false;
    }
    assert(PyBool_Check(field));
    ros_message->led_3 = (Py_True == field);
    Py_DECREF(field);
  }

  return true;
}

ROSIDL_GENERATOR_C_EXPORT
PyObject * interface__msg__led__convert_to_py(void * raw_ros_message)
{
  /* NOTE(esteve): Call constructor of Led */
  PyObject * _pymessage = NULL;
  {
    PyObject * pymessage_module = PyImport_ImportModule("interface.msg._led");
    assert(pymessage_module);
    PyObject * pymessage_class = PyObject_GetAttrString(pymessage_module, "Led");
    assert(pymessage_class);
    Py_DECREF(pymessage_module);
    _pymessage = PyObject_CallObject(pymessage_class, NULL);
    Py_DECREF(pymessage_class);
    if (!_pymessage) {
      return NULL;
    }
  }
  interface__msg__Led * ros_message = (interface__msg__Led *)raw_ros_message;
  {  // led_1
    PyObject * field = NULL;
    field = PyBool_FromLong(ros_message->led_1 ? 1 : 0);
    {
      int rc = PyObject_SetAttrString(_pymessage, "led_1", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // led_2
    PyObject * field = NULL;
    field = PyBool_FromLong(ros_message->led_2 ? 1 : 0);
    {
      int rc = PyObject_SetAttrString(_pymessage, "led_2", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // led_3
    PyObject * field = NULL;
    field = PyBool_FromLong(ros_message->led_3 ? 1 : 0);
    {
      int rc = PyObject_SetAttrString(_pymessage, "led_3", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }

  // ownership of _pymessage is transferred to the caller
  return _pymessage;
}
