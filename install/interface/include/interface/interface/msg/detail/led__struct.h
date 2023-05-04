// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from interface:msg/Led.idl
// generated code does not contain a copyright notice

#ifndef INTERFACE__MSG__DETAIL__LED__STRUCT_H_
#define INTERFACE__MSG__DETAIL__LED__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

/// Struct defined in msg/Led in the package interface.
typedef struct interface__msg__Led
{
  bool led_1;
  bool led_2;
  bool led_3;
} interface__msg__Led;

// Struct for a sequence of interface__msg__Led.
typedef struct interface__msg__Led__Sequence
{
  interface__msg__Led * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} interface__msg__Led__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // INTERFACE__MSG__DETAIL__LED__STRUCT_H_
