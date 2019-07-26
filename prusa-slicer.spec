# Currently all of the test suite requires the old Perl infrastructure to run.
%bcond_without perltests

Name:           prusa-slicer
Version:        2.0.0
Release:        4%{?dist}
Summary:        3D printing slicer optimized for Prusa printers

# The main PrusaSlicer code and resources are AGPLv3, with small parts as
# Boost.  but it includes some bundled libraries under varying licenses which
# are statically linked into the main executable.  The full list would be:
# "AGPLv3 and CC-BY and GPLv2+ and (Copyright only or BSD) and Boost and
# MPLv2.0 and MIT and Unlicense and zlib and Qhull" (with Unlicense removed in
# F31) but the AGPLv3 dominates in the final executable.
# Technically the appdata.xml file is 0BSD but it seems quite pointless to list
# that here.
License:        AGPLv3
URL:            https://github.com/prusa3d/PrusaSlicer/
Source0:        https://github.com/prusa3d/PrusaSlicer/archive/version_2.0.0.tar.gz

Source1:        %name.desktop
Source2:        %name.appdata.xml

# A single test suite fails, but only on aarch64 and s390x, due to floating
# point rouding issues.   This patch adds small epsilon (4e-15) to one
# comparison to work around this.
# We will conditionally apply this so it's a source file, not a patch.
# https://github.com/prusa3d/PrusaSlicer/issues/2461
Source10:       patch-testsuite-epsilon

# Fix an improper include of expat.h
# https://github.com/prusa3d/PrusaSlicer/pull/2315
Patch0:         patch-expat-includes

# Fix improper qhull include locations
# https://github.com/prusa3d/PrusaSlicer/pull/2319
Patch1:         patch-qhull-includes

# Fix a number of failing unit tests
# https://github.com/prusa3d/PrusaSlicer/issues/2288
Patch10:        https://github.com/prusa3d/PrusaSlicer/commit/07282eb24d027817b4279f59ebbf0d80bac5f950.patch

# These patches are pulled from upstream's Debian packaging, and were cherry picked from post-release commits.
# I (JT) have not personally seen the bugs these fix but upstream asked that they be included.
Patch20:        https://raw.githubusercontent.com/prusa3d/PrusaSlicer/debian/debian/patches/fix-gizmo-icon-size.patch
Patch21:        https://raw.githubusercontent.com/prusa3d/PrusaSlicer/debian/debian/patches/handle-wx-assert-with-boost.patch
Patch22:        https://raw.githubusercontent.com/prusa3d/PrusaSlicer/debian/debian/patches/mode-switching-fix.patch

BuildRequires:  boost-devel
BuildRequires:  cmake
BuildRequires:  curl-devel
BuildRequires:  desktop-file-utils
BuildRequires:  eigen3-devel
BuildRequires:  expat-devel
BuildRequires:  gcc-c++
BuildRequires:  gettext
BuildRequires:  git-core
BuildRequires:  glew-devel
BuildRequires:  gtest-devel
BuildRequires:  ImageMagick
BuildRequires:  miniz-devel
BuildRequires:  NLopt-devel
BuildRequires:  tbb-devel
BuildRequires:  wxBase3-devel
BuildRequires:  wxGTK3-devel

# Upstream says this is obsolete, but still needed to compile
BuildRequires:  poly2tri-devel

# Things we wish we could unbundle
#BuildRequires:  admesh-devel >= 0.98.1
#BuildRequires:  polyclipping-devel >= 6.2.0
#BuildRequires:  boost-nowide-devel
#BuildRequires:  qhull-devel

%if %{with perltests}
# All of the old Perl dependencies needed to run the test suite
BuildRequires:  perl-devel
BuildRequires:  perl-generators
BuildRequires:  perl(Class::XSAccessor)
BuildRequires:  perl(Devel::CheckLib)
BuildRequires:  perl(Encode::Locale)
BuildRequires:  perl(ExtUtils::Embed)
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(ExtUtils::ParseXS)
BuildRequires:  perl(ExtUtils::Typemaps::Default)
BuildRequires:  perl(ExtUtils::Typemaps)
BuildRequires:  perl(File::Basename)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(Getopt::Long)
BuildRequires:  perl(Growl::GNTP)
BuildRequires:  perl(IO::Scalar)
BuildRequires:  perl(List::Util)
BuildRequires:  perl(local::lib)
BuildRequires:  perl(Math::PlanePath)
BuildRequires:  perl(Module::Build::WithXSpp)
BuildRequires:  perl(Moo)
BuildRequires:  perl(parent)
BuildRequires:  perl(POSIX)
BuildRequires:  perl(Scalar::Util)
BuildRequires:  perl(Storable)
BuildRequires:  perl(SVG)
BuildRequires:  perl(Test::Harness)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(Thread::Semaphore)
BuildRequires:  perl(threads)
BuildRequires:  perl(Time::HiRes)
BuildRequires:  perl(Unicode::Normalize)
BuildRequires:  perl(Wx)
BuildRequires:  perl(XML::SAX)
BuildRequires:  perl(XML::SAX::ExpatXS)
%endif

Requires:       hicolor-icon-theme

# === Bundled libraries ===
# Many are described here:
# https://github.com/prusa3d/PrusaSlicer/blob/master/doc/Dependencies.md

# Note that the developers have performed the worst sort of bundling: they are
# often using random portions of other projects, without keeping documentation
# or license files, and adding their own build system.  It can be very
# difficult to tell what versions have been bundled or even where they came
# from.

# Upstream has custom patches, reluctant to send to upstream
# License: GPLv2+
# Upstream: http://github.com/admesh/admesh/
Provides: bundled(admesh-libs) = 0.98.1

# This is a header-only library, not packaged in Fedora
# License: Copyright only or BSD
# Upstream: http://antigrain.com
Provides: bundled(agg) = 2.4

# Patched to fix a bug in some Prusa hardware
# License: GPLv2+
# Upstream: http://www.nongnu.org/avrdude
Provides: bundled(avrdude) = 6.3

# This could be unbundled, but the Fedora package is broken....
# This is a version from 2017, seemingly the last commit available.
# Fedora bug: https://bugzilla.redhat.com/show_bug.cgi?id=1712550
# License: Boost
# Upstream: https://github.com/artyom-beilis/nowide
Provides: bundled(boost-nowide)

# License: MPLv2.0
# Upstream: https://github.com/libigl/libigl
Provides: bundled(igl)

# Not packaged in Fedora, but could be.
# License: MIT
# Upstream: https://github.com/ocornut/imgui
Provides: bundled(imgui) = 1.66

# Some old code extracted from mesa libGLU that was last changed upstream in
# 2010 and last substantially changed before things were imported to git.
# The files are in src/glu-libtess.
# License: MIT
Provides: bundled(mesa-libGLU)

%if %{?fedora <= 30}
# For <= F30, the system miniz is too old to be used.  The bundled library is a
# fork from somewhere around 2.0.6, with various C++ source files added.
# License: MIT and Unlicense
Provides: bundled(miniz) = 2.0.6
%endif

# A header-only library, developed by one of the authors of PrusaSlicer.  Not
# packaged in Fedora, but could be (for little benefit).
# None of the source files carry licensing information, but a file LICENSE.txt
# exists and contains the AGPL text.
# License: AGPLv3
# Upstream: https://github.com/tamasmeszaros/libnest2d
Provides: bundled(libnest2d) = 0.3.2

# A tiny header-only library, not packaged in Fedora (but could be, though
# there is little point).  The filees appear to include commits up to and
# including one made on 2018-12-14 (c1f6e20) but nothing after.
# License: zlib
# Upstream: https://github.com/memononen/nanosvg
Provides: bundled(nanosvg)

# Two files from an old version of the Clipper/polyclipping library are used,
# but have been modified to add dependencies on other pieces of PrusaSlicer and
# to other bundled libraries.  The library is packaged in Fedora but that
# version is not usable.  (The bundled files are in src/clipper.)
# License: Boost
# Upstream: https://sourceforge.net/projects/polyclipping
Provides: bundled(polyclipping) = 6.2.9

# A tiny library, not packaged in Fedora (but could be).  Supposedly this is a
# candidate for removal but is still required for compilation.
# License: MIT
# Upstream: https://github.com/ivanfratric/polypartition
Provides: bundled(polypartition)

# It looks like we could unbundle this, but the Fedora package is old and
# doesn't appear to be suitable.  There is one change from upstream: in
# lib
# this, the compilation will fail as the slicer code expects floats while qhull
# uses doubles.
# License: Qhull
# Upstream: http://www.qhull.org
Provides: bundled(qhull) = 2016.01

# Is intended to be embedded (or installed into a source tree using clib).
# Could technically be packaged in Fedora but isn't currently.
# License: MIT
# Upstream: https://github.com/h2non/semver.c
Provides: bundled(semver) = 1.0.0

# Not packaged in Fedora; this is different from the existing "shiny" package.
# Upstream seems dead or idle as well.  To top it all off, the files have been
# reorganized from the upstream version.  Could technically be packaged, but
# PrusaSlicer would probably need patches to use it.
# License: MIT
# Upstream: https://sourceforge.net/projects/shinyprofiler/
Provides: bundled(shinyprofiler) = 2.6~rc1

# In case someone tries to install the upstream name
Provides: PrusaSlicer = %version-%release

# Because the old profiles are not compatible, don't replace slic3r-prusa3d
# until F31.  Both packages can be installed and used in parallel
%if %{?fedora} >= 31
Obsoletes: slic3r-prusa3d < 1.41.3-2
Provides: slic3r-prusa3d = %version-%release
%endif

%description
PrusaSlicer takes 3D models (STL, OBJ, AMF) and converts them into G-code
instructions for FFF printers or PNG layers for mSLA 3D printers. It's
compatible with any modern printer based on the RepRap toolchain, including all
those based on the Marlin, Prusa, Sprinter and Repetier firmware. It also works
with Mach3, LinuxCNC and Machinekit controllers.

PrusaSlicer is based on Slic3r by Alessandro Ranelucci and the RepRap
community.

%prep
%autosetup -S git -n PrusaSlicer-version_2.0.0

commit () { git commit -q -a -m "$1" --author "%{__scm_author}"; }

# Fix the "UNKNOWN" in the displayed version string
sed -i 's/UNKNOWN/Fedora/' version.inc
commit "Fix version string"

# F29 has the nlopt library under a different name
%if %{?fedora} < 30
sed -ri 's/^(.*_NLopt_LIB_NAMES "nlopt)(".*)$/\1_cxx\2/' src/libnest2d/cmake_modules/FindNLopt.cmake
commit "Fix name of nlopt library"
%endif

# Copy out specific license files so we can reference them later.
license () { mv src/$1/$2 $2-$1; git add $2-$1; echo %%license $2-$1 >> license-files; }
license agg copying
license avrdude COPYING
license imgui LICENSE.txt
license libnest2d LICENSE.txt
license qhull COPYING.txt
commit "Move license files"

# Delete a stray font file
rm -rf resources/fonts
commit "Remove stray font file"

# Unbundle libraries
unbundle () {
    rm -rf src/$1
    sed -i "/add_subdirectory($1)/d" src/CMakeLists.txt
    commit "Unbundle $1"
}

unbundle eigen
unbundle expat
unbundle glew

# This code doesn't seem to be used, so remove it to (potentially) simplify the
# licensing issue.
unbundle igl/copyleft

# Upstream says this is obsolete, but it's still needed for compilation.
# The Fedora version appears to work fine for that purpose so we'll use it.
unbundle poly2tri

# The miniz in F30 is too old to unbundle.
# The sed could be a patch, but conditionally applying patches is problematic
# and this will be fixed upstream in the next release.
%if %{?fedora} >= 31
unbundle miniz
sed -i 's/^#include.*miniz.*/#include <miniz.h>/' \
    src/libslic3r/Format/{3mf.cpp,AMF.cpp,PRUS.cpp} \
    src/libslic3r/Rasterizer/Rasterizer.cpp \
    src/libslic3r/Zipper.cpp
commit "Fix miniz includes"
%endif

# A single test fails on these architectures due to a difference in floating
# point rounding causing a tiny value instead of an expected zero.
%ifarch  s390x aarch64
git apply %SOURCE10
commit "Testsuite fix"
%endif


%build
mkdir Build
pushd Build

# -DSLIC3R_PCH=0 - Disable precompiled headers, which break cmake for some reason
# -DSLIC3R_FHS=1 - Enable FHS layout instead of installing things into the resources directory
# -DSLIC3R_WX_STABLE=1 - Allow use of wxGTK version 3.0 instead of 3.1.
%cmake .. -DSLIC3R_PCH=0 -DSLIC3R_FHS=1 -DSLIC3R_WX_STABLE=1 -DSLIC3R_GTK=3 \
    -DSLIC3R_BUILD_TESTS=1 -DCMAKE_BUILD_TYPE=Release \
%if %{with perltests}
    -DSLIC3R_PERL_XS=1
%endif

%make_build
popd

# Extract multiple sizes of PNG from the included .ico file.  The order of
# extracted files can change, so a bit of magic is required to get stable
# filenames.
mkdir hicolor
pushd hicolor
convert -set filename:dim '%%wx%%h' ../resources/icons/PrusaSlicer.ico %name-%%[filename:dim].png
for res in 16 32 48 64 128 256; do
    mkdir -p ${res}x${res}/apps
    cp %name-${res}x${res}.png ${res}x${res}/apps/%name.png
done
rm %name-*.png
popd

# To avoid "iCCP: Not recognized known sRGB profile that has been edited"
pushd resources/icons
find . -type f -name "*.png" -exec convert {} -strip {} \;
popd


%install
pushd Build
%make_install
popd

# Since the binary segfaults under Wayland, we have to wrap it.
mv %buildroot%_bindir/prusa-slicer %buildroot%_bindir/prusa-slicer.wrapped
cat >> %buildroot%_bindir/prusa-slicer <<'END'
#!/bin/bash
export GDK_BACKEND=x11
exec %_bindir/prusa-slicer.wrapped "$@"
END
chmod 755 %buildroot%_bindir/prusa-slicer

mkdir -p %buildroot%_datadir/icons/hicolor/
cp -r hicolor/* %buildroot%_datadir/icons/hicolor/

mkdir -p %buildroot%_datadir/appdata
install -m 644 %SOURCE2 %buildroot%_datadir/appdata/%name.appdata.xml

desktop-file-install --dir=%buildroot%_datadir/applications %SOURCE1

# For now, delete the Perl module that gets installed.  It only exists because
# we want the test suite to run.  It could be placed into a subpackage, but
# nothing needs it currently and it would conflict with the other slic3r
# package.
rm -rf %buildroot/%perl_vendorarch
rm -rf %buildroot/%perl_vendorlib

# Upstream installs the translation source files when they probably shouldn't
ls -lR %buildroot%_datadir/PrusaSlicer/localization
rm %buildroot%_datadir/PrusaSlicer/localization/{PrusaSlicer.pot,list.txt}
find %buildroot%_datadir/PrusaSlicer/localization/ -name \*.po -delete

# Handle locale files.  The find_lang macro doesn't work because it doesn't
# understand the directory structure.  This copies part of the funtionality of
# find-lang.sh by:
#   * Getting a listing of all files
#   * removing the buildroot prefix
#   * inserting the proper 'lang' tag
#   * removing everything that doesn't have a lang tag
#   * A list of lang-specific directories is also added
# The resulting file is included in the files list, where we must be careful to
# exclude that directory.
find %buildroot%_datadir/PrusaSlicer/localization -type f -o -type l | sed '
    s:'"%buildroot"'::
    s:\(.*/PrusaSlicer/localization/\)\([^/_]\+\)\(.*\.mo$\):%%lang(\2) \1\2\3:
    s:^\([^%].*\)::
    s:%lang(C) ::
    /^$/d
' > lang-files

find %buildroot%_datadir/PrusaSlicer/localization -type d | sed '
    s:'"%buildroot"'::
    s:\(.*\):%dir \1:
' >> lang-files


%check
# Some tests are Perl but there is a framework for other tests even though
# currently the only thing that uses them is one of the bundled libraries.
# There's no reason not to run as much as we can.
pushd Build
make test ARGS=-V


%files -f license-files -f lang-files
%license LICENSE
%doc README.md
%_bindir/%name
%_bindir/%name.wrapped
%_datadir/icons/hicolor/*/apps/%name.png
%_datadir/applications/%name.desktop
%_datadir/appdata/%name.appdata.xml
%dir %_datadir/PrusaSlicer
%_datadir/PrusaSlicer/{icons,models,profiles,shaders}/


%changelog
* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Jun 14 2019 Jason L Tibbitts III <tibbs@math.uh.edu> - 2.0.0-3
- Wrap the executable to set GDK_BACKEND=x11 to avoid segfault on Wayland.

* Wed Jun 05 2019 Jason L Tibbitts III <tibbs@math.uh.edu> - 2.0.0-2
- Update with review feedback
- Add in three patches suggested by upstream
- Try to enable building on aarch64 and s390x

* Mon May 20 2019 Jason L Tibbitts III <tibbs@math.uh.edu> - 2.0.0-1
- Update to 2.0.0 final release.

* Fri Feb 15 2019 Jason L Tibbitts III <tibbs@math.uh.edu> - 1.41.3-1
- Update to 1.41.3.

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.41.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Jan 30 2019 Jonathan Wakely <jwakely@redhat.com> - 1.41.0-3
- Rebuilt and patched for Boost 1.69

* Sun Dec 23 2018 Miro Hrončok <mhroncok@redhat.com> - 1.41.0-2
- Set GDK_BACKEND=x11 to prevent crashes on Wayland (#1661324)

* Mon Oct  1 2018 Tom Callaway <spot@fedoraproject.org> - 1.41.0-1
- update to 1.41.0

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.33.8-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sat Jun 30 2018 Jitka Plesnikova <jplesnik@redhat.com> - 1.33.8-11
- Perl 5.28 rebuild

* Tue Jun 05 2018 Jitka Plesnikova <jplesnik@redhat.com> - 1.33.8-10
- Add missing BR perl(ExtUtils::CBuilder)

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.33.8-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jan 18 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.33.8-8
- Remove obsolete scriptlets
- Rebuilt for new boost

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.33.8-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.33.8-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Jul 19 2017 Jonathan Wakely <jwakely@redhat.com> - 1.33.8-5
- Rebuilt for s390x binutils bug

* Tue Jul 18 2017 Jonathan Wakely <jwakely@redhat.com> - 1.33.8-4
- Rebuilt for Boost 1.64

* Thu Jun 08 2017 Jitka Plesnikova <jplesnik@redhat.com> - 1.33.8-3
- Perl 5.26 re-rebuild of bootstrapped packages

* Mon May 15 2017 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.33.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_27_Mass_Rebuild

* Wed Feb 22 2017 Miro Hrončok <mhroncok@redhat.com> - 1.33.8-1
- Update to 1.33.8
- Mention it's a fork in the description and appdata file
- Require hicolor-icon-theme
- Exclude big endian arches

* Sat Dec 17 2016 Miro Hrončok <mhroncok@redhat.com> - 1.31.6-1
- Update to 1.31.6
- Bundle admesh
- Recommend Thread::Queue for faster slicing
- Unbundle glew

* Fri Nov 11 2016 Miro Hrončok <mhroncok@redhat.com> - 1.31.4-1
- New package adapted from the slic3r package