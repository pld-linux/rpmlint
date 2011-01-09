Summary:	Tool for checking common errors in RPM packages
Name:		rpmlint
Version:	1.0
Release:	1
License:	GPL v2
Group:		Development/Building
Source0:	http://rpmlint.zarb.org/download/%{name}-%{version}.tar.bz2
# Source0-md5:	c27b574f3e70a3ffeb8eeb550e597c2d
Patch0:		%{name}-groups.patch
Patch1:		%{name}-config.patch
Patch2:		%{name}-licenses.patch
Patch3:		rpm-compat.patch
Patch4:		pythonpath.patch
URL:		http://rpmlint.zarb.org/
BuildRequires:	python >= 1.5.2
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
Requires:	python-rpm
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
Group:		Applications/Shells
Requires:	%{name} = %{version}-%{release}
Requires:	bash-completion

%description -n bash-completion-%{name}
bash-completion for rpmlint.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1

cat <<'EOF' > rpmlint
#!/bin/sh
exec python -tt -u -O %{py_sitescriptdir}/%{name}/rpmlint.pyc "$@"
EOF
touch __init__.py

%build
# Create GROUPS for -groups.patch
rpm --qf '%{_docdir}/%{N}-%{V}/groups.gz' -q rpm | xargs gzip -dc | awk '/^[A-Z].*/ { print }' > GROUPS

%{__make} \
	COMPILE_PYC=1

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	ETCDIR=%{_sysconfdir} \
	MANDIR=%{_mandir} \
	LIBDIR=%{py_sitescriptdir}/%{name} \
	BINDIR=%{_bindir} \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_datadir}/%{name}
cp -a GROUPS $RPM_BUILD_ROOT%{_datadir}/%{name}

%py_ocomp $RPM_BUILD_ROOT%{py_sitescriptdir}
%py_comp $RPM_BUILD_ROOT%{py_sitescriptdir}
%py_postclean

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog README*
%dir %{_sysconfdir}/rpmlint
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/rpmlint/config
%attr(755,root,root) %{_bindir}/rpmdiff
%attr(755,root,root) %{_bindir}/rpmlint
%{_mandir}/man1/rpmlint.1*
%dir %{_datadir}/rpmlint
%{_datadir}/rpmlint/GROUPS
%dir %{py_sitescriptdir}/rpmlint
%{py_sitescriptdir}/rpmlint/*.py[co]

%files -n bash-completion-%{name}
%defattr(644,root,root,755)
/etc/bash_completion.d/rpmlint
