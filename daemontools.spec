Summary:	DJB daemontools
Name:		daemontools
Version:	0.53
Release:	1
Copyright:	D. J. Bernstein
Group:		Networking/Admin
Source: 	ftp://koobera.math.uic.edu/www/software/daemontools-0.53.tar.gz
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
supervise monitors a service. It starts the service and restarts the
service if it dies. The companion svc program stops, pauses, or restarts
the service on sysadmin request. The svstat program prints a one-line
status report.

cyclog writes a log to disk. It automatically synchronizes the log every
100KB (by default) to guarantee data integrity after a crash. It
automatically rotates the log to keep it below 1MB (by default). If the
disk fills up, cyclog pauses and then tries again, without losing any
data.

accustamp puts a precise timestamp on each line of input. The timestamp
is a numeric TAI timestamp with microsecond precision. The companion
tailocal program converts TAI timestamps to local time.

usually watches a log for lines that do not match specified patterns,
copying those lines to stderr. The companion errorsto program redirects
stderr to a file.

setuser runs a program under a user's uid and gid. Unlike su, setuser
does not gain privileges; it does not check passwords, and it cannot be
run except by root.

%prep
%setup -q

%build
echo %{_bindir} >conf-bin
echo %{_mandir} >conf-man

make; make man

%install
install -d		$RPM_BUILD_ROOT{%{_bindir},%{_mandir}/man1}

install accustamp	$RPM_BUILD_ROOT%{_bindir}
install cyclog 		$RPM_BUILD_ROOT%{_bindir}
install errorsto	$RPM_BUILD_ROOT%{_bindir}
install fifo		$RPM_BUILD_ROOT%{_bindir}
install supervise	$RPM_BUILD_ROOT%{_bindir}
install svc		$RPM_BUILD_ROOT%{_bindir}
install svstat		$RPM_BUILD_ROOT%{_bindir}
install tailocal	$RPM_BUILD_ROOT%{_bindir}
install testfilelock	$RPM_BUILD_ROOT%{_bindir}
install usually		$RPM_BUILD_ROOT%{_bindir}
install setuser		$RPM_BUILD_ROOT%{_bindir}
install *.1 		$RPM_BUILD_ROOT%{_mandir}/man1

gzip -9nf BLURB CHANGES INSTALL README THANKS TODO VERSION $RPM_BUILD_ROOT%{_mandir}/man1/*.1

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc {BLURB,CHANGES,INSTALL,README,THANKS,TODO,VERSION}.gz
%attr(644,root,root) %{_mandir}/*
%attr(755,root,root) %{_bindir}/*
