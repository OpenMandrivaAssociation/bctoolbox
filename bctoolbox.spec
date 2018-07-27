%define major	1
%define libname	%mklibname bctoolbox %{major}
%define devname	%mklibname -d bctoolbox
%define devstat	%mklibname -s bctoolbox

Summary:	Library for accessing USB devices
Name:		bctoolbox
Version:	0.6.0
Release:	1
License:	LGPLv2+
Group:		System/Libraries
Url:		https://github.com/BelledonneCommunications/
Source0:	https://github.com/BelledonneCommunications/bctoolbox/archive/%{version}.tar.gz
BuildRequires:	polarssl-devel
BuildRequires:	cmake

%description
Utilities library used by Belledonne Communications
softwares like belle-sip, mediastreamer2 and linphone.

%package -n	%{libname}
Summary:	Library for accessing USB devices
Group:		System/Libraries

%description -n	%{libname}
Library used by Belledonne Communications
softwares like belle-sip, mediastreamer2 and linphone.

%package -n	%{devname}
Summary:	Development files for %{name}
Group:		Development/C
Requires:	%{libname} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}
Obsoletes:	%{name}-devel-doc < 1.0.15-2

%description -n	%{devname}
This package includes the development files for %{name}.

%package -n	%{devstat}
Summary:	Development files for %{name}
Group:		Development/C
Requires:	%{devname} = %{version}-%{release}
Provides:	%{name}-static-devel = %{version}-%{release}

%description -n	%{devname}
This package includes the development files for %{name}.

%prep
%setup -q

%build
sed -i 's!CMAKE_INSTALL_PREFIX}/lib!CMAKE_INSTALL_PREFIX}/%{_lib}!g' CMakeLists.txt
%cmake -DENABLE_TESTS=NO -DENABLE_TESTS_COMPONENT=NO
%make

%install
%makeinstall_std -C build

%files -n %{libname}
%{_libdir}/libbctoolbox.so.%{major}*

%files -n %{devstat}
%{_libdir}/libbctoolbox.a

%files -n %{devname}
%{_libdir}/libbctoolbox.so
%{_includedir}/%{name}
%{_datadir}/%{name}/cmake/
%{_libdir}/pkgconfig/%{name}.pc
