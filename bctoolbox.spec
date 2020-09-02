%define _disable_ld_no_undefined 1
%define _disable_lto 1

%define major	1
%define libname	%mklibname bctoolbox %{major}
%define tlibname %mklibname bctoolbox-tester %{major}
%define devname	%mklibname -d bctoolbox
%define devstat	%mklibname -s bctoolbox

Summary:	Library for accessing USB devices
Name:		bctoolbox
Version:	4.3.2
Release:	1
License:	LGPLv2+
Group:		System/Libraries
Url:		https://github.com/BelledonneCommunications/
Source0:	https://github.com/BelledonneCommunications/bctoolbox/archive/%{version}/%{name}-%{version}.tar.gz
Patch0:		bctoolbox-0.6.0-polarssl-1.3.patch
BuildRequires:	cmake
BuildRequires:	pkgconfig(bcunit)
BuildRequires:	mbedtls-devel

%description
Utilities library used by Belledonne Communications
softwares like belle-sip, mediastreamer2 and linphone.

%package -n	%{libname}
Summary:	Library for accessing USB devices
Group:		System/Libraries

%description -n	%{libname}
Library used by Belledonne Communications
softwares like belle-sip, mediastreamer2 and linphone.

%package -n	%{tlibname}
Summary:	%{name} testing library
Group:		System/Libraries

%description -n	%{tlibname}
%{name} testing library

%package -n	%{devname}
Summary:	Development files for %{name}
Group:		Development/C
Requires:	%{libname} = %{version}-%{release}
Requires:	%{tlibname} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}
Obsoletes:	%{name}-devel-doc < 1.0.15-2

%description -n	%{devname}
This package includes the development files for %{name}.

%package -n	%{devstat}
Summary:	Development files for %{name}
Group:		Development/C
Requires:	%{devname} = %{version}-%{release}
Provides:	%{name}-static-devel = %{version}-%{release}

%description -n	%{devstat}
This package includes the static library files for %{name}.

%prep
%autosetup -p1

%build
sed -i 's!CMAKE_INSTALL_PREFIX}/lib!CMAKE_INSTALL_PREFIX}/%{_lib}!g' CMakeLists.txt
%cmake \
	-DENABLE_STRICT:BOOL=NO \
	-DENABLE_MBEDTLS:BOOL=ON \
	-DENABLE_POLARSSL:BOOL=OFF
%make

%install
%makeinstall_std -C build

%files -n %{libname}
%{_libdir}/libbctoolbox.so.%{major}*

%files -n %{tlibname}
%{_libdir}/libbctoolbox-tester.so.%{major}*

%files -n %{devstat}
%{_libdir}/libbctoolbox.a
%{_libdir}/libbctoolbox-tester.a

%files -n %{devname}
%{_libdir}/libbctoolbox.so
%{_libdir}/libbctoolbox-tester.so
%{_includedir}/%{name}
%{_datadir}/%{name}/cmake/
%{_libdir}/pkgconfig/%{name}.pc
%{_libdir}/pkgconfig/%{name}-tester.pc
