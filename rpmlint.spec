#
# Conditional build:
%bcond_without	tests		# build without tests
%bcond_with	rpm4		# build for rpm4

Summary:	Tool for checking common errors in RPM packages
Summary(pl.UTF-8):	Narzędzie do sprawdzania pakietów RPM pod kątem częstych błędów
Name:		rpmlint
Version:	1.11
Release:	1
License:	GPL v2
Group:		Development/Building
Source0:	https://github.com/rpm-software-management/rpmlint/archive/%{name}-%{version}.tar.gz
# Source0-md5:	2642bb6f08f6e2a2f2c0fe9f07634d49
Source1:	%{name}.config
Source3:	%{name}-etc.config
Patch0:		%{name}-groups.patch
Patch1:		pythonpath.patch
Patch2:		%{name}-licenses.patch
Patch3:		postshell.patch
Patch4:		rpm5.patch
Patch5:		bash-completion.patch
Patch6:		revert-9f71923e.patch
Patch7:		rpm4.15.patch
Patch8:		python3.patch
Patch9:		libc-warnings.patch
Patch10:	fix-tests.patch
URL:		https://github.com/rpm-software-management/rpmlint
%if %{with rpm4}
BuildRequires:	python3
BuildRequires:	python3-modules
%if %{with tests}
BuildRequires:	python3-pytest
BuildRequires:	python3-flake8
BuildRequires:	python3-rpm >= 1:4.16
%endif
%else
BuildRequires:	python >= 1:2.6
BuildRequires:	python-modules
%if %{with tests}
BuildRequires:	python-flake8
BuildRequires:	python-pytest
BuildRequires:	python-rpm >= 5.4.10-12}
%endif
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.673
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
%if %{with rpm4}
Requires:	python3
Requires:	python3-magic
Requires:	python3-pyenchant
Requires:	python3-rpm >= 1:4.16
%else
Requires:	python >= 1.5.2
Requires:	python-magic
Requires:	python-pyenchant
Requires:	python-rpm >= 5.4.10-12
%endif
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
%{!?with_rpm4:%patch0 -p1}
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch5 -p1
%if %{with rpm4}
%patch7 -p1
%patch8 -p1
%else
%patch4 -p1
%patch6 -p1
%endif
%patch9 -p1
%patch10 -p1

cp -p config config.example
cp -p %{SOURCE3} config

touch __init__.py
%if %{with rpm4}
%{__sed} -i -e '1s,/usr/bin/python,%{__python3},' rpmdiff rpmlint
%else
%{__sed} -i -e '1s,/usr/bin/python,%{__python},' rpmdiff rpmlint
# this syntax is not supported by rpm5?
%{__rm} test/test.CheckInclude.py test/test_tags.py
%endif

%build
%if %{without rpm4}
# Create GROUPS for -groups.patch
rpmnv=$(rpm -q rpm --qf '%{N}-%{V}')
gzip -dc "%{_docdir}/$rpmnv/groups.gz" | awk '/^[A-Z].*/ { print }' > GROUPS
test -s GROUPS
%endif

%{__make} \
	bash_compdir=%{bash_compdir} \
%if %{with rpm4}
	PYTHON=%{__python3} \
%else
	PYTHON=%{__python} \
%endif
	COMPILE_PYC=1

%if %{with tests}
%{__make} check \
%if %{with rpm4}
	PYTHON=%{__python3} \
	PYTEST=py.test-3 \
	FLAKE8=flake8-3 \
%else
	PYTHON=%{__python} \
	PYTEST=py.test \
	FLAKE8=flake8-2 \
%endif
%endif

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	bash_compdir=%{bash_compdir} \
%if %{with rpm4}
	PYTHON=%{__python3} \
	LIBDIR=%{py3_sitescriptdir}/%{name} \
%else
	PYTHON=%{__python} \
	LIBDIR=%{py_sitescriptdir}/%{name} \
%endif
	ETCDIR=%{_sysconfdir} \
	MANDIR=%{_mandir} \
	BINDIR=%{_bindir} \
	DESTDIR=$RPM_BUILD_ROOT

%if %{with rpm4}
%{__mv} $RPM_BUILD_ROOT%{_bindir}/rpmlint $RPM_BUILD_ROOT%{py3_sitescriptdir}/%{name}/rpmlint.py
cat <<'EOF' > $RPM_BUILD_ROOT%{_bindir}/rpmlint
#!/bin/sh
exec %{__python3} -tt -u -O %{py3_sitescriptdir}/%{name}/rpmlint.py "$@"
EOF
%else
%{__mv} $RPM_BUILD_ROOT%{_bindir}/rpmlint $RPM_BUILD_ROOT%{py_sitescriptdir}/%{name}/rpmlint.py
cat <<'EOF' > $RPM_BUILD_ROOT%{_bindir}/rpmlint
#!/bin/sh
exec %{__python} -tt -u -O %{py_sitescriptdir}/%{name}/rpmlint.pyc "$@"
EOF
%endif

install -d $RPM_BUILD_ROOT%{_datadir}/%{name}
cp -p %{SOURCE1} $RPM_BUILD_ROOT%{_datadir}/%{name}/config
%{!?with_rpm4:cp -p GROUPS $RPM_BUILD_ROOT%{_datadir}/%{name}}

%if %{without rpm4}
%py_ocomp $RPM_BUILD_ROOT%{py_sitescriptdir}
%py_comp $RPM_BUILD_ROOT%{py_sitescriptdir}
%py_postclean
%endif

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
%{_datadir}/%{name}/config
%if %{with rpm4}
%dir %{py3_sitescriptdir}/%{name}
%{py3_sitescriptdir}/%{name}/__pycache__
%{py3_sitescriptdir}/%{name}/*.py
%else
%dir %{py_sitescriptdir}/%{name}
%{py_sitescriptdir}/%{name}/*.py[co]
%{_datadir}/%{name}/GROUPS
%endif

%files -n bash-completion-%{name}
%defattr(644,root,root,755)
%{bash_compdir}/rpmlint
%{bash_compdir}/rpmdiff
