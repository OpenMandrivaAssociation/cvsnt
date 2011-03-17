%define name cvsnt
%define version 2.5.04.3236
%define release %mkrel 6

Summary: A powerful CVS replacement
Name: %{name}
Version: %{version}
Release: %{release}
Source0: http://march-hare.com/archive/%{name}-%{version}.tar.gz
Patch1: cvsnt-2.5.04.3236-fix-detect-pcre.patch
Patch2: cvsnt-2.5.04.3236-gcc43.patch
License: GPLv1+
Group: Development/Other
Url: http://www.cvsnt.com
BuildRoot: %{_tmppath}/%{name}-buildroot
BuildRequires: sqlite3-devel
BuildRequires: mysql-devel
BuildRequires: unixODBC-devel
BuildRequires: postgresql-devel
BuildRequires: pam-devel
BuildRequires: krb5-devel
BuildRequires: pcre-devel
BuildRequires: zlib-devel
BuildRequires: libxml2-devel
Obsoletes: %{_lib}cvsnt2.5.03.2382

%description
CVSNT is software used to keep a track of changes to files stored on a computer
This is the function at the heart of all Source Code Management, Document
Management and Configuration Management Systems.

%package rcs
Summary: RCS compatible commande from %name
Group: Development/Other
Conflicts: rcs

%description rcs
RCS compatible commande from %name

%package database-mysql
Summary: Mysql database backend for %name
Group: Development/Other

%description database-mysql
Mysql database backend for %name

%package database-sqlite
Summary: Sqlite database backend for %name
Group: Development/Other

%description database-sqlite
Sqlite database backend for %name

%package database-pgsql
Summary: PostgreSql database backend for %name
Group: Development/Other

%description database-pgsql
PostgreSql database backend for %name

%package database-odbc
Summary: ODBC database backend for %name
Group: Development/Other

%description database-odbc
ODBC database backend for %name

%prep
%setup -q
%patch1 -p0 -b .pcre
%patch2 -p0 -b .gcc43

%build
# (tv) fix build on x86_64:
export CFLAGS="$CFLAGS -fPIC"
export CXXFLAGS="$CXXFLAGS -fPIC"
autoreconf
%configure2_5x \
    --enable-sqlite \
    --enable-mysql \
    --enable-odbc \
    --enable-postgres \
    --enable-pam \
    --enable-server \
    --enable-lockserver \
    --enable-pserver \
    --enable-ext \
    --enable-fork \
    --enable-rsh \
    --enable-gserver \
    --enable-sserver \
    --enable-sspi \
    --enable-enum \
    --enable-rcs
%make

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall_std

# nice but we don't want of this link
rm -f %{buildroot}%{_bindir}/cvs

# what can we do with .la without .h files ?
find %{buildroot}%{_libdir} -name "*.la" -exec rm -f {} \;
find %{buildroot}%{_libdir} -type l -exec rm -f {} \;

mv %{buildroot}%{_mandir}/man1/cvs.1 %{buildroot}%{_mandir}/man1/cvsnt.1
mv %{buildroot}%{_mandir}/man5/cvs.5 %{buildroot}%{_mandir}/man5/cvsnt.5

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc AUTHORS ChangeLog NEWS README
%_sysconfdir/%name
%_bindir/cvsnt
%_bindir/cvslockd
%_bindir/cvsscript
%_mandir/*/*
%_libdir/*-%{version}.so
%dir %_libdir/%name
%dir %_libdir/%name/database
%_libdir/%name/protocols
%_libdir/%name/triggers
%_libdir/%name/xdiff
%_libdir/%name/mdns

%files rcs
%defattr(-,root,root)
%_bindir/co
%_bindir/rcsdiff
%_bindir/rlog

%files database-mysql
%defattr(-,root,root)
%_libdir/%name/database/mysql.so

%files database-sqlite
%defattr(-,root,root)
%_libdir/%name/database/sqlite.so

%files database-pgsql
%defattr(-,root,root)
%_libdir/%name/database/postgres.so

%files database-odbc
%defattr(-,root,root)
%_libdir/%name/database/odbc.so

