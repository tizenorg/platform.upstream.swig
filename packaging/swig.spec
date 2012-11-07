#
# spec file for package swig
#
# Copyright (c) 2012 SUSE LINUX Products GmbH, Nuernberg, Germany.
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via http://bugs.opensuse.org/
#


Name:           swig
Version:        2.0.7
Release:        0
License:        GPL-3.0+ and BSD-3-Clause
Summary:        Simplified Wrapper and Interface Generator
Url:            http://www.swig.org/
Group:          Development/Languages/C and C++
Source:         http://sourceforge.net/projects/swig/files/swig/%{name}-%{version}/%{name}-%{version}.tar.gz
Source1:        %{name}.rpmlintrc
# PATCH-FIX-UPSTREAM swig-2.0.4-guile2.patch pgajdos@suse.com -- generate guile 2 friendly code
Patch0:         swig-2.0.4-guile2.patch
# PATCH-PENDING-UPSTREAM - Ruby 1.9 - kkaempf@suse.de
Patch1:         0001-Ruby-replace-obsolete-STR2CSTR-macro-with-StringValu.patch
Patch2:         0002-Ruby-use-RbConfig-instead-of-deprecated-Config-modul.patch
Patch3:         0003-Ruby-Fix-include-pathes-for-Ruby-1.9.patch
Patch4:         0004-Ruby-Add-local-dir-to-loadpath-for-Ruby-1.9.patch
Patch5:         0007-Ruby-1.9-methods-returns-array-of-Symbols-now.patch
Patch6:         0008-Ruby-Disable-broken-tests.patch
Patch7:         0012-Python-Disable-broken-test-in-threads_exception.patch
# Upstream ID 3530078
Patch8:         0013-Fix-call-to-Swig_name_decl-upstream-ID-3530078.patch
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  boost-devel
%define docpath %{_docdir}/%{name}
BuildRequires:  fdupes
BuildRequires:  gcc-c++
BuildRequires:  libtool
BuildRequires:  pcre-devel
BuildRequires:  perl
BuildRequires:  pkg-config
BuildRequires:  python-devel
BuildRoot:      %{_tmppath}/%{name}-%{version}-build

%description
SWIG is a compiler that attempts to make it easy to integrate C, C++,
or Objective-C code with scripting languages including Perl, Tcl, and
Python.  In a nutshell, you give it a bunch of ANSI C/C++ declarations
and it generates an interface between C and your favorite scripting
language.  However, this is only scratching the surface of what SWIG
can do--some of its more advanced features include automatic
documentation generation, module and library management, extensive
customization options, and more.

%package doc
License:        BSD-3-Clause
Summary:        SWIG Manual
Group:          Documentation/Man
Requires:       swig
BuildArch:      noarch

%description doc
SWIG is a compiler that attempts to make it easy to integrate C, C++,
or Objective-C code with scripting languages including Perl, Tcl, and
Python.  In a nutshell, you give it a bunch of ANSI C/C++ declarations
and it generates an interface between C and your favorite scripting
language.  However, this is only scratching the surface of what SWIG
can do--some of its more advanced features include automatic
documentation generation, module and library management, extensive
customization options, and more.

This package contains the SWIG manual.

%package examples
License:        BSD-3-Clause
Summary:        SWIG example files
Group:          Documentation/Howto
Requires:       swig

%description examples
SWIG is a compiler that attempts to make it easy to integrate C, C++,
or Objective-C code with scripting languages including Perl, Tcl, and
Python.  In a nutshell, you give it a bunch of ANSI C/C++ declarations
and it generates an interface between C and your favorite scripting
language.  However, this is only scratching the surface of what SWIG
can do--some of its more advanced features include automatic
documentation generation, module and library management, extensive
customization options, and more.

This package contains SWIG examples, useful both for testing and
understandig SWIG usage.

%prep
%setup -q
# guile 2 from 12.1
%patch0 -p1
# Ruby 1.9 from 12.1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1

%build
sh autogen.sh
%configure --disable-ccache
make %{?_smp_mflags}

%check
# Segfaults
rm -f Examples/test-suite/python/li_std_containers_int_runme.py
rm -f Examples/test-suite/python/li_boost_shared_ptr_runme.py
make check

%install
%make_install

install -d %{buildroot}%{docpath}
cp -a TODO ANNOUNCE CHANGES* LICENSE README Doc/{Devel,Manual} \
	%{buildroot}%{docpath}
install -d %{buildroot}%{_libdir}/swig
cp -a Examples %{buildroot}%{_libdir}/swig/examples
rm -rf %{buildroot}%{_libdir}/swig/examples/test-suite

# rm files that are not needed for running or rebuilding the examples
find %{buildroot}%{_libdir}/swig \
	-name '*.dsp' -o -name '*.vcproj' -o -name '*.sln' -o \
	-name '*.o' -o -name '*_wrap.c' | xargs rm

# fix perms
chmod -x %{buildroot}%{docpath}/Manual/*
find %{buildroot}%{_libdir}/swig -name '*.h' -perm +111 | \
	xargs --no-run-if-empty chmod -x
ln -s %{_libdir}/swig/examples %{buildroot}%{docpath}/Examples

%fdupes %{buildroot}

%files
%defattr(644,root,root,755)
%dir %{docpath}
%{docpath}/[A-Z][A-Z]*
%{_datadir}/swig
%attr(755,root,root) %{_bindir}/swig

%files doc
%defattr(-,root,root)
%{docpath}/Devel
%{docpath}/Manual

%files examples
%defattr(-,root,root)
%{docpath}/Examples
%{_libdir}/swig

%changelog
