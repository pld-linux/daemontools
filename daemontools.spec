$Revision: 1.1 $
Summary: DJB daemontools
Name: daemontools
Version: 0.53
Release: 1
Copyright: D. J. Bernstein
Group: Networking/Admin
Source: ftp://koobera.math.uic.edu/www/software/daemontools-0.53.tar.gz
Patch0: daemontools-0.53.redhat.patch
Buildroot: /var/tmp/daemontools-root

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
%setup
%patch0 -p1

%build
make; make man

%install
mkdir -p $RPM_BUILD_ROOT/usr/{bin,man/man1}
install -s -m 755 accustamp cyclog errorsto fifo supervise svc svstat tailocal testfilelock usually $RPM_BUILD_ROOT/usr/bin
install -s -m 700 setuser $RPM_BUILD_ROOT/usr/bin
install -m 644 accustamp.1 cyclog.1 errorsto.1 fifo.1 setuser.1 supervise.1 svc.1 svstat.1 tailocal.1 testfilelock.1 usually.1 $RPM_BUILD_ROOT/usr/man/man1

%clean
rm -rf $RPM_BUILD_ROOT

%files
%doc BLURB CHANGES INSTALL README THANKS TODO VERSION
/usr/bin/accustamp
/usr/bin/cyclog
/usr/bin/errorsto
/usr/bin/fifo
/usr/bin/supervise
/usr/bin/svc
/usr/bin/svstat
/usr/bin/tailocal
/usr/bin/testfilelock
/usr/bin/usually
/usr/bin/setuser
/usr/man/man1/accustamp.1
/usr/man/man1/cyclog.1
/usr/man/man1/errorsto.1
/usr/man/man1/fifo.1
/usr/man/man1/setuser.1
/usr/man/man1/supervise.1
/usr/man/man1/svc.1
/usr/man/man1/svstat.1
/usr/man/man1/tailocal.1
/usr/man/man1/testfilelock.1
/usr/man/man1/usually.1
