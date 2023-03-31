%define major	1
%define libname	 %mklibname %{name}
%define tlibname %mklibname %{name}-tester
%define devname	 %mklibname %{name} -d
%define devstat	 %mklibname %{name} -d -s

%bcond_without	mbedtls
%bcond_with	polarssl
%bcond_without	static
%bcond_with	strict

Summary:	Library for accessing USB devices
Name:		bctoolbox
Version:	5.2.38
Release:	2
License:	LGPLv2+
Group:		System/Libraries
Url:		https://www.linphone.org
Source0:	https://gitlab.linphone.org/BC/public/%{name}/-/archive/%{version}/%{name}-%{version}.tar.bz2
Patch0:		bctoolbox-4.4.24-cmake-fix-pkgconfig-pc-file.patch
Patch1:		bctoolbox-5.2.0-cmake-fix-version.patch
Patch2:		bctoolbox-5.2.0-fix-strict-prototypes-warinigs.patch 

BuildRequires:	cmake
BuildRequires:	ninja
BuildRequires:	pkgconfig(bcunit)
BuildRequires:	pkgconfig(ncurses)
BuildRequires:	pkgconfig(zlib)
BuildRequires:	libdecaf-devel
BuildRequires:	mbedtls-devel

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
%{_bindir}/%{name}_tester
%{_libdir}/libbctoolbox-tester.so.%{major}*

#---------------------------------------------------------------------------

%package -n	%{devname}
Summary:	Development files for %{name}
Group:		Development/C
Requires:	%{libname} = %{version}-%{release}
Requires:	%{tlibname} = %{version}-%{release}
Requires:	%{devstat} = %{version}-%{release}
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
%{_datadir}/cmake/%{name}

#---------------------------------------------------------------------------

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

#---------------------------------------------------------------------------

%prep
%autosetup -p1

%build
%cmake \
	-DENABLE_STATIC:BOOL=%{?with_static:ON}%{?!with_static:OFF} \
	-DENABLE_STRICT:BOOL=%{?with_strict:ON}%{?!with_strict:OFF} \
	-DENABLE_MBEDTLS:BOOL=%{?with_mbedtls:ON}%{?!with_mbedtls:OFF} \
	-DENABLE_POLARSSL:BOOL=%{?with_polarssl:ON}%{?!with_polarssl:OFF} \
	-G Ninja

%ninja_build

%install
%ninja_install -C build

