%include	/usr/lib/rpm/macros.python
Summary:	Rpm correctness checker
Name:		rpmlint
Version:	0.46
Release:	0.1
Source0:	http://people.mandrakesoft.com/~flepied/projects/rpmlint/dist/%{name}-%{version}.tar.bz2
URL:		http://people.mandrakesoft.com/~flepied/projects/rpmlint/
License:	GPL
Group:		Development/Building
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
BuildRequires:	rpm-pythonprov
BuildRequires:	python >= 1.5.2, rpm-devel, make
Requires:	python >= 1.5.2, rpm-devel, binutils, file, findutils, cpio, /lib/cpp, grep, /bin/bash
BuildArch:	noarch

%description
Rpmlint is a tool to check common errors on rpm packages. Binary and
source packages can be checked.

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
%doc COPYING ChangeLog INSTALL README*
%attr(755,root,root) %{_bindir}/*
%{_datadir}/rpmlint
%config(noreplace) %{_sysconfdir}/rpmlint/config
%dir %{_sysconfdir}/rpmlint
