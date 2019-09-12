# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 3.10

# Delete rule output on recipe failure.
.DELETE_ON_ERROR:


#=============================================================================
# Special targets provided by cmake.

# Disable implicit rules so canonical targets will work.
.SUFFIXES:


# Remove some rules from gmake that .SUFFIXES does not remove.
SUFFIXES =

.SUFFIXES: .hpux_make_needs_suffix_list


# Suppress display of executed commands.
$(VERBOSE).SILENT:


# A target that is always out of date.
cmake_force:

.PHONY : cmake_force

#=============================================================================
# Set environment variables for the build.

# The shell in which to execute make rules.
SHELL = /bin/sh

# The CMake executable.
CMAKE_COMMAND = /usr/bin/cmake

# The command to remove a file.
RM = /usr/bin/cmake -E remove -f

# Escaping for special characters.
EQUALS = =

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = /root/lite-client

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /root/liteclient-build

# Include any dependencies generated for this target.
include crypto/CMakeFiles/test-block.dir/depend.make

# Include the progress variables for this target.
include crypto/CMakeFiles/test-block.dir/progress.make

# Include the compile flags for this target's objects.
include crypto/CMakeFiles/test-block.dir/flags.make

crypto/CMakeFiles/test-block.dir/block/test-block.cpp.o: crypto/CMakeFiles/test-block.dir/flags.make
crypto/CMakeFiles/test-block.dir/block/test-block.cpp.o: /root/lite-client/crypto/block/test-block.cpp
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/root/liteclient-build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building CXX object crypto/CMakeFiles/test-block.dir/block/test-block.cpp.o"
	cd /root/liteclient-build/crypto && /usr/bin/c++  $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -o CMakeFiles/test-block.dir/block/test-block.cpp.o -c /root/lite-client/crypto/block/test-block.cpp

crypto/CMakeFiles/test-block.dir/block/test-block.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/test-block.dir/block/test-block.cpp.i"
	cd /root/liteclient-build/crypto && /usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /root/lite-client/crypto/block/test-block.cpp > CMakeFiles/test-block.dir/block/test-block.cpp.i

crypto/CMakeFiles/test-block.dir/block/test-block.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/test-block.dir/block/test-block.cpp.s"
	cd /root/liteclient-build/crypto && /usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /root/lite-client/crypto/block/test-block.cpp -o CMakeFiles/test-block.dir/block/test-block.cpp.s

crypto/CMakeFiles/test-block.dir/block/test-block.cpp.o.requires:

.PHONY : crypto/CMakeFiles/test-block.dir/block/test-block.cpp.o.requires

crypto/CMakeFiles/test-block.dir/block/test-block.cpp.o.provides: crypto/CMakeFiles/test-block.dir/block/test-block.cpp.o.requires
	$(MAKE) -f crypto/CMakeFiles/test-block.dir/build.make crypto/CMakeFiles/test-block.dir/block/test-block.cpp.o.provides.build
.PHONY : crypto/CMakeFiles/test-block.dir/block/test-block.cpp.o.provides

crypto/CMakeFiles/test-block.dir/block/test-block.cpp.o.provides.build: crypto/CMakeFiles/test-block.dir/block/test-block.cpp.o


# Object files for target test-block
test__block_OBJECTS = \
"CMakeFiles/test-block.dir/block/test-block.cpp.o"

# External object files for target test-block
test__block_EXTERNAL_OBJECTS =

crypto/test-block: crypto/CMakeFiles/test-block.dir/block/test-block.cpp.o
crypto/test-block: crypto/CMakeFiles/test-block.dir/build.make
crypto/test-block: crypto/libton_crypto.a
crypto/test-block: crypto/libfift.a
crypto/test-block: crypto/libton_block.a
crypto/test-block: tl/libtl_api.a
crypto/test-block: crypto/libton_db.a
crypto/test-block: crypto/libton_crypto.a
crypto/test-block: tddb/libtddb.a
crypto/test-block: tdactor/libtdactor.a
crypto/test-block: tdutils/libtdutils.a
crypto/test-block: /usr/lib/x86_64-linux-gnu/libcrypto.so
crypto/test-block: /usr/lib/x86_64-linux-gnu/libz.so
crypto/test-block: third-party/crc32c/libcrc32c.a
crypto/test-block: crypto/CMakeFiles/test-block.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir=/root/liteclient-build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Linking CXX executable test-block"
	cd /root/liteclient-build/crypto && $(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/test-block.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
crypto/CMakeFiles/test-block.dir/build: crypto/test-block

.PHONY : crypto/CMakeFiles/test-block.dir/build

crypto/CMakeFiles/test-block.dir/requires: crypto/CMakeFiles/test-block.dir/block/test-block.cpp.o.requires

.PHONY : crypto/CMakeFiles/test-block.dir/requires

crypto/CMakeFiles/test-block.dir/clean:
	cd /root/liteclient-build/crypto && $(CMAKE_COMMAND) -P CMakeFiles/test-block.dir/cmake_clean.cmake
.PHONY : crypto/CMakeFiles/test-block.dir/clean

crypto/CMakeFiles/test-block.dir/depend:
	cd /root/liteclient-build && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /root/lite-client /root/lite-client/crypto /root/liteclient-build /root/liteclient-build/crypto /root/liteclient-build/crypto/CMakeFiles/test-block.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : crypto/CMakeFiles/test-block.dir/depend
