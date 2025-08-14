DEBFILE=rel-minifi-cpp-0.15.0.deb
if test -f /opt/visagir/debs/$DEBFILE ; then
  dpkg -i /opt/visagir/debs/$DEBFILE && apt install -f \
  ; else

  wget https://github.com/apache/nifi-minifi-cpp/archive/refs/tags/rel/minifi-cpp-0.15.0.zip

  unzip minifi-cpp-0.15.0.zip

  pushd nifi-minifi-cpp-rel-minifi-cpp-0.15.0
  mkdir build
  pushd build
  # prometheus requires compiler with native atomic support
  # cmake .. -DENABLE_PROMETHEUS=OFF
  cmake ..
  make -j$(nproc)

  # create binary assembly
  make package -j $(nproc)

  # create source assembly 
  # make package_source

  popd # nifi-minifi-cpp-rel-minifi-cpp-0.15.0

fi
