Summary:	D. J. Bernstein daemontools
Name:		daemontools
Version:	0.70
Release:	2
Copyright:	D. J. Bernstein
Group:		Networking/Admin
Group(pl):	Sieciowe/Administacyjne
Source0:	http://cr.yp.to/%{name}/%{name}-%{version}.tar.gz
Source1:	ftp://ftp.innominate.org/pub/pape/djb/%{name}-%{version}-man.tar.gz
Source2:	%{name}.sysconfig
Source3:        %{name}.init
Patch0:		daemontools-time.patch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
daemontools is a collection of tools for managing UNIX services.

supervise monitors a service. It starts the service and restarts the service if it dies.
Setting up a new service is easy: all supervise needs is a directory with a run script
that runs the service.

multilog saves error messages to one or more logs. It optionally timestamps each line and,
for each log, includes or excludes lines matching specified patterns. It automatically
rotates logs to limit the amount of disk space used. If the disk fills up, it pauses and
tries again, without losing any data.

%prep
tar zxf %{SOURCE1}

%setup -q
%patch0 -p1

%build
echo %{_bindir} >conf-home

make

%install
rm -rf $RPM_BUILD_ROOT

install -d		$RPM_BUILD_ROOT{%{_sbindir},%{_mandir}/man8}
install -d		$RPM_BUILD_ROOT/etc/{rc.d/init.d,sysconfig}
install	-d		$RPM_BUILD_ROOT/var/run/service
install -d		$RPM_BUILD_ROOT/var/lib/service

install envdir		$RPM_BUILD_ROOT%{_sbindir}
install envuidgid	$RPM_BUILD_ROOT%{_sbindir}
install fghack          $RPM_BUILD_ROOT%{_sbindir}
install multilog        $RPM_BUILD_ROOT%{_sbindir}
install setlock         $RPM_BUILD_ROOT%{_sbindir}
install setuidgid       $RPM_BUILD_ROOT%{_sbindir}
install softlimit       $RPM_BUILD_ROOT%{_sbindir}
install supervise	$RPM_BUILD_ROOT%{_sbindir}
install svc		$RPM_BUILD_ROOT%{_sbindir}
install svok		$RPM_BUILD_ROOT%{_sbindir}
install svscan		$RPM_BUILD_ROOT%{_sbindir}
install svstat		$RPM_BUILD_ROOT%{_sbindir}
install	tai64n		$RPM_BUILD_ROOT%{_sbindir}
install tai64nlocal	$RPM_BUILD_ROOT%{_sbindir}
install ../%{name}-%{version}-man/*.8 	$RPM_BUILD_ROOT%{_mandir}/man8
install %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/svscan
install %{SOURCE3} $RPM_BUILD_ROOT/etc/rc.d/init.d/svscan

gzip -9nf CHANGES README TODO VERSION $RPM_BUILD_ROOT%{_mandir}/man8/*.8

%clean
rm -rf $RPM_BUILD_ROOT
#rm -rf ../%{name}-%{version}-man

%post
/sbin/chkconfig --add svscan
if [ -f /var/lock/subsys/svscan ]; then
	/etc/rc.d/init.d/svscan restart >&2
else
	echo "Execute \"/etc/rc.d/init.d/svscan\" to start svscan daemon."
fi

%preun
if [ "$1" = "0" ]; then
	if [ -f /var/lock/subsys/svscan ]; then
		/etc/rc.d/init.d/svscan stop >&2
	fi
	/sbin/chkconfig --del svscan
fi

%files
%defattr(644,root,root,755)
%doc {CHANGES,README,TODO,VERSION}.gz
%attr(644,root,root) %{_mandir}/*
%attr(755,root,root) %{_sbindir}/*
%attr(700,root,root) /var/run/service
%attr(700,root,root) /var/lib/service
%attr(754,root,root) /etc/rc.d/init.d/svscan
%config(noreplace) %verify(not size mtime md5) /etc/sysconfig/svscan
