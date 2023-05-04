// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from interface:msg/Led.idl
// generated code does not contain a copyright notice

#ifndef INTERFACE__MSG__DETAIL__LED__TRAITS_HPP_
#define INTERFACE__MSG__DETAIL__LED__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "interface/msg/detail/led__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

namespace interface
{

namespace msg
{

inline void to_flow_style_yaml(
  const Led & msg,
  std::ostream & out)
{
  out << "{";
  // member: led_1
  {
    out << "led_1: ";
    rosidl_generator_traits::value_to_yaml(msg.led_1, out);
    out << ", ";
  }

  // member: led_2
  {
    out << "led_2: ";
    rosidl_generator_traits::value_to_yaml(msg.led_2, out);
    out << ", ";
  }

  // member: led_3
  {
    out << "led_3: ";
    rosidl_generator_traits::value_to_yaml(msg.led_3, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const Led & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: led_1
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "led_1: ";
    rosidl_generator_traits::value_to_yaml(msg.led_1, out);
    out << "\n";
  }

  // member: led_2
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "led_2: ";
    rosidl_generator_traits::value_to_yaml(msg.led_2, out);
    out << "\n";
  }

  // member: led_3
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "led_3: ";
    rosidl_generator_traits::value_to_yaml(msg.led_3, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const Led & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace msg

}  // namespace interface

namespace rosidl_generator_traits
{

[[deprecated("use interface::msg::to_block_style_yaml() instead")]]
inline void to_yaml(
  const interface::msg::Led & msg,
  std::ostream & out, size_t indentation = 0)
{
  interface::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use interface::msg::to_yaml() instead")]]
inline std::string to_yaml(const interface::msg::Led & msg)
{
  return interface::msg::to_yaml(msg);
}

template<>
inline const char * data_type<interface::msg::Led>()
{
  return "interface::msg::Led";
}

template<>
inline const char * name<interface::msg::Led>()
{
  return "interface/msg/Led";
}

template<>
struct has_fixed_size<interface::msg::Led>
  : std::integral_constant<bool, true> {};

template<>
struct has_bounded_size<interface::msg::Led>
  : std::integral_constant<bool, true> {};

template<>
struct is_message<interface::msg::Led>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // INTERFACE__MSG__DETAIL__LED__TRAITS_HPP_
