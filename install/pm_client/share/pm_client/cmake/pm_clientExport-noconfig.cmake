#----------------------------------------------------------------
# Generated CMake target import file.
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "pm_client::pm_client" for configuration ""
set_property(TARGET pm_client::pm_client APPEND PROPERTY IMPORTED_CONFIGURATIONS NOCONFIG)
set_target_properties(pm_client::pm_client PROPERTIES
  IMPORTED_LINK_INTERFACE_LANGUAGES_NOCONFIG "CXX"
  IMPORTED_LOCATION_NOCONFIG "${_IMPORT_PREFIX}/lib/libpm_client.a"
  )

list(APPEND _IMPORT_CHECK_TARGETS pm_client::pm_client )
list(APPEND _IMPORT_CHECK_FILES_FOR_pm_client::pm_client "${_IMPORT_PREFIX}/lib/libpm_client.a" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
