Name:           file
BuildRequires:  findutils
BuildRequires:  libtool
BuildRequires:  zlib-devel
Url:            http://www.darwinsys.com/file/
Version:        5.11
Release:        0
Summary:        A Tool to Determine File Types
License:        BSD-2-Clause
Group:          Productivity/File utilities
Source:         ftp://ftp.astron.com/pub/file/file-%{version}.tar.gz
Source2:        baselibs.conf
%global         _sysconfdir /etc
%global         _miscdir    %{_datadir}/misc

%description
With the file command, you can obtain information on the file type of a
specified file. File type recognition is controlled by the file
/etc/magic, which contains the classification criteria. This command is
used by apsfilter to permit automatic printing of different file types.

%package -n libmagic-data
Summary:        The magic files for libmagic to use
Group:          Development/Libraries/Other

%description -n libmagic-data
This package contains the basic magic files that libmagic reads and uses
to estimate a file's type.

%package -n libmagic
Summary:        Library with file's functionality
Group:          Development/Libraries/Other
Requires:       libmagic-data = %{version}
Provides:	libfile
Obsoletes:	libfile =< 5.04

%description -n libmagic
This library reads magic files and detects file types. Used by file command

%package     -n file-devel
Summary:        Include Files and Libraries mandatory for Development
Group:          Development/Libraries/Other
Provides:       file:/usr/include/magic.h
Requires:       glibc-devel
Requires:       libmagic = %{version}

%description -n file-devel
This package contains all necessary include files and libraries needed
to develop applications that require the magic "file" interface.

%prep
%setup -q -n file-%{version}
%build
export LANG=POSIX
export LC_ALL=POSIX
rm -f Magdir/*,v Magdir/*~
rm -f ltcf-c.sh ltconfig ltmain.sh
autoreconf -fiv
CFLAGS="$RPM_OPT_FLAGS -DHOWMANY=69632"
%configure --disable-silent-rules --datadir=%{_miscdir} --disable-static --with-pic --enable-fsect-man5
%{__make} %{?_smp_mflags} pkgdatadir='$(datadir)'
%if 0%{?build_python_bindings:1}
pushd python
python setup.py build
popd
%endif

%install
export LANG=POSIX
export LC_ALL=POSIX
mkdir  %{buildroot}/etc
make DESTDIR=%{buildroot} install pkgdatadir='$(datadir)'
rm -vf %{buildroot}%{_sysconfdir}/magic
echo '# Localstuff: file(1) magic(5) for locally observed files' > %{buildroot}%{_sysconfdir}/magic
echo '#     global magic file is %{_miscdir}/magic(.mgc)'	>> %{buildroot}%{_sysconfdir}/magic
%{nil install -s dcore %{buildroot}%{_bindir}}
# Check out that the binary does not bail out:
LD_LIBRARY_PATH=%{buildroot}%{_libdir}
export LD_LIBRARY_PATH
find %{buildroot}%{_bindir}/file %{_bindir}/ /%{_lib}/ %{_libdir}/ | \
	xargs %{buildroot}%{_bindir}/file -m %{buildroot}%{_miscdir}/magic
unset LD_LIBRARY_PATH
%{__rm} -f %{buildroot}%{_libdir}/*.la

%post -n libmagic -p /sbin/ldconfig

%postun -n libmagic -p /sbin/ldconfig

%files -n libmagic
%defattr (644,root,root,755)
%{_libdir}/lib*.so.*

%files -n libmagic-data
%defattr (644,root,root,755)
%config(noreplace) %{_sysconfdir}/magic
%{_miscdir}/magic
%{_miscdir}/magic.mgc
%doc %{_mandir}/man5/magic.5.gz

%files
%defattr (644,root,root,755)
%{nil %{_bindir}/dcore}
%attr(755,root,root) %{_bindir}/file
%doc %{_mandir}/man1/file.1.gz
%doc COPYING 

%files -n file-devel
%defattr (644,root,root,755)
%{_libdir}/lib*.so
%{_includedir}/magic.h
%doc %{_mandir}/man3/libmagic.3.gz
%doc README COPYING

%changelog
