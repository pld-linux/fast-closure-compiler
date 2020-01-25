Summary:	Make the Google Closure Compiler start faster
Name:		fast-closure-compiler
Version:	0.0.1
Release:	0.2
License:	MIT
Group:		Applications/WWW
Source0:	https://github.com/Jimdo/fast-closure-compiler/archive/master/%{name}-%{version}.tar.gz
# Source0-md5:	16401ba7f17bf8011d743b59e7429f06
URL:		https://github.com/Jimdo/fast-closure-compiler
BuildRequires:	jdk
BuildRequires:	jpackage-utils
BuildRequires:	rpm-javaprov
BuildRequires:	rpmbuild(macros) >= 1.555
Requires:	jpackage-utils
Requires:	nailgun
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This gets around the long startup time of Google Closure Compiler
using Nailgun, which runs a single java process in the background and
keeps all of the classes loaded.

%prep
%setup -qc
mv fast-closure-compiler-*/* .

%build
cd bin
%javac NailgunTest.java

%{__cc} NailgunTest.c -shared -fPIC %{rpmcppflags} %{rpmcflags} %{rpmldflags} -o libNailgunTest.jnilib \
	-I%{_jvmlibdir}/java/include \
	-I%{_jvmlibdir}/java/include/%{_os}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_jnidir},%{_javadir}}
install -p bin/closure $RPM_BUILD_ROOT%{_bindir}
install -p bin/libNailgunTest.jnilib $RPM_BUILD_ROOT%{_jnidir}
cp -p bin/NailgunTest.class $RPM_BUILD_ROOT%{_javadir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/closure
%attr(755,root,root) %{_jnidir}/libNailgunTest.jnilib
%{_javadir}/NailgunTest.class
