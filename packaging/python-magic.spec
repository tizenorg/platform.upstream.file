%define build_python_bindings 1
%global         _miscdir    %{_datadir}/misc

Name:           python-magic
BuildRequires:  findutils
BuildRequires:  libtool
BuildRequires:  python-devel
BuildRequires:  zlib-devel
Url:            http://www.darwinsys.com/file/
Version:        5.20
Release:        0
Summary:        Python module to use libmagic
License:        BSD-3-Clause and BSD-4-Clause
Group:          Platform Development/Python
Source99:       file.spec
BuildArch:      noarch

%{expand:%(sed -n -e '/^### SOURCES BEGIN ###/,/^### SOURCES END ###/p' <%_sourcedir/file.spec)}
Source:         ftp://ftp.astron.com/pub/file/file-%{version}.tar.gz

%description 
This package contains the python binding that require the magic "file"
interface.


%prep
%setup -q -n file-%{version}
%{expand:%(sed -n -e '/^### PREP BEGIN ###/,/^### PREP END ###/p' <%_sourcedir/file.spec)}

%build
%{expand:%(sed -n -e '/^### BUILD BEGIN ###/,/^### BUILD END ###/p' <%_sourcedir/file.spec)}

%install
pushd python
python setup.py install --root=%{buildroot} \
                        --prefix=%{_prefix} \
                        --record-rpm=../python_files
popd

%files -f python_files
%defattr(-,root,root)

