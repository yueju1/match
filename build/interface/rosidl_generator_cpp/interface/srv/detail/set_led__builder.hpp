// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from interface:srv/SetLed.idl
// generated code does not contain a copyright notice

#ifndef INTERFACE__SRV__DETAIL__SET_LED__BUILDER_HPP_
#define INTERFACE__SRV__DETAIL__SET_LED__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "interface/srv/detail/set_led__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace interface
{

namespace srv
{

namespace builder
{

class Init_SetLed_Request_empty
{
public:
  Init_SetLed_Request_empty()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::interface::srv::SetLed_Request empty(::interface::srv::SetLed_Request::_empty_type arg)
  {
    msg_.empty = std::move(arg);
    return std::move(msg_);
  }

private:
  ::interface::srv::SetLed_Request msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::interface::srv::SetLed_Request>()
{
  return interface::srv::builder::Init_SetLed_Request_empty();
}

}  // namespace interface


namespace interface
{

namespace srv
{

namespace builder
{

class Init_SetLed_Response_led_3_state
{
public:
  explicit Init_SetLed_Response_led_3_state(::interface::srv::SetLed_Response & msg)
  : msg_(msg)
  {}
  ::interface::srv::SetLed_Response led_3_state(::interface::srv::SetLed_Response::_led_3_state_type arg)
  {
    msg_.led_3_state = std::move(arg);
    return std::move(msg_);
  }

private:
  ::interface::srv::SetLed_Response msg_;
};

class Init_SetLed_Response_sucess
{
public:
  Init_SetLed_Response_sucess()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_SetLed_Response_led_3_state sucess(::interface::srv::SetLed_Response::_sucess_type arg)
  {
    msg_.sucess = std::move(arg);
    return Init_SetLed_Response_led_3_state(msg_);
  }

private:
  ::interface::srv::SetLed_Response msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::interface::srv::SetLed_Response>()
{
  return interface::srv::builder::Init_SetLed_Response_sucess();
}

}  // namespace interface

#endif  // INTERFACE__SRV__DETAIL__SET_LED__BUILDER_HPP_
