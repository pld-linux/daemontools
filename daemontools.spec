Summary:	D. J. Bernstein daemontools
Summary(pl.UTF-8):	daemontools D. J. Bernsteina
Name:		daemontools
Version:	0.76
Release:	14
License:	Public Domain
Group:		Networking/Admin
Source0:	http://cr.yp.to/daemontools/%{name}-%{version}.tar.gz
# Source0-md5:	1871af2453d6e464034968a0fbcb2bfc
Source1:	http://smarden.org/pape/djb/manpages/%{name}-%{version}-man.tar.gz
# Source1-md5:	2d3858a48f293c87202f76cd883438ee
Source2:	%{name}.sysconfig
Source3:	%{name}.init
Patch0:		%{name}-glibc.patch
URL:		http://cr.yp.to/daemontools.html
BuildRequires:	rpmbuild(macros) >= 1.268
Requires(post,preun):	/sbin/chkconfig
Requires:	rc-scripts >= 0.4.3.0
Conflicts:	ucspi-tcp < 0.88-7
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

%description -l pl.UTF-8
daemontools to zestaw narzędzi do zarządzania usługami uniksowymi.

supervise monitoruje usługi. Startuje usługi i restartuje je, gdy
umrą. Ustawienie nowej usługi jest proste: wszystko czego supervise
potrzebuje to katalog ze skryptami startowymi, które startują usługi.

multilog zapisuje komunikaty o błędach do jednego lub większej liczby
plików logów. Opcjonalnie oznacza każdą linię datą oraz, w każdym
logu, dołącza lub pomija linie pasujące do określonych wzorców.
Automatycznie wykonuje rotację logów do limitu miejsca na dysku.
Jeżeli dysk jest zapełniony, pauzuje i próbuje ponownie, bez strat
danych.

%prep
%setup -q -c -a1
mv admin/daemontools-%{version}/* .
cd src
%patch0 -p0

%build
echo "%{__cc} %{rpmcflags} -Wall" > src/conf-cc
echo "%{__cc} %{rpmldflags}" > src/conf-ld
./package/compile

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sbindir},%{_mandir}/man8} \
	$RPM_BUILD_ROOT/etc/{rc.d/init.d,sysconfig} \
	$RPM_BUILD_ROOT%{_sysconfdir}/supervise \
	$RPM_BUILD_ROOT{/var/lib/service,%{servicedir}}

# install manuals
cp -p %{name}-man/*.8* $RPM_BUILD_ROOT%{_mandir}/man8

# install binaries
cd command
install -p envdir envuidgid fghack multilog pgrphack \
	readproctitle setlock setuidgid softlimit \
	supervise svc svok svscan svscanboot svstat tai64n tai64nlocal \
	$RPM_BUILD_ROOT%{_sbindir}

# install rc & sysconfig files
cp -p %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/svscan
install -p %{SOURCE3} $RPM_BUILD_ROOT/etc/rc.d/init.d/svscan

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add svscan
%service svscan restart

%preun
if [ "$1" = "0" ]; then
	%service svscan stop
	/sbin/chkconfig --del svscan
fi

%files
%defattr(644,root,root,755)
%doc package/README src/{CHANGES,TODO}
%attr(755,root,root) %{_sbindir}/envdir
%attr(755,root,root) %{_sbindir}/envuidgid
%attr(755,root,root) %{_sbindir}/fghack
%attr(755,root,root) %{_sbindir}/multilog
%attr(755,root,root) %{_sbindir}/pgrphack
%attr(755,root,root) %{_sbindir}/readproctitle
%attr(755,root,root) %{_sbindir}/setlock
%attr(755,root,root) %{_sbindir}/setuidgid
%attr(755,root,root) %{_sbindir}/softlimit
%attr(755,root,root) %{_sbindir}/supervise
%attr(755,root,root) %{_sbindir}/svc
%attr(755,root,root) %{_sbindir}/svok
%attr(755,root,root) %{_sbindir}/svscan
%attr(755,root,root) %{_sbindir}/svscanboot
%attr(755,root,root) %{_sbindir}/svstat
%attr(755,root,root) %{_sbindir}/tai64n
%attr(755,root,root) %{_sbindir}/tai64nlocal
%attr(700,root,root) %{servicedir}
%dir %{_sysconfdir}/supervise
%attr(700,root,root) /var/lib/service
%attr(754,root,root) /etc/rc.d/init.d/svscan
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/svscan
%{_mandir}/man8/envdir.8*
%{_mandir}/man8/envuidgid.8*
%{_mandir}/man8/fghack.8*
%{_mandir}/man8/multilog.8*
%{_mandir}/man8/pgrphack.8*
%{_mandir}/man8/readproctitle.8*
%{_mandir}/man8/setlock.8*
%{_mandir}/man8/setuidgid.8*
%{_mandir}/man8/softlimit.8*
%{_mandir}/man8/supervise.8*
%{_mandir}/man8/svc.8*
%{_mandir}/man8/svok.8*
%{_mandir}/man8/svscan.8*
%{_mandir}/man8/svscanboot.8*
%{_mandir}/man8/svstat.8*
%{_mandir}/man8/tai64n.8*
%{_mandir}/man8/tai64nlocal.8*
