# Install script for directory: /Users/erage/Desktop/lite-client

# Set the install prefix
if(NOT DEFINED CMAKE_INSTALL_PREFIX)
  set(CMAKE_INSTALL_PREFIX "/usr/local")
endif()
string(REGEX REPLACE "/$" "" CMAKE_INSTALL_PREFIX "${CMAKE_INSTALL_PREFIX}")

# Set the install configuration name.
if(NOT DEFINED CMAKE_INSTALL_CONFIG_NAME)
  if(BUILD_TYPE)
    string(REGEX REPLACE "^[^A-Za-z0-9_]+" ""
           CMAKE_INSTALL_CONFIG_NAME "${BUILD_TYPE}")
  else()
    set(CMAKE_INSTALL_CONFIG_NAME "")
  endif()
  message(STATUS "Install configuration: \"${CMAKE_INSTALL_CONFIG_NAME}\"")
endif()

# Set the component getting installed.
if(NOT CMAKE_INSTALL_COMPONENT)
  if(COMPONENT)
    message(STATUS "Install component: \"${COMPONENT}\"")
    set(CMAKE_INSTALL_COMPONENT "${COMPONENT}")
  else()
    set(CMAKE_INSTALL_COMPONENT)
  endif()
endif()

# Is this installation the result of a crosscompile?
if(NOT DEFINED CMAKE_CROSSCOMPILING)
  set(CMAKE_CROSSCOMPILING "FALSE")
endif()

if(NOT CMAKE_INSTALL_LOCAL_ONLY)
  # Include the install script for each subdirectory.
  include("/Users/erage/Desktop/liteclient-build/tdutils/cmake_install.cmake")
  include("/Users/erage/Desktop/liteclient-build/memprof/cmake_install.cmake")
  include("/Users/erage/Desktop/liteclient-build/tdactor/cmake_install.cmake")
  include("/Users/erage/Desktop/liteclient-build/tdnet/cmake_install.cmake")
  include("/Users/erage/Desktop/liteclient-build/tddb/cmake_install.cmake")
  include("/Users/erage/Desktop/liteclient-build/tdtl/cmake_install.cmake")
  include("/Users/erage/Desktop/liteclient-build/tl/cmake_install.cmake")
  include("/Users/erage/Desktop/liteclient-build/terminal/cmake_install.cmake")
  include("/Users/erage/Desktop/liteclient-build/keys/cmake_install.cmake")
  include("/Users/erage/Desktop/liteclient-build/tl-utils/cmake_install.cmake")
  include("/Users/erage/Desktop/liteclient-build/adnl/cmake_install.cmake")
  include("/Users/erage/Desktop/liteclient-build/crypto/cmake_install.cmake")
  include("/Users/erage/Desktop/liteclient-build/lite-client/cmake_install.cmake")

endif()

if(CMAKE_INSTALL_COMPONENT)
  set(CMAKE_INSTALL_MANIFEST "install_manifest_${CMAKE_INSTALL_COMPONENT}.txt")
else()
  set(CMAKE_INSTALL_MANIFEST "install_manifest.txt")
endif()

string(REPLACE ";" "\n" CMAKE_INSTALL_MANIFEST_CONTENT
       "${CMAKE_INSTALL_MANIFEST_FILES}")
file(WRITE "/Users/erage/Desktop/liteclient-build/${CMAKE_INSTALL_MANIFEST}"
     "${CMAKE_INSTALL_MANIFEST_CONTENT}")
