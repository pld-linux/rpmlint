#
# Conditional build:
%bcond_without	tests		# build without tests

Summary:	Tool for checking common errors in RPM packages
Summary(pl.UTF-8):	Narzędzie do sprawdzania pakietów RPM pod kątem częstych błędów
Name:		rpmlint
Version:	1.9
Release:	1
License:	GPL v2
Group:		Development/Building
Source0:	https://github.com/rpm-software-management/rpmlint/archive/%{name}-%{version}.tar.gz
# Source0-md5:	810d7fd565d389fec305ff80af53ba40
Source1:	%{name}.config
Source3:	%{name}-etc.config
Patch0:		%{name}-groups.patch
Patch1:		pythonpath.patch
Patch2:		%{name}-licenses.patch
Patch3:		postshell.patch
Patch4:		rpm5.patch
Patch5:		bash-completion.patch
Patch6:		revert-9f71923e.patch
URL:		https://github.com/rpm-software-management/rpmlint
BuildRequires:	python >= 1:2.6
BuildRequires:	python-modules
%{?with_tests:BuildRequires:	python-rpm >= 5.4.10-12}
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.673
# tests require rpmlint in installed packages database
%{?with_tests:BuildRequires:	rpmlint}
Requires:	/bin/bash
Requires:	/lib/cpp
Requires:	binutils
Requires:	bzip2
Requires:	cpio
Requires:	desktop-file-utils
Requires:	file
Requires:	findutils
Requires:	grep
Requires:	gzip
Requires:	python >= 1.5.2
Requires:	python-magic
Requires:	python-pyenchant
Requires:	python-rpm >= 5.4.10-12
Requires:	xz
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Rpmlint is a tool to check common errors on rpm packages. Binary and
source packages can be checked.

%description -l pl.UTF-8
rpmlint to narzędzie do sprawdzania pakietów RPM pod kątem często
występujących błędów. Można sprawdzać pakiety źródłowe i binarne.

%package -n bash-completion-%{name}
Summary:	bash-completion for rpmlint
Summary(pl.UTF-8):	Bashowe uzupełnianie parametrów dla polecenia rpmlint
Group:		Applications/Shells
Requires:	%{name} = %{version}-%{release}
Requires:	bash-completion >= 2.0

%description -n bash-completion-%{name}
bash-completion for rpmlint.

%description -n bash-completion-%{name} -l pl.UTF-8
Bashowe uzupełnianie parametrów dla polecenia rpmlint.

%prep
%setup -q -n %{name}-rpmlint-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1

cp -p config config.example
cp -p %{SOURCE3} config

mv %{name} %{name}.py
%{__sed} -i -e 's,python ./rpmlint,./rpmlint.py,' test.sh

cat <<'EOF' > %{name}
#!/bin/sh
exec python -tt -u -O %{py_sitescriptdir}/%{name}/rpmlint.pyc "$@"
EOF
touch __init__.py

%build
# Create GROUPS for -groups.patch
rpmnv=$(rpm -q rpm --qf '%{N}-%{V}')
gzip -dc "%{_docdir}/$rpmnv/groups.gz" | awk '/^[A-Z].*/ { print }' > GROUPS
test -s GROUPS

%{__make} \
	bash_compdir=%{bash_compdir} \
	COMPILE_PYC=1

%if %{with tests}
%{__make} check
%endif

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	bash_compdir=%{bash_compdir} \
	ETCDIR=%{_sysconfdir} \
	MANDIR=%{_mandir} \
	LIBDIR=%{py_sitescriptdir}/%{name} \
	BINDIR=%{_bindir} \
	DESTDIR=$RPM_BUILD_ROOT

install -p %{name} $RPM_BUILD_ROOT%{_bindir}/%{name}
install -d $RPM_BUILD_ROOT%{_datadir}/%{name}
cp -p GROUPS $RPM_BUILD_ROOT%{_datadir}/%{name}
cp -p %{SOURCE1} $RPM_BUILD_ROOT%{_datadir}/%{name}/config

%py_ocomp $RPM_BUILD_ROOT%{py_sitescriptdir}
%py_comp $RPM_BUILD_ROOT%{py_sitescriptdir}
%py_postclean

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README* config.example
%dir %{_sysconfdir}/rpmlint
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/rpmlint/config
%attr(755,root,root) %{_bindir}/rpmdiff
%attr(755,root,root) %{_bindir}/rpmlint
%{_mandir}/man1/rpmdiff.1*
%{_mandir}/man1/rpmlint.1*
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/GROUPS
%{_datadir}/%{name}/config
%dir %{py_sitescriptdir}/%{name}
%{py_sitescriptdir}/%{name}/*.py[co]

%files -n bash-completion-%{name}
%defattr(644,root,root,755)
%{bash_compdir}/rpmlint
%{bash_compdir}/rpmdiff
