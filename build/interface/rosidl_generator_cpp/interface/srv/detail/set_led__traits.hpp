// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from interface:srv/SetLed.idl
// generated code does not contain a copyright notice

#ifndef INTERFACE__SRV__DETAIL__SET_LED__TRAITS_HPP_
#define INTERFACE__SRV__DETAIL__SET_LED__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "interface/srv/detail/set_led__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

namespace interface
{

namespace srv
{

inline void to_flow_style_yaml(
  const SetLed_Request & msg,
  std::ostream & out)
{
  out << "{";
  // member: empty
  {
    out << "empty: ";
    rosidl_generator_traits::value_to_yaml(msg.empty, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const SetLed_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: empty
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "empty: ";
    rosidl_generator_traits::value_to_yaml(msg.empty, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const SetLed_Request & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace srv

}  // namespace interface

namespace rosidl_generator_traits
{

[[deprecated("use interface::srv::to_block_style_yaml() instead")]]
inline void to_yaml(
  const interface::srv::SetLed_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  interface::srv::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use interface::srv::to_yaml() instead")]]
inline std::string to_yaml(const interface::srv::SetLed_Request & msg)
{
  return interface::srv::to_yaml(msg);
}

template<>
inline const char * data_type<interface::srv::SetLed_Request>()
{
  return "interface::srv::SetLed_Request";
}

template<>
inline const char * name<interface::srv::SetLed_Request>()
{
  return "interface/srv/SetLed_Request";
}

template<>
struct has_fixed_size<interface::srv::SetLed_Request>
  : std::integral_constant<bool, true> {};

template<>
struct has_bounded_size<interface::srv::SetLed_Request>
  : std::integral_constant<bool, true> {};

template<>
struct is_message<interface::srv::SetLed_Request>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace interface
{

namespace srv
{

inline void to_flow_style_yaml(
  const SetLed_Response & msg,
  std::ostream & out)
{
  out << "{";
  // member: sucess
  {
    out << "sucess: ";
    rosidl_generator_traits::value_to_yaml(msg.sucess, out);
    out << ", ";
  }

  // member: led_3_state
  {
    out << "led_3_state: ";
    rosidl_generator_traits::value_to_yaml(msg.led_3_state, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const SetLed_Response & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: sucess
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "sucess: ";
    rosidl_generator_traits::value_to_yaml(msg.sucess, out);
    out << "\n";
  }

  // member: led_3_state
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "led_3_state: ";
    rosidl_generator_traits::value_to_yaml(msg.led_3_state, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const SetLed_Response & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace srv

}  // namespace interface

namespace rosidl_generator_traits
{

[[deprecated("use interface::srv::to_block_style_yaml() instead")]]
inline void to_yaml(
  const interface::srv::SetLed_Response & msg,
  std::ostream & out, size_t indentation = 0)
{
  interface::srv::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use interface::srv::to_yaml() instead")]]
inline std::string to_yaml(const interface::srv::SetLed_Response & msg)
{
  return interface::srv::to_yaml(msg);
}

template<>
inline const char * data_type<interface::srv::SetLed_Response>()
{
  return "interface::srv::SetLed_Response";
}

template<>
inline const char * name<interface::srv::SetLed_Response>()
{
  return "interface/srv/SetLed_Response";
}

template<>
struct has_fixed_size<interface::srv::SetLed_Response>
  : std::integral_constant<bool, true> {};

template<>
struct has_bounded_size<interface::srv::SetLed_Response>
  : std::integral_constant<bool, true> {};

template<>
struct is_message<interface::srv::SetLed_Response>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace rosidl_generator_traits
{

template<>
inline const char * data_type<interface::srv::SetLed>()
{
  return "interface::srv::SetLed";
}

template<>
inline const char * name<interface::srv::SetLed>()
{
  return "interface/srv/SetLed";
}

template<>
struct has_fixed_size<interface::srv::SetLed>
  : std::integral_constant<
    bool,
    has_fixed_size<interface::srv::SetLed_Request>::value &&
    has_fixed_size<interface::srv::SetLed_Response>::value
  >
{
};

template<>
struct has_bounded_size<interface::srv::SetLed>
  : std::integral_constant<
    bool,
    has_bounded_size<interface::srv::SetLed_Request>::value &&
    has_bounded_size<interface::srv::SetLed_Response>::value
  >
{
};

template<>
struct is_service<interface::srv::SetLed>
  : std::true_type
{
};

template<>
struct is_service_request<interface::srv::SetLed_Request>
  : std::true_type
{
};

template<>
struct is_service_response<interface::srv::SetLed_Response>
  : std::true_type
{
};

}  // namespace rosidl_generator_traits

#endif  // INTERFACE__SRV__DETAIL__SET_LED__TRAITS_HPP_
