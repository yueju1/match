// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from interface:msg/Led.idl
// generated code does not contain a copyright notice

#ifndef INTERFACE__MSG__DETAIL__LED__BUILDER_HPP_
#define INTERFACE__MSG__DETAIL__LED__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "interface/msg/detail/led__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace interface
{

namespace msg
{

namespace builder
{

class Init_Led_led_3
{
public:
  explicit Init_Led_led_3(::interface::msg::Led & msg)
  : msg_(msg)
  {}
  ::interface::msg::Led led_3(::interface::msg::Led::_led_3_type arg)
  {
    msg_.led_3 = std::move(arg);
    return std::move(msg_);
  }

private:
  ::interface::msg::Led msg_;
};

class Init_Led_led_2
{
public:
  explicit Init_Led_led_2(::interface::msg::Led & msg)
  : msg_(msg)
  {}
  Init_Led_led_3 led_2(::interface::msg::Led::_led_2_type arg)
  {
    msg_.led_2 = std::move(arg);
    return Init_Led_led_3(msg_);
  }

private:
  ::interface::msg::Led msg_;
};

class Init_Led_led_1
{
public:
  Init_Led_led_1()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_Led_led_2 led_1(::interface::msg::Led::_led_1_type arg)
  {
    msg_.led_1 = std::move(arg);
    return Init_Led_led_2(msg_);
  }

private:
  ::interface::msg::Led msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::interface::msg::Led>()
{
  return interface::msg::builder::Init_Led_led_1();
}

}  // namespace interface

#endif  // INTERFACE__MSG__DETAIL__LED__BUILDER_HPP_
