// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from interface:msg/Led.idl
// generated code does not contain a copyright notice

#ifndef INTERFACE__MSG__DETAIL__LED__STRUCT_HPP_
#define INTERFACE__MSG__DETAIL__LED__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


#ifndef _WIN32
# define DEPRECATED__interface__msg__Led __attribute__((deprecated))
#else
# define DEPRECATED__interface__msg__Led __declspec(deprecated)
#endif

namespace interface
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct Led_
{
  using Type = Led_<ContainerAllocator>;

  explicit Led_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->led_1 = false;
      this->led_2 = false;
      this->led_3 = false;
    }
  }

  explicit Led_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    (void)_alloc;
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->led_1 = false;
      this->led_2 = false;
      this->led_3 = false;
    }
  }

  // field types and members
  using _led_1_type =
    bool;
  _led_1_type led_1;
  using _led_2_type =
    bool;
  _led_2_type led_2;
  using _led_3_type =
    bool;
  _led_3_type led_3;

  // setters for named parameter idiom
  Type & set__led_1(
    const bool & _arg)
  {
    this->led_1 = _arg;
    return *this;
  }
  Type & set__led_2(
    const bool & _arg)
  {
    this->led_2 = _arg;
    return *this;
  }
  Type & set__led_3(
    const bool & _arg)
  {
    this->led_3 = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    interface::msg::Led_<ContainerAllocator> *;
  using ConstRawPtr =
    const interface::msg::Led_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<interface::msg::Led_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<interface::msg::Led_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      interface::msg::Led_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<interface::msg::Led_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      interface::msg::Led_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<interface::msg::Led_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<interface::msg::Led_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<interface::msg::Led_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__interface__msg__Led
    std::shared_ptr<interface::msg::Led_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__interface__msg__Led
    std::shared_ptr<interface::msg::Led_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const Led_ & other) const
  {
    if (this->led_1 != other.led_1) {
      return false;
    }
    if (this->led_2 != other.led_2) {
      return false;
    }
    if (this->led_3 != other.led_3) {
      return false;
    }
    return true;
  }
  bool operator!=(const Led_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct Led_

// alias to use template instance with default allocator
using Led =
  interface::msg::Led_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace interface

#endif  // INTERFACE__MSG__DETAIL__LED__STRUCT_HPP_
