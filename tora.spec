%define name	tora
%define version	2.0.0
%define release %mkrel 1

Summary:	Toolkit for Oracle with MySQL and PostgreSQL support only
Name:		%{name}
Version:	%{version}
Release:	%{release}
Source:		%{name}-%{version}.tar.gz
Source1:	tora-README.urpmi
Patch0:		fix_cmake_install_error.patch
Patch1:		fix_kde_theme_qt45.patch
Patch2:		fix_includes.patch
URL:		http://tora.sourceforge.net
Group:		Development/Databases
License:	GPLv2+
BuildRoot:	%{_tmppath}/tora-root
Requires:	libqscintilla-qt4_2
Requires:	qt4-common
Requires:	qt4-database-plugin-mysql
Requires:	qt4-database-plugin-pgsql
#Requires:	libaio
BuildRequires:	kdelibs4-devel
BuildRequires:	postgresql-devel
BuildRequires:	qscintilla-qt4-devel
BuildRequires:	qt4-devel

Conflicts:	tora-oracle

%description

TOra - Toolkit for Oracle, MySQL and PostgreSQL

ATTENTION: This package of TOra doesn't include Oracle support.
If you need Oracle support please install Oracle instant client
and the tora-oracle package instead.

In addition, TOra also supports postgres and mysql if your Qt library
is compiled with that support.

The features that are available so far is (As of version 1.2):

* Handles multiple connections
* Support Oracle & MySQL
* Advanced SQL Worksheet
	* Explain plan
	* PL/SQL auto indentation
	* Statement statistics
	* Error location indication
	* SQL syntax highlighting
	* Code completion
	* Visualization of result
	* PL/SQL block parsing
	* Statement statistics comparison
* Schema browser
	* Table & view editing
	* References & dependencies
	* Reverse engeneering of objects
	* Tab & tree based browsing
	* Object & data filtering
* PL/SQL Editor/Debugger
	* Breakpoints
	* Watches
	* Line stepping
	* SQL Output viewing
	* Structure tree parsing
* Server tuning
	* Server overview
	* Tuning charts
	* Wait state analyzer
	* I/O by tablespace & file
	* Performance indicators
	* Server statistics
	* Parameter editor (P-file editor)
* Security manager
* Storage manager with object & extent viewer

* Session manager
* Rollback manager with snapshot too old detection
* SGA and long operations trace
* Current session information

* PL/SQL profiler
* Explain plan browser
* Statistics manager
* DBMS alert tool
* Invalid object browser
* SQL Output viewer
* Database/schema comparison and search
* Extract schema objects to SQL script

* Easily extendable
* Possible to add support for new or older Oracle versions without programming.
* SQL template help
* Full UNICODE support
* Printing of any list, text or chart

Oracle is copyright of Oracle Corporation.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
%cmake_kde4	-DPOSTGRESQL_PATH_LIB=%{libdir}/postgresql/ \
		-DPOSTGRESQL_PATH_INCLUDES=%{includedir}/postgresql/
%make

%install
%makeinstall_std -C build

%find_lang %name

# menu
%{__mkdir_p} $RPM_BUILD_ROOT%{_datadir}/applications
cat > $RPM_BUILD_ROOT%{_datadir}/applications/%{name}.desktop << EOF
[Desktop Entry]
Encoding=UTF-8
Name=TOra
Comment=Toolkit for Oracle
Exec=%{name}
Icon=%{name}
Terminal=false
Type=Application
X-KDE-StartupNotify=true
Categories=X-MandrivaLinux-MoreApplications-Databases;Database;Office;KDE;Qt;
MimeType=application/x-tora;
EOF

%{__install} -D --mode=644 src/icons/tora.xpm $RPM_BUILD_ROOT%{_iconsdir}/hicolor/32x32/apps/tora.xpm
%{__install} -D --mode=644 src/icons/toramini.xpm $RPM_BUILD_ROOT%{_iconsdir}/hicolor/16x16/apps/tora.xpm
%{__install} -d $RPM_BUILD_ROOT%{_menudir}
%{__mkdir_p} $RPM_BUILD_ROOT%{_libdir}
%{__install} --mode=644 src/templates/*.tpl $RPM_BUILD_ROOT%{_libdir}/

# Explain the user we cannot provide the Oracle connector
cp %{SOURCE1} README.urpmi

%post
%update_icon_cache hicolor

%postun
%clean_icon_cache hicolor

%files
%defattr(-,root,root)
%{_bindir}/*
%{_libdir}/*.tpl
%_datadir/applications/%{name}.desktop
#%_datadir/doc/tora/*
%{_iconsdir}/hicolor/*/apps/%{name}*.xpm
%doc README.urpmi

