Summary:	D. J. Bernstein daemontools
Summary(pl):	daemontools D. J. Bernsteina
Name:		daemontools
Version:	0.76
Release:	1
License:	DJB (http://cr.yp.to/distributors.html)
Group:		Networking/Admin
Source0:	http://cr.yp.to/%{name}/%{name}-%{version}.tar.gz
Source1:	http://smarden.org/pape/djb/manpages/%{name}-%{version}-man.tar.gz
Source2:	%{name}.sysconfig
Source3:	%{name}.init
Patch0:		%{name}-glibc.patch
URL:		http://cr.yp.to/daemontools.html
Requires(post,preun):	/sbin/chkconfig
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# /etc/service or /var/lib/service? (also in .sysconfig)
%define		servicedir	/service

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

%description -l pl
daemontools to zestaw narzêdzi do zarz±dzania us³ugami uniksowymi.

supervise monitoruje us³ugi. Startuje us³ugi i restartuje je, gdy
umr±. Ustawienie nowej us³ugi jest proste: wszystko czego supervise
potrzebuje to katalog ze skryptami startowymi, które startuj± us³ugi.

multilog zapisuje komunikaty o b³êdach do jednego lub wiêkszej liczby
plików logów. Opcjonalnie oznacza ka¿d± liniê dat± oraz, w ka¿dym
logu, do³±cza lub pomija linie pasuj±ce do okre¶lonych wzorców.
Automatycznie wykonuje rotacjê logów do limitu miejsca na dysku.
Je¿eli dysk jest zape³niony, pauzuje i próbuje ponownie, bez strat
danych.

%prep
%setup -q -n admin -a1
cd %{name}-%{version}/src
%patch0 -p0

%build
cd %{name}-%{version}
echo "%{__cc} %{rpmcflags} -Wall" >src/conf-cc
echo "%{__cc} %{rpmldflags}" >src/conf-ld

package/compile

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sbindir},%{_mandir}/man8} \
	$RPM_BUILD_ROOT/etc/{rc.d/init.d,sysconfig} \
	$RPM_BUILD_ROOT{/var/lib/service,%{servicedir}}

# install manuals
install %{name}-man/*.8* $RPM_BUILD_ROOT%{_mandir}/man8

# install binaries
cd %{name}-%{version}/command
install envdir envuidgid fghack multilog pgrphack \
	readproctitle setlock setuidgid softlimit \
	supervise svc svok svscan svscanboot svstat tai64n tai64nlocal \
	$RPM_BUILD_ROOT%{_sbindir}

# install rc & sysconfig files
install %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/svscan
install %{SOURCE3} $RPM_BUILD_ROOT/etc/rc.d/init.d/svscan

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add svscan
if [ -f /var/lock/subsys/svscan ]; then
	/etc/rc.d/init.d/svscan restart >&2
else
	echo "Execute \"/etc/rc.d/init.d/svscan start\" to start svscan daemon."
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
%doc %{name}-%{version}/{package/README,src/{CHANGES,TODO}}
%attr(755,root,root) %{_sbindir}/*
%attr(700,root,root) %{servicedir}
%attr(700,root,root) /var/lib/service
%attr(754,root,root) /etc/rc.d/init.d/svscan
%config(noreplace) %verify(not size mtime md5) /etc/sysconfig/svscan
%{_mandir}/man8/*
