Name:           python-magic
%define build_python_bindings 1
BuildRequires:  findutils
BuildRequires:  libtool
BuildRequires:  python-devel
BuildRequires:  zlib-devel
Url:            http://www.darwinsys.com/file/
Version:        5.11
Release:        0
Summary:        Python module to use libmagic
License:        BSD-3-Clause and BSD-4-Clause
Group:          Development/Languages/Python
Source99:       file.spec
Source:         ftp://ftp.astron.com/pub/file/file-%{version}.tar.gz
Source2:        baselibs.conf
Source1001:     file.manifest
%global         _miscdir    %{_datadir}/misc
%global         _sysconfdir /etc
BuildRoot:      %{_tmppath}/%{name}-%{version}-build

%description 
This package contains the python binding that require the magic "file"
interface.

%prep
%setup -q -n file-%{version}
cp %{SOURCE1001} .
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
pushd python
python setup.py install --root=%{buildroot}	\
			--prefix=%{_prefix}	\
			--record-rpm=../python_files
popd

%files -f python_files
%defattr(-,root,root)

%changelog
