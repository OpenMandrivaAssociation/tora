%define name	tora
%define version	2.1.3
%define release %mkrel 1

Summary:	Toolkit for Oracle with MySQL and PostgreSQL support only
Name:		%{name}
Version:	%{version}
Release:	%{release}
Source:		%{name}-%{version}.tar.bz2
#Patch1:		fix_kde_theme_qt45.patch
URL:		http://tora.sourceforge.net
Group:		Development/Databases
License:	GPLv2+
BuildRoot:	%{_tmppath}/tora-root

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

Oracle is copyright of Oracle Corporation.

%prep
%setup -q
#%patch1 -p1

%build
%cmake_kde4 -DPOSTGRESQL_PATH_LIB=%{libdir}/postgresql/  \
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
Categories=X-MandrivaLinux-MoreApplications-Databases;Database;KDE;Qt;
MimeType=application/x-tora;
EOF

%{__install} -D --mode=644 src/icons/tora.xpm $RPM_BUILD_ROOT%{_iconsdir}/hicolor/32x32/apps/tora.xpm
%{__install} -D --mode=644 src/icons/toramini.xpm $RPM_BUILD_ROOT%{_iconsdir}/hicolor/16x16/apps/tora.xpm
%{__install} -d $RPM_BUILD_ROOT%{_menudir}
%{__mkdir_p} $RPM_BUILD_ROOT%{_libdir}
%{__install} --mode=644 src/templates/*.tpl $RPM_BUILD_ROOT%{_libdir}/

cat > ${RPM_BUILD_ROOT}/%{_docdir}/tora/README.urpmi << EOF

ATTENTION:
This package of TOra doesn't include Oracle support.

If you need Oracle support, please install Oracle instant client
first and download tora-oracle package For Mandriva from
http://www.sourceforge.net/projects/tora/files instead. 

You can download Oracle instant client from Oracle web site 
for free.

EOF

%post
%update_icon_cache hicolor

%postun
%clean_icon_cache hicolor

%files
%defattr(-,root,root)
%{_bindir}/*
%{_libdir}/*.tpl
%_datadir/applications/%{name}.desktop
%_datadir/doc/tora/*
%{_iconsdir}/hicolor/*/apps/%{name}*.xpm

