# TODO
# - pldize initscript
# - install only needed stuff
# - fix paths
Summary:	A Cross Platform Monitoring Agent
Name:		nagios-ncpa
Version:	1.8.1
Release:	0.1
# License states that NCPA can be used only with Nagios LLC products (#6 in LICENSE.md)
License:	NOSL v1.3
Group:		Networking
URL:		https://assets.nagios.com/downloads/ncpa/docs/html/index.html
Source0:	https://github.com/NagiosEnterprises/ncpa/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	ee7e11c7ecc12ddd7bc4bc63a4308980
Requires:	nagios-common
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_appdir	%{_prefix}/lib/ncpa
%define		_sysconfdir	/etc/nagios

%description
Installs on your system with zero requirements and allows for
monitoring via Nagios.

%prep
%setup -q -n ncpa-%{version}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/etc/rc.d/init.d,%{_sysconfdir},%{_appdir}}

cp -a agent/* $RPM_BUILD_ROOT%{_appdir}
mv $RPM_BUILD_ROOT{%{_appdir}/etc/*,%{_sysconfdir}}

mv $RPM_BUILD_ROOT{%{_appdir}/build_resources/listener_init,/etc/rc.d/init.d/ncpa_listener}
mv $RPM_BUILD_ROOT{%{_appdir}/build_resources/passive_init,/etc/rc.d/init.d/ncpa_passive}

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add ncpa_listener
/sbin/chkconfig --add ncpa_passive
%service ncpa_listener restart
%service ncpa_passive restart

%preun
if [ "$1" = "0" ]; then
	/sbin/chkconfig --del ncpa_listener
	/sbin/chkconfig --del ncpa_passive
	%service ncpa_listener stop
	%service ncpa_passive stop
fi

%files
%defattr(644,root,root,755)
%doc CHANGES.rst CONTRIBUTING.rst README.rst VERSION.md LICENSE.md
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/ncpa.cfg
%dir %{_sysconfdir}/ncpa.cfg.d
%{_sysconfdir}/ncpa.cfg.d/README
%attr(754,root,root) /etc/rc.d/init.d/ncpa_listener
%attr(754,root,root) /etc/rc.d/init.d/ncpa_passive
%{_appdir}
