Summary:	RPM correctness checker
Summary(pl):	Narzêdzie do sprawdzania poprawno¶ci pakietów RPM
Name:		rpmlint
Version:	0.68
Release:	1
License:	GPL
Group:		Development/Building
Source0:	http://people.mandrakesoft.com/~flepied/projects/rpmlint/dist/%{name}-%{version}.tar.bz2
# Source0-md5:	e321c9868b403366d314c77e637e09b9
URL:		http://people.mandrakesoft.com/~flepied/projects/rpmlint/
BuildRequires:	python >= 1.5.2
BuildRequires:	rpm-devel
Requires:	/bin/bash
Requires:	/lib/cpp
Requires:	binutils
Requires:	cpio
Requires:	file
Requires:	findutils
Requires:	grep
Requires:	python >= 1.5.2
Requires:	python-rpm
Requires:	rpm-devel
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Rpmlint is a tool to check common errors on rpm packages. Binary and
source packages can be checked.

%description -l pl
rpmlint to narzêdzie do sprawdzania pakietów RPM pod k±tem czêsto
wystêpuj±cych b³êdów. Mo¿na sprawdzaæ pakiety ¼ród³owe i binarne.

%prep
%setup -q

%build
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc ChangeLog README*
%attr(755,root,root) %{_bindir}/*
%{_datadir}/rpmlint
%dir %{_sysconfdir}/rpmlint
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/rpmlint/config
