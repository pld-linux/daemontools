Summary:	D. J. Bernstein daemontools
Name:		daemontools
Version:	0.70
Release:	2
Copyright:	D. J. Bernstein
Group:		Networking/Admin
Group(de):	Netzwerkwesen/Administration
Group(pl):	Sieciowe/Administracyjne
Source0:	http://cr.yp.to/%{name}/%{name}-%{version}.tar.gz
Source1:	ftp://ftp.innominate.org/pub/pape/djb/%{name}-%{version}-man.tar.gz
Source2:	%{name}.sysconfig
Patch0:		%{name}-time.patch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
daemontools is a collection of tools for managing UNIX services.

supervise monitors a service. It starts the service and restarts the
service if it dies. Setting up a new service is easy: all supervise
needs is a directory with a run script that runs the service.

multilog saves error messages to one or more logs. It optionally
timestamps each line and, for each log, includes or excludes lines
matching specified patterns. It automatically rotates logs to limit
the amount of disk space used. If the disk fills up, it pauses and
tries again, without losing any data.

%prep
tar zxf %{SOURCE1}

%setup -q
%patch0 -p1

%build
echo %{_bindir} >conf-home

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sbindir},%{_mandir}/man8} \
$RPM_BUILD_ROOT%{_sysconfdir}/{rc.d/init.d,sysconfig} \
	$RPM_BUILD_ROOT/var/{run/service,lib/service}

install envdir envuidgid fghack multilog setlock setuidgid softlimit \
	supervise supervise svc svok svscan svstat tai64n tai64nlocal \
	$RPM_BUILD_ROOT%{_sbindir}
install ../%{name}-%{version}-man/*.8 $RPM_BUILD_ROOT%{_mandir}/man8
install %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/svscan
install %{SOURCE3} $RPM_BUILD_ROOT/etc/rc.d/init.d/svscan

gzip -9nf CHANGES README TODO

%clean
rm -rf $RPM_BUILD_ROOT

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
%doc *.gz
%attr(755,root,root) %{_sbindir}/*
%attr(700,root,root) /var/run/service
%attr(700,root,root) /var/lib/service
%attr(754,root,root) /etc/rc.d/init.d/svscan
%config(noreplace) %verify(not size mtime md5) /etc/sysconfig/svscan
%{_mandir}/man8/*
