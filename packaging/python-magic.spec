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
%{expand:%(sed -n -e '/^Source:/,/^BuildRoot:/p' <%_sourcedir/file.spec)}
%global         _sysconfdir /etc
%global         _miscdir    %{_datadir}/misc

%description 
This package contains the python binding that require the magic "file"
interface.

%prep
%{expand:%(sed -n -e '/^%%prep/,/^%%install/p' <%_sourcedir/file.spec | sed -e '1d' -e '$d')}

%install
pushd python
python setup.py install --root=%{buildroot}	\
			--prefix=%{_prefix}	\
			--record-rpm=../python_files
popd

%files -f python_files
%defattr(-,root,root)

%changelog
