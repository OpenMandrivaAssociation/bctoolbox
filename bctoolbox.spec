%define major	1
%define libname	%mklibname %{name}
%define tlibname	%mklibname %{name}-tester
%define devname	%mklibname %{name} -d
%define devstat	%mklibname %{name} -d -s

# exclude unwanted cmake requires
%global __provides_exclude_from ^%{_datadir}/cmake/.*/Find.*cmake$
%global __requires_exclude cmake\\(decaf\\)|cmake\\(Decaf\\) \
	|cmake\\(mbedtls\\)|cmake\\(MbedTLS\\)

%bcond mbedtls			1
%bcond decaf			1
%bcond strict			0
%bcond unit_tests		1
%bcond unit_tests_install	0

Summary:	Library for accessing USB devices
Name:		bctoolbox
Version:	5.3.97
Release:	1
License:	LGPLv2+
Group:		System/Libraries
Url:		https://www.linphone.org
Source0:	https://gitlab.linphone.org/BC/public/%{name}/-/archive/%{version}/%{name}-%{version}.tar.bz2
Patch0:		bctoolbox-5.3.6-cmake-fix_cmake_path.patch
Patch1:		bctoolbox-5.3.6-cmake-fix-version.patch
Patch2:		bctoolbox-5.3.97-mbed.patch

BuildRequires:	cmake
BuildRequires:	ninja
BuildRequires:	cmake(bcunit)
BuildRequires:	pkgconfig(mbedtls)
BuildRequires:	pkgconfig(ncurses)
BuildRequires:	pkgconfig(zlib)
BuildRequires:	libdecaf-devel

%description
Utilities library used by Belledonne Communications
softwares like belle-sip, mediastreamer2 and linphone.

#---------------------------------------------------------------------------

%package -n	%{libname}
Summary:	Library for accessing USB devices
Group:		System/Libraries

%description -n	%{libname}
Library used by Belledonne Communications
softwares like belle-sip, mediastreamer2 and linphone.

%files -n %{libname}
%{_libdir}/libbctoolbox.so.%{major}*

#---------------------------------------------------------------------------

%package -n	%{tlibname}
Summary:	%{name} testing library
Group:		System/Libraries

%description -n	%{tlibname}
%{name} testing library

%files -n %{tlibname}
%if %{with unit_tests_install}
%{_bindir}/%{name}-tester
%endif
%{_libdir}/libbctoolbox-tester.so.%{major}*

#---------------------------------------------------------------------------

%package -n	%{devname}
Summary:	Development files for %{name}
Group:		Development/C
Requires:	%{libname} = %{version}-%{release}
Requires:	%{tlibname} = %{version}-%{release}
%if %{with static}
Requires:	%{devstat} = %{version}-%{release}
%endif
Provides:	%{name}-devel = %{version}-%{release}
Obsoletes:	%{name}-devel-doc < 1.0.15-2

%description -n	%{devname}
This package includes the development files for %{name}.

%files -n %{devname}
%{_libdir}/libbctoolbox.so
%{_libdir}/libbctoolbox-tester.so
%{_includedir}/%{name}
%{_libdir}/pkgconfig/%{name}.pc
%{_libdir}/pkgconfig/%{name}-tester.pc
%{_datadir}/cmake/BCToolbox

#---------------------------------------------------------------------------

%if %{with static}
%package -n	%{devstat}
Summary:	Development files for %{name}
Group:		Development/C
Requires:	%{devname} = %{version}-%{release}
Provides:	%{name}-static-devel = %{version}-%{release}
%rename		%{_lib}bctoolbox-static

%description -n	%{devstat}
This package includes the static library files for %{name}.

%files -n %{devstat}
%{_libdir}/libbctoolbox.a
%{_libdir}/libbctoolbox-tester.a
%endif

#---------------------------------------------------------------------------

%prep
%autosetup -p1

%build
%cmake \
	-DENABLE_STRICT:BOOL=%{?with_strict:ON}%{?!with_strict:OFF} \
	-DENABLE_DECAF:BOOL=%{?with_defac:ON}%{?!with_decaf:OFF} \
	-DENABLE_UNIT_TESTS:BOOL=%{?with_unit_tests:ON}%{?!with_unit_tests:OFF} \
	-DCONFIG_PACKAGE_LOCATION:PATH=%{_datadir}/cmake/%{oname} \
	-G Ninja

%ninja_build

%install
%ninja_install -C build

# don't install unit tester
%if %{with unit_tests} && ! %{with unit_tests_install}
rm -f  %{buildroot}%{_bindir}/%{name}-tester
rm -fr %{buildroot}%{_datadir}/%{name}-tester/
%endif

%check
%if %{with unit_tests}
pushd build
ctest
popd
%endif

