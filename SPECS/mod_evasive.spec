# apxs script location
%{!?_httpd_apxs: %global _httpd_apxs %{_bindir}/apxs}

# Module Magic Number
%{!?_httpd_mmn: %global _httpd_mmn %(cat %{_includedir}/httpd/.mmn 2>/dev/null || echo missing-httpd-devel)}

# Configuration directory
%{!?_httpd_confdir: %global _httpd_confdir %{_sysconfdir}/httpd/conf.d}
%{!?_httpd_moddir: %global _httpd_moddir %{_libdir}/httpd/modules}
%{!?_fail2ban_confdir: %global _fail2ban_confdir %{_sysconfdir}/fail2ban/filter.d}

%global httpd24 1
%global rundir /run

Name:		mod_evasive
Version:	2.1
Release:	2%{?dist}
Summary:	Realtime blacklist module for Apache 2
Group:		System Environment/Daemons
License:	GPL 2.0
URL:		https://github.com/apisnetworks/mod_evasive
Source0:  mod_evasive.c
Source1:  evasive.conf
Source2:  apache-modevasive.conf
Source3:  README.md
Source4:  LICENSE
Source5:  CHANGELOG
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(id -nu)
BuildRequires:	httpd-devel >= 2.4, pkgconfig, fail2ban
Requires:	httpd-mmn = %{_httpd_mmn}

%description
mod_evasive is an evasive maneuvers module for Apache to provide evasive action 
in the event of an HTTP DoS or DDoS attack or brute force attack. 
It is also designed to be a detection tool, and can be easily configured to 
talk to ipchains, firewalls, routers, and etcetera.

%prep
cp -p %{SOURCE0} mod_evasive.c
cp -p %{SOURCE1} evasive.conf
cp -p %{SOURCE2} apache-modevasive.conf
cp -p %{SOURCE3} README.md
cp -p %{SOURCE4} LICENSE
cp -p %{SOURCE5} CHANGELOG

%build
%{_httpd_apxs} -c -Wc,"%{optflags} -Wall -pedantic -std=c99" mod_evasive.c

%install
rm -rf $RPM_BUILD_ROOT
install -Dm 755 .libs/mod_evasive.so $RPM_BUILD_ROOT%{_httpd_moddir}/mod_evasive.so
install -Dp -m 0644 evasive.conf $RPM_BUILD_ROOT%{_httpd_confdir}/evasive.conf
install -Dp -m 0644 apache-modevasive.conf $RPM_BUILD_ROOT%{_fail2ban_confdir}/apache-modevasive.conf

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc README.md LICENSE CHANGELOG
%config(noreplace) %{_httpd_confdir}/evasive.conf
%config(noreplace) %{_fail2ban_confdir}/apache-modevasive.conf
%{_httpd_moddir}/*.so

%changelog
* Sun Jan 13 2019 Matt Saladna <matt@apisnetworks.com> - 2.1-2
- Bump baseline site count to 300/4 seconds

* Fri Dec 14 2018 Matt Saladna <matt@apisnetworks.com> - 2.1-1
- ISE on exec()

* Sun Dec 02 2018 Matt Saladna <matt@apisnetworks.com> - 2.1-0
- Merge custom HTTP status, per-virtualhost patch from jvdmr/mod_evasive
- Improve bot penetration tracking with global hash table per process instead of per server rec
- Shorten hash markers
- Invert whitelist class resolution D -> C -> B -> A
- Send no-cache header when blocked

* Sun Apr 08 2018 Matt Saladna <matt@apisnetworks.com> - 2.0-0
- Initial release
