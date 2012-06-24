Summary:	RPM correctness checker
Summary(pl):	Narz�dzie do sprawdzania poprawno�ci pakiet�w RPM
Name:		rpmlint
Version:	0.71
Release:	1
License:	GPL v2
Group:		Development/Building
Source0:	http://people.mandriva.com/~flepied/projects/rpmlint/dist/%{name}-%{version}.tar.bz2
# Source0-md5:	9e7645ee79bfc75540c885f05dca0751
Patch0:		%{name}-groups.patch
Patch1:		%{name}-config.patch
URL:		http://people.mandriva.com/~flepied/projects/rpmlint/
BuildRequires:	python >= 1.5.2
BuildRequires:	rpm-devel >= 4.4.1
Requires:	/bin/bash
Requires:	/lib/cpp
Requires:	binutils
Requires:	cpio
Requires:	file
Requires:	findutils
Requires:	grep
Requires:	python-rpm
Requires:	python >= 1.5.2
Requires:	rpm-devel
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Rpmlint is a tool to check common errors on rpm packages. Binary and
source packages can be checked.

%description -l pl
rpmlint to narz�dzie do sprawdzania pakiet�w RPM pod k�tem cz�sto
wyst�puj�cych b��d�w. Mo�na sprawdza� pakiety �r�d�owe i binarne.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

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
%doc AUTHORS ChangeLog README*
%attr(755,root,root) %{_bindir}/*
%{_datadir}/rpmlint
%dir %{_sysconfdir}/rpmlint
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/rpmlint/config
