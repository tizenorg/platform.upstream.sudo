Name:           sudo
Version:        1.8.10p3
Release:        0
Summary:        Execute some commands as root
License:        ISC
Group:          System/Utilities
Url:            http://www.sudo.ws/
Source0:        http://sudo.ws/sudo/dist/%{name}-%{version}.tar.gz
Source1:        sudo.pamd
Source1001:     sudo.manifest
BuildRequires:  groff
BuildRequires:  pam-devel
Requires(pre):  coreutils

%description
Sudo is a command that allows users to execute some commands as root.
The /etc/sudoers file (edited with 'visudo') specifies which users have
access to sudo and which commands they can run. Sudo logs all its
activities to syslogd, so the system administrator can keep an eye on
things. Sudo asks for the password for initializing a check period of a
given time N (where N is defined at installation and is set to 5
minutes by default).

%package devel
Summary:        Header files needed for sudo plugin development
Group:          System/Utilities

%description devel
These header files are needed for building of sudo plugins.

%package rpm
Summary:        Script making possible to run RPM as root from inside build
Group:          System/Utilities
Requires:       sudo

%description rpm
The package will add ALL ALL = (root) NOPASSWD: /usr/bin/rpm to sudoers and
makes possible to install packages from inside build.

%prep
%setup -q
cp %{SOURCE1001} .

%build
export CFLAGS+=" -fvisibility=hidden"
  export CXXFLAGS+=" -fvisibility=hidden"
  
F_PIE=-fpie
export CFLAGS="%{optflags} -Wall $F_PIE -DLDAP_DEPRECATED"
export LDFLAGS="-pie"
%configure \
--libexecdir=%{_libexecdir}/sudo \
--docdir=%{_docdir}/%{name} \
--with-noexec=%{_libexecdir}/sudo/sudo_noexec.so \
--with-pam \
--with-logfac=auth \
--without-insults \
--with-ignore-dot \
--with-tty-tickets \
--enable-shell-sets-home \
--enable-warnings \
--with-sudoers-mode=0440 \
--with-env-editor \
--without-secure-path \
--with-passprompt='%%p\x27s password:' \
--with-rundir=%{_localstatedir}/lib/sudo
%__make %{?_smp_mflags}

%install
%make_install
install -d -m 755 %{buildroot}%{_sysconfdir}/pam.d
install -m 644 %{SOURCE1} %{buildroot}%{_sysconfdir}/pam.d/sudo
rm -f %{buildroot}%{_bindir}/sudoedit
ln -sf %{_bindir}/sudo %{buildroot}%{_bindir}/sudoedit
rm -f %{buildroot}%{_docdir}/%{name}/sample.pam
rm -f %{buildroot}%{_docdir}/%{name}/sample.syslog.conf
rm -f %{buildroot}%{_docdir}/%{name}/schema.OpenLDAP
rm -f %{buildroot}%{_libexecdir}/%{name}/sudoers.la
%find_lang %{name}
%find_lang sudoers
cat sudoers.lang >> %{name}.lang

%post
chmod 0440 %{_sysconfdir}/sudoers

%post rpm
echo 'ALL ALL = (root) NOPASSWD: /usr/bin/rpm' >> %{_sysconfdir}/sudoers

%lang_package

%files 
%manifest %{name}.manifest
%defattr(-,root,root)
%license LICENSE
%config(noreplace) %attr(0440,root,root) %{_sysconfdir}/sudoers
%dir %{_sysconfdir}/sudoers.d
%config %{_sysconfdir}/pam.d/sudo
%attr(4755,root,root) %{_bindir}/sudo
%{_bindir}/sudoedit
%{_bindir}/sudoreplay
%{_sbindir}/visudo
%{_libexecdir}/sudo
%attr(0700,root,root) %dir %ghost %{_localstatedir}/lib/sudo
%{_docdir}/%{name}
%{_mandir}/man?/*

%files devel
%manifest %{name}.manifest
%defattr(-,root,root)
%{_includedir}/sudo_plugin.h

%files rpm
