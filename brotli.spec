Name:           brotli
Version:        0.6.0
Release:        4%{?dist}
Summary:        Lossless compression algorithm

License:        MIT
URL:            https://github.com/google/brotli
Source0:        https://github.com/google/brotli/archive/v%{version}.tar.gz

BuildRequires:  python2-devel python3-devel gcc-c++ gcc cmake

%description
Brotli is a generic-purpose lossless compression algorithm that compresses
data using a combination of a modern variant of the LZ77 algorithm, Huffman
coding and 2nd order context modeling, with a compression ratio comparable
to the best currently available general-purpose compression methods.
It is similar in speed with deflate but offers more dense compression.

%package -n python2-%{name}
Summary:        Lossless compression algorithm (python 2)
Requires: python2
%{?python_provide:%python_provide python2-%{name}}

%description -n python2-%{name}
Brotli is a generic-purpose lossless compression algorithm that compresses
data using a combination of a modern variant of the LZ77 algorithm, Huffman
coding and 2nd order context modeling, with a compression ratio comparable
to the best currently available general-purpose compression methods.
It is similar in speed with deflate but offers more dense compression.
This package installs a Python 2 module.


%package -n python3-%{name}
Requires: python3
Summary:        Lossless compression algorithm (python 3)
%{?python_provide:%python_provide python3-%{name}}

%description -n python3-%{name}
Brotli is a generic-purpose lossless compression algorithm that compresses
data using a combination of a modern variant of the LZ77 algorithm, Huffman
coding and 2nd order context modeling, with a compression ratio comparable
to the best currently available general-purpose compression methods.
It is similar in speed with deflate but offers more dense compression.
This package installs a Python 3 module.


%package -n %{name}-devel
Summary:        Lossless compression algorithm (development files)
Requires: %{name}%{?_isa} = %{version}-%{release} 

%description -n %{name}-devel
Brotli is a generic-purpose lossless compression algorithm that compresses
data using a combination of a modern variant of the LZ77 algorithm, Huffman
coding and 2nd order context modeling, with a compression ratio comparable
to the best currently available general-purpose compression methods.
It is similar in speed with deflate but offers more dense compression.
This package installs the development files

%prep
%autosetup
# fix permissions for -debuginfo
# rpmlint will complain if I create an extra %%files section for
# -debuginfo for this so we'll put it here instead
%{__chmod} 644 enc/*.[ch]
%{__chmod} 644 include/brotli/*.h
%build

mkdir -p build
cd build
%cmake .. -DCMAKE_INSTALL_PREFIX="%{_prefix}" \
    -DCMAKE_INSTALL_LIBDIR="%{_libdir}"
%make_build
cd ..
%py2_build
%py3_build

%install
cd build
%make_install
cd ..
# Must do the python2 install first because the scripts in /usr/bin are
# overwritten with every setup.py install, and in general we want the
# python3 version to be the default. If, however, we're installing separate
# executables for python2 and python3, the order needs to be reversed so
# the unversioned executable is the python2 one.
%py2_install
%py3_install
%{__install} -dm755 "%{buildroot}%{_mandir}/man3"
cd docs
for i in *.3;do
%{__install} -m644 "$i" "%{buildroot}%{_mandir}/man3/${i}brotli"
done

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%check
cd build
ctest -V
cd ..
%{__python2} setup.py test
%{__python3} setup.py test

%files
%{_bindir}/bro
%{_libdir}/*.so.*
%license LICENSE

# Note that there is no %%files section for the unversioned python module
# if we are building for several python runtimes
%files -n python2-%{name}
%{python2_sitearch}/*
%license LICENSE

%files -n python3-%{name}
%{python3_sitearch}/*
%license LICENSE

%files -n %{name}-devel
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*
%{_mandir}/man3/*


%changelog
* Tue May 23 2017 Travis Kendrick <pouar@pouar.net> - 0.6.0-4
- add man pages

* Sun May 14 2017 Travis Kendrick <pouar@pouar.net> - 0.6.0-3
- wrong directory for ctest
- LICENSE not needed in -devel
- fix "spurious-executable-perm"
- rpmbuild does the cleaning for us, so 'rm -rf %%{buildroot}' isn't needed

* Sat May 13 2017 Travis Kendrick <pouar@pouar.net> - 0.6.0-2
- include libraries and development files

* Sat May 06 2017 Travis Kendrick <pouar@pouar.net> - 0.6.0-1
- Initial build
