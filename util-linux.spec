Summary:	Collection of basic system utilities for Linux
Name:		util-linux
Version:	2.23.2
Release:	1
License:	GPL
Group:		Applications/System
Source0:	ftp://ftp.kernel.org/pub/linux/utils/util-linux/v2.23/%{name}-%{version}.tar.xz
# Source0-md5:	b39fde897334a4858bb2098edcce5b3f
Source2:	login.pamd
Source3:	su.pamd
Patch0:		%{name}-paths.patch
URL:		http://userweb.kernel.org/~kzak/util-linux-ng/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	gettext-devel
BuildRequires:	intltool
BuildRequires:	ncurses-devel
BuildRequires:	pam-devel
BuildRequires:	sed
BuildRequires:	texinfo
BuildRequires:	zlib-devel
Requires:	pam
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_localestatedir	/run

%description
util-linux contains a large variety of low-level system utilities
necessary for a functional Linux system. This includes, among other
things, configuration tools such as fdisk and system programs such as
logger.

%package -n libblkid
Summary:	Library to handle device identification and token extraction
License:	LGPL v2.1+
Group:		Libraries
Requires:	libuuid = %{version}-%{release}


%description -n libblkid
Library to handle device identification and token extraction.

%package -n libblkid-devel
Summary:	blkid library - development files
Group:		Development/Libraries
Requires:	libblkid = %{version}-%{release}

%description -n libblkid-devel
blkid library - development files.

%package -n libblkid-static
Summary:	blkid static library
Group:		Development/Libraries
Requires:	libblkid-devel = %{version}-%{release}

%package -n libmount
Summary:	Library to handle mounting-related tasks
License:	LGPL
Group:		Libraries
Requires:	libblkid = %{version}-%{release}

%description -n libmount
Library to handle mounting-related tasks.

%package -n libmount-devel
Summary:	Header files for mount library
License:	LGPL
Group:		Development/Libraries
Requires:	libblkid-devel = %{version}-%{release}
Requires:	libmount = %{version}-%{release}

%description -n libmount-devel
Header files for mount library.

%package -n libmount-static
Summary:	Static version of mount library
License:	LGPL
Group:		Development/Libraries
Requires:	libmount-devel = %{version}-%{release}

%description -n libmount-static
Static version of mount library.


%description -n libblkid-static
blkid static library.

%package -n libuuid
Summary:	Library for accessing and manipulating UUID
Group:		Libraries

%description -n libuuid
Library for accessing and manipulating UUID.

%package -n libuuid-devel
Summary:	Header files for library for accessing and manipulating UUID
Group:		Development/Libraries
Requires:	libuuid = %{version}-%{release}

%description -n libuuid-devel
Library for accessing and manipulating UUID - development files.

%package -n libuuid-static
Summary:	uuid static library
Group:		Development/Libraries
Requires:	libuuid-devel = %{version}-%{release}

%description -n libuuid-static
uuid static library.

%prep
%setup -qn %{name}-%{version}
%patch0 -p1

%build
%{__libtoolize}
%{__gettextize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
CPPFLAGS="%{rpmcppflags} -I/usr/include/ncurses"
export CPPFLAGS
%configure \
	--disable-silent-rules		\
	--disable-use-tty-group		\
	--enable-fs-paths-extra=/usr/bin:/usr/sbin	\
	--enable-socket-activation	\
	--enable-write			\
	--without-selinux
%{__make}

#%%{__make} check

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/{pam.d,sysconfig,security}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

sed -i -e 's,/usr/spool/mail,/var/mail,g' $RPM_BUILD_ROOT%{_mandir}/man1/login.1

install %{SOURCE2} $RPM_BUILD_ROOT/etc/pam.d/login
install %{SOURCE3} $RPM_BUILD_ROOT/etc/pam.d/su
install %{SOURCE3} $RPM_BUILD_ROOT/etc/pam.d/su-l

:> $RPM_BUILD_ROOT%{_sysconfdir}/blkid.tab

ln -sf hwclock $RPM_BUILD_ROOT%{_sbindir}/clock
echo '.so hwclock.8' > $RPM_BUILD_ROOT%{_mandir}/man8/clock.8

%find_lang %{name}

rm -f $RPM_BUILD_ROOT%{_infodir}/dir

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /usr/sbin/postshell
-/usr/sbin/fix-info-dir -c %{_infodir}

%postun	-p /usr/sbin/postshell
-/usr/sbin/fix-info-dir -c %{_infodir}

%post	-n libblkid -p /usr/sbin/ldconfig
%postun	-n libblkid -p /usr/sbin/ldconfig

%post	-n libmount -p /usr/sbin/ldconfig
%postun -n libmount -p /usr/sbin/ldconfig

%post	-n libuuid -p /usr/sbin/ldconfig
%postun	-n libuuid -p /usr/sbin/ldconfig

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc NEWS
%attr(2755,root,tty) %{_bindir}/write
%attr(4755,root,root) %{_bindir}/mount
%attr(4755,root,root) %{_bindir}/umount
%attr(755,root,root) %{_bindir}/cal
%attr(755,root,root) %{_bindir}/chrt
%attr(755,root,root) %{_bindir}/col
%attr(755,root,root) %{_bindir}/colcrt
%attr(755,root,root) %{_bindir}/colrm
%attr(755,root,root) %{_bindir}/column
%attr(755,root,root) %{_bindir}/cytune
%attr(755,root,root) %{_bindir}/dmesg
%attr(755,root,root) %{_bindir}/eject
%attr(755,root,root) %{_bindir}/fallocate
%attr(755,root,root) %{_bindir}/findmnt
%attr(755,root,root) %{_bindir}/flock
%attr(755,root,root) %{_bindir}/getopt
%attr(755,root,root) %{_bindir}/hexdump
%attr(755,root,root) %{_bindir}/i386
%attr(755,root,root) %{_bindir}/ionice
%attr(755,root,root) %{_bindir}/ipcmk
%attr(755,root,root) %{_bindir}/ipcrm
%attr(755,root,root) %{_bindir}/ipcs
%attr(755,root,root) %{_bindir}/isosize
%attr(755,root,root) %{_bindir}/kill
%attr(755,root,root) %{_bindir}/linux*
%attr(755,root,root) %{_bindir}/logger
%attr(755,root,root) %{_bindir}/login
%attr(755,root,root) %{_bindir}/look
%attr(755,root,root) %{_bindir}/lsblk
%attr(755,root,root) %{_bindir}/lscpu
%attr(755,root,root) %{_bindir}/lslocks
%attr(755,root,root) %{_bindir}/mcookie
%attr(755,root,root) %{_bindir}/more
%attr(755,root,root) %{_bindir}/mountpoint
%attr(755,root,root) %{_bindir}/namei
%attr(755,root,root) %{_bindir}/nsenter
%attr(755,root,root) %{_bindir}/pg
%attr(755,root,root) %{_bindir}/prlimit
%attr(755,root,root) %{_bindir}/rename
%attr(755,root,root) %{_bindir}/renice
%attr(755,root,root) %{_bindir}/rev
%attr(755,root,root) %{_bindir}/script
%attr(755,root,root) %{_bindir}/scriptreplay
%attr(755,root,root) %{_bindir}/setarch
%attr(755,root,root) %{_bindir}/setpriv
%attr(755,root,root) %{_bindir}/setsid
%attr(755,root,root) %{_bindir}/setterm
%attr(755,root,root) %{_bindir}/su
%attr(755,root,root) %{_bindir}/tailf
%attr(755,root,root) %{_bindir}/taskset
%attr(755,root,root) %{_bindir}/ul
%attr(755,root,root) %{_bindir}/unshare
%attr(755,root,root) %{_bindir}/utmpdump
%attr(755,root,root) %{_bindir}/wall
%attr(755,root,root) %{_bindir}/wdctl
%attr(755,root,root) %{_bindir}/whereis

%ifarch %{x8664}
%attr(755,root,root) %{_bindir}/x86_64
%{_mandir}/man8/x86_64*
%endif

%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/pam.d/login
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/pam.d/su
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/pam.d/su-l

%ghost %{_sysconfdir}/blkid.tab
%attr(755,root,root) %{_sbindir}/blkid
%attr(755,root,root) %{_sbindir}/addpart
%attr(755,root,root) %{_sbindir}/agetty
%attr(755,root,root) %{_sbindir}/blockdev
%attr(755,root,root) %{_sbindir}/cfdisk
%attr(755,root,root) %{_sbindir}/chcpu
%attr(755,root,root) %{_sbindir}/clock
%attr(755,root,root) %{_sbindir}/ctrlaltdel
%attr(755,root,root) %{_sbindir}/delpart
%attr(755,root,root) %{_sbindir}/fdformat
%attr(755,root,root) %{_sbindir}/fdisk
%attr(755,root,root) %{_sbindir}/findfs
%attr(755,root,root) %{_sbindir}/fsck
%attr(755,root,root) %{_sbindir}/fsck.cramfs
%attr(755,root,root) %{_sbindir}/fsck.minix
%attr(755,root,root) %{_sbindir}/fsfreeze
%attr(755,root,root) %{_sbindir}/fstrim
%attr(755,root,root) %{_sbindir}/hwclock*
%attr(755,root,root) %{_sbindir}/ldattach
%attr(755,root,root) %{_sbindir}/losetup
%attr(755,root,root) %{_sbindir}/mkfs
%attr(755,root,root) %{_sbindir}/mkfs.bfs
%attr(755,root,root) %{_sbindir}/mkfs.cramfs
%attr(755,root,root) %{_sbindir}/mkfs.minix
%attr(755,root,root) %{_sbindir}/mkswap
%attr(755,root,root) %{_sbindir}/partx
%attr(755,root,root) %{_sbindir}/pivot_root
%attr(755,root,root) %{_sbindir}/raw
%attr(755,root,root) %{_sbindir}/readprofile
%attr(755,root,root) %{_sbindir}/resizepart
%attr(755,root,root) %{_sbindir}/rtcwake
%attr(755,root,root) %{_sbindir}/sfdisk
%attr(755,root,root) %{_sbindir}/sulogin
%attr(755,root,root) %{_sbindir}/swaplabel
%attr(755,root,root) %{_sbindir}/swapoff
%attr(755,root,root) %{_sbindir}/swapon
%attr(755,root,root) %{_sbindir}/switch_root
%attr(755,root,root) %{_sbindir}/wipefs
%attr(755,root,root) %{_sbindir}/blkdiscard
%attr(755,root,root) %{_sbindir}/runuser

%{_mandir}/man1/cal.1*
%{_mandir}/man1/chrt.1*
%{_mandir}/man1/col.1*
%{_mandir}/man1/colcrt.1*
%{_mandir}/man1/colrm.1*
%{_mandir}/man1/column.1*
%{_mandir}/man1/dmesg.1*
%{_mandir}/man1/eject.1*
%{_mandir}/man1/fallocate.1*
%{_mandir}/man1/flock.1*
%{_mandir}/man1/getopt.1*
%{_mandir}/man1/hexdump.1*
%{_mandir}/man1/ionice.1*
%{_mandir}/man1/ipcmk.1*
%{_mandir}/man1/ipcrm.1*
%{_mandir}/man1/ipcs.1*
%{_mandir}/man1/kill.1*
%{_mandir}/man1/logger.1*
%{_mandir}/man1/login.1*
%{_mandir}/man1/look.1*
%{_mandir}/man1/lscpu.1*
%{_mandir}/man1/mcookie.1*
%{_mandir}/man1/more.1*
%{_mandir}/man1/mountpoint.1*
%{_mandir}/man1/namei.1*
%{_mandir}/man1/nsenter.1*
%{_mandir}/man1/pg.1*
%{_mandir}/man1/prlimit.1*
%{_mandir}/man1/rename.1*
%{_mandir}/man1/renice.1*
%{_mandir}/man1/rev.1*
%{_mandir}/man1/runuser.1*
%{_mandir}/man1/script.1*
%{_mandir}/man1/scriptreplay.1*
%{_mandir}/man1/setpriv.1*
%{_mandir}/man1/setsid.1*
%{_mandir}/man1/setterm.1*
%{_mandir}/man1/su.1*
%{_mandir}/man1/tailf.1*
%{_mandir}/man1/taskset.1*
%{_mandir}/man1/ul.1*
%{_mandir}/man1/unshare.1*
%{_mandir}/man1/utmpdump.1*
%{_mandir}/man1/wall.1*
%{_mandir}/man1/whereis.1*
%{_mandir}/man1/write.1*

%{_mandir}/man3/libblkid.3*

%{_mandir}/man5/fstab.5*

%{_mandir}/man8/addpart.8*
%{_mandir}/man8/agetty.8*
%{_mandir}/man8/blkdiscard.8*
%{_mandir}/man8/blkid.8*
%{_mandir}/man8/blockdev.8*
%{_mandir}/man8/cfdisk.8*
%{_mandir}/man8/chcpu.8*
%{_mandir}/man8/clock.8*
%{_mandir}/man8/ctrlaltdel.8*
%{_mandir}/man8/cytune.8*
%{_mandir}/man8/delpart.8*
%{_mandir}/man8/fdformat.8*
%{_mandir}/man8/fdisk.8*
%{_mandir}/man8/findfs.8*
%{_mandir}/man8/findmnt.8*
%{_mandir}/man8/fsck.8*
%{_mandir}/man8/fsck.cramfs.8*
%{_mandir}/man8/fsck.minix.8*
%{_mandir}/man8/fsfreeze.8*
%{_mandir}/man8/fstrim.8*
%{_mandir}/man8/hwclock.8*
%{_mandir}/man8/i386*
%{_mandir}/man8/isosize.8*
%{_mandir}/man8/ldattach.8*
%{_mandir}/man8/linux*
%{_mandir}/man8/losetup.8*
%{_mandir}/man8/lsblk.8*
%{_mandir}/man8/lslocks.8*
%{_mandir}/man8/mkfs.8*
%{_mandir}/man8/mkfs.bfs.8*
%{_mandir}/man8/mkfs.cramfs.8*
%{_mandir}/man8/mkfs.minix.8*
%{_mandir}/man8/mkswap.8*
%{_mandir}/man8/mount.8*
%{_mandir}/man8/partx.8*
%{_mandir}/man8/pivot_root.8*
%{_mandir}/man8/raw.8.gz
%{_mandir}/man8/readprofile.8*
%{_mandir}/man8/resizepart.8*
%{_mandir}/man8/rtcwake.8*
%{_mandir}/man8/setarch.8*
%{_mandir}/man8/sfdisk.8*
%{_mandir}/man8/sulogin.8*
%{_mandir}/man8/swaplabel.8*
%{_mandir}/man8/swapoff.8*
%{_mandir}/man8/swapon.8*
%{_mandir}/man8/switch_root.8*
%{_mandir}/man8/umount.8*
%{_mandir}/man8/uuidd.8*
%{_mandir}/man8/wdctl.8*
%{_mandir}/man8/wipefs.8*

%files -n libblkid
%defattr(644,root,root,755)
%attr(755,root,root) %ghost %{_libdir}/libblkid.so.?
%attr(755,root,root) %{_libdir}/libblkid.so.*.*.*

%files -n libblkid-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libblkid.so
%{_includedir}/blkid
%{_pkgconfigdir}/blkid.pc

%files -n libblkid-static
%defattr(644,root,root,755)
%{_libdir}/libblkid.a

%files -n libmount
%defattr(644,root,root,755)
%attr(755,root,root) %ghost %{_libdir}/libmount.so.?
%attr(755,root,root) %{_libdir}/libmount.so.*.*

%files -n libmount-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libmount.so
%{_includedir}/libmount
%{_pkgconfigdir}/mount.pc

%files -n libmount-static
%defattr(644,root,root,755)
%{_libdir}/libmount.a

%files -n libuuid
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/uuidgen
%attr(755,root,root) %ghost %{_libdir}/libuuid.so.?
%attr(755,root,root) %{_libdir}/libuuid.so.*.*.*
%{_mandir}/man1/uuidgen.1*

%files -n libuuid-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libuuid.so
%{_includedir}/uuid
%{_pkgconfigdir}/uuid.pc
%{_mandir}/man3/*uuid*

%files -n libuuid-static
%defattr(644,root,root,755)
%{_libdir}/libuuid.a

%if 0
%attr(755,root,root) %{_sbindir}/uuidd
/usr/lib/systemd/system/uuidd.service
/usr/lib/systemd/system/uuidd.socket
%endif

