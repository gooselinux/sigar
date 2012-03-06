Name:		sigar
Version:	1.6.5
Release:	0.1.git833ca18%{?dist}
Summary:	System Information Gatherer And Reporter

%global sigar_suffix  0-g4b67f57
%global sigar_hash    833ca18

Group:		System Environment/Libraries
License:	ASL 2.0
URL:		http://sigar.hyperic.com/

# Once 1.6.5 is released, we can use tarballs from GitHub:
#    Source0:	http://download.github.com/hyperic-sigar-{name}-{version}-{sigar_suffix}.tar.gz
#
# Until then the tarball can be re-generated with:
#    git clone git://github.com/hyperic/sigar.git
#    cd sigar
#    git archive --prefix=sigar-1.6.5/ 833ca18 | bzip2 > sigar-1.6.5-833ca18.tbz2
#
# The diff from 1.6.4 is too huge to contemplate cherrypicking from
Source0:	%{name}-%{version}-%{sigar_hash}.tbz2

BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:	gcc cmake

%description
The Sigar API provides a portable interface for gathering system
information such as:
- System memory, swap, CPU, load average, uptime, logins
- Per-process memory, CPU, credential info, state, arguments,
  environment, open files
- File system detection and metrics
- Network interface detection, configuration info and metrics
- Network route and connection tables

This information is available in most operating systems, but each OS
has their own way(s) providing it. SIGAR provides developers with one
API to access this information regardless of the underlying platform.

#The core API is implemented in pure C with bindings currently
#implemented for Java, Perl and C#.

%package devel 
License:	ASL 2.0
Group:		Development/Libraries
Summary:	SIGAR Development package - System Information Gatherer And Reporter
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for developing against the Sigar API

%prep
# When using the GitHub tarballs, use:
# setup -q -n hyperic-{name}-{sigar_hash}
%setup -q -n %{name}-%{version}

%build

# Fix lib directory
sed -i.sed s:DESTINATION\ lib:DESTINATION\ %{_lib}: src/CMakeLists.txt

mkdir build
pushd build
%cmake ..
make %{?_smp_mflags}
popd

%install
rm -rf $RPM_BUILD_ROOT
pushd build
%cmake ..
make install DESTDIR=$RPM_BUILD_ROOT
popd

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc ChangeLog README LICENSE NOTICE AUTHORS
%{_libdir}/libsigar.so

%files devel
%defattr(-,root,root,-)
%{_includedir}/sigar*.h
%doc LICENSE NOTICE AUTHORS

%changelog
* Thu Dec 16 2010 Andrew Beekhof <andrew@beekhof.net> - 1.6.5-0.1.git833ca18
- Incorporate review feedback
  + Add calls to ldconfig
  + Fix package group
  + Resolve rpmlint warnings
  + Added LICENSE, NOTICE and AUTHORS to the doc list
  + Document how the tarball was generated
  + Update version number to be a .5 pre-release snapshot

* Wed Dec 1 2010 Andrew Beekhof <andrew@beekhof.net> - 1.6.4-1
- Initial checkin
