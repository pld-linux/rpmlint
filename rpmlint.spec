#
# Conditional build:
%bcond_with	tests		# build without tests

Summary:	Tool for checking common errors in RPM packages
Summary(pl.UTF-8):	Narzędzie do sprawdzania pakietów RPM pod kątem częstych błędów
Name:		rpmlint
Version:	2.6.1
Release:	1
License:	GPL v2
Group:		Development/Building
Source0:	https://github.com/rpm-software-management/rpmlint/archive/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	767e7fa006cb7cbc7101a867d57de6a1
Source1:	licenses.toml
Source2:	pld.toml
Source3:	scoring.toml
Source4:	users-groups.toml
URL:		https://github.com/rpm-software-management/rpmlint
BuildRequires:	python3
BuildRequires:	python3-modules
%if %{with tests}
BuildRequires:	python3-flake8
BuildRequires:	python3-pytest
BuildRequires:	python3-rpm >= 1:4.16
BuildRequires:	python3-setuptools
BuildRequires:	python3-zstd
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.673
Requires:	/bin/bash
Requires:	/lib/cpp
Requires:	binutils
Requires:	bzip2
Requires:	checkbashisms
Requires:	cpio
Requires:	dash
Requires:	desktop-file-utils
Requires:	file
Requires:	findutils
Requires:	grep
Requires:	gzip
Requires:	python3
Requires:	python3-magic
Requires:	python3-pyenchant
Requires:	python3-rpm >= 1:4.16
Requires:	xz
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Rpmlint is a tool to check common errors on rpm packages. Binary and
source packages can be checked.

%description -l pl.UTF-8
rpmlint to narzędzie do sprawdzania pakietów RPM pod kątem często
występujących błędów. Można sprawdzać pakiety źródłowe i binarne.

%prep
%setup -q

%build
%py3_build %{?with_tests:test}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_sysconfdir}/xdg/rpmlint

%py3_install

cp -p %{SOURCE1} %{SOURCE2} %{SOURCE3} %{SOURCE4} \
	$RPM_BUILD_ROOT%{_sysconfdir}/xdg/rpmlint

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README*
%dir %{_sysconfdir}/xdg/rpmlint
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/xdg/rpmlint/*.toml
%attr(755,root,root) %{_bindir}/rpmdiff
%attr(755,root,root) %{_bindir}/rpmlint
%dir %{py3_sitescriptdir}/rpmlint
%{py3_sitescriptdir}/rpmlint/configdefaults.toml
%{py3_sitescriptdir}/rpmlint/*.py
%{py3_sitescriptdir}/rpmlint/__pycache__
%dir %{py3_sitescriptdir}/rpmlint/checks
%{py3_sitescriptdir}/rpmlint/checks/*.py
%{py3_sitescriptdir}/rpmlint/checks/__pycache__
%dir %{py3_sitescriptdir}/rpmlint/descriptions
%{py3_sitescriptdir}/rpmlint/descriptions/*.toml
%{py3_sitescriptdir}/rpmlint-%{version}-py*.egg-info
