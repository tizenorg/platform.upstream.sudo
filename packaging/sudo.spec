Name:           sudo
Version:        1.8.6p6
Release:        0
Summary:        Execute some commands as root
License:        ISC
Group:          System/Base
Url:            http://www.sudo.ws/
Source0:        http://sudo.ws/sudo/dist/%{name}-%{version}.tar.gz
Source1:        sudo.pamd
Source2:        tizen_conf
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
Group:          Development/Libraries

%description devel
These header files are needed for building of sudo plugins.

%prep
%setup -q

%build
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
--with-timedir=%{_localstatedir}/lib/sudo
make %{?_smp_mflags}

%install
%make_install
install -d -m 755 %{buildroot}%{_sysconfdir}/pam.d
install -m 644 %{SOURCE1} %{buildroot}%{_sysconfdir}/pam.d/sudo
install -m 644 %{SOURCE2} %{buildroot}%{_sysconfdir}/sudoers.d
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


%lang_package

%files 
%defattr(-,root,root)
%config(noreplace) %attr(0440,root,root) %{_sysconfdir}/sudoers
%dir %{_sysconfdir}/sudoers.d
%{_sysconfdir}/sudoers.d/*
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
%defattr(-,root,root)
%{_includedir}/sudo_plugin.h

%changelog
