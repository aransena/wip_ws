// Generated by gencpp from file tcd_fb2/String.msg
// DO NOT EDIT!


#ifndef TCD_FB2_MESSAGE_STRING_H
#define TCD_FB2_MESSAGE_STRING_H

#include <ros/service_traits.h>


#include <tcd_fb2/StringRequest.h>
#include <tcd_fb2/StringResponse.h>


namespace tcd_fb2
{

struct String
{

typedef StringRequest Request;
typedef StringResponse Response;
Request request;
Response response;

typedef Request RequestType;
typedef Response ResponseType;

}; // struct String
} // namespace tcd_fb2


namespace ros
{
namespace service_traits
{


template<>
struct MD5Sum< ::tcd_fb2::String > {
  static const char* value()
  {
    return "b8f71fbc3d8ee368e453fca947ab59d1";
  }

  static const char* value(const ::tcd_fb2::String&) { return value(); }
};

template<>
struct DataType< ::tcd_fb2::String > {
  static const char* value()
  {
    return "tcd_fb2/String";
  }

  static const char* value(const ::tcd_fb2::String&) { return value(); }
};


// service_traits::MD5Sum< ::tcd_fb2::StringRequest> should match 
// service_traits::MD5Sum< ::tcd_fb2::String > 
template<>
struct MD5Sum< ::tcd_fb2::StringRequest>
{
  static const char* value()
  {
    return MD5Sum< ::tcd_fb2::String >::value();
  }
  static const char* value(const ::tcd_fb2::StringRequest&)
  {
    return value();
  }
};

// service_traits::DataType< ::tcd_fb2::StringRequest> should match 
// service_traits::DataType< ::tcd_fb2::String > 
template<>
struct DataType< ::tcd_fb2::StringRequest>
{
  static const char* value()
  {
    return DataType< ::tcd_fb2::String >::value();
  }
  static const char* value(const ::tcd_fb2::StringRequest&)
  {
    return value();
  }
};

// service_traits::MD5Sum< ::tcd_fb2::StringResponse> should match 
// service_traits::MD5Sum< ::tcd_fb2::String > 
template<>
struct MD5Sum< ::tcd_fb2::StringResponse>
{
  static const char* value()
  {
    return MD5Sum< ::tcd_fb2::String >::value();
  }
  static const char* value(const ::tcd_fb2::StringResponse&)
  {
    return value();
  }
};

// service_traits::DataType< ::tcd_fb2::StringResponse> should match 
// service_traits::DataType< ::tcd_fb2::String > 
template<>
struct DataType< ::tcd_fb2::StringResponse>
{
  static const char* value()
  {
    return DataType< ::tcd_fb2::String >::value();
  }
  static const char* value(const ::tcd_fb2::StringResponse&)
  {
    return value();
  }
};

} // namespace service_traits
} // namespace ros

#endif // TCD_FB2_MESSAGE_STRING_H
