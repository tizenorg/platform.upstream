%define gitexecdir %{_libexecdir}/git
%define _fwdefdir /etc/sysconfig/SuSEfirewall2.d/services

Name:           git
Version:        1.8.0
Release:        0
License:        GPL-2.0
Summary:        Fast, scalable, distributed revision control system
Url:            http://git-scm.com
Group:          Development/Tools/Version Control
Source:         %{name}-%{version}.tar.bz2
BuildRequires:  curl
BuildRequires:  expat-devel
BuildRequires:  fdupes
BuildRequires:  gettext-tools
BuildRequires:  libcurl-devel
BuildRequires:  libopenssl-devel
BuildRequires:  perl-Error
BuildRequires:  python
Requires:       git-core = %{version}

%description
Git is a fast, scalable, distributed revision control system with an
unusually rich command set that provides both high-level operations and
full access to internals.

This package itself only provides the README of git but with the
packages it requires, it brings you a complete Git environment
including GTK and email interfaces and tools for importing source code
repositories from other revision control systems such as subversion,
CVS, and GNU arch.

%package core
Summary:        Core git tools
Group:          Development/Tools/Version Control
Requires:       less
Requires:       openssh
Requires:       perl-Error
Requires:       perl-base = %{perl_version}
Requires:       rsync

%description core
Git is a fast, scalable, distributed revision control system with an
unusually rich command set that provides both high-level operations and
full access to internals.

These are the core tools with minimal dependencies.

%package svn
Summary:        Git tools for importing Subversion repositories
Group:          Development/Tools/Version Control
Requires:       git-core = %{version}
Requires:       subversion
Requires:       subversion-perl

%description svn
Tools for importing Subversion repositories to the Git version control
system.

%package cvs
Summary:        Git tools for importing CVS repositories
Group:          Development/Tools/Version Control
Requires:       cvs
Requires:       cvsps
Requires:       git-core = %{version}
Requires:       perl-DBD-SQLite

%description cvs
Tools for importing CVS repositories to the Git version control system.

%package arch
Summary:        Git tools for importing Arch repositories
Group:          Development/Tools/Version Control
Requires:       git-core = %{version}
# Requires:       tla

%description arch
Tools for importing GNU Arch repositories to the GIT version control
system.

%package email
Summary:        Git tools for sending email
Group:          Development/Tools/Version Control
Requires:       git-core = %{version}
# For sending mails over secure SMTP:
Recommends:     perl-Authen-SASL
Recommends:     perl-Net-SMTP-SSL,

%description email
Email interface for the GIT version control system.

%package daemon
Summary:        Simple Server for Git Repositories
Group:          Development/Tools/Version Control
Requires(pre):  /usr/sbin/useradd
Requires:       git-core = %{version}

%description daemon
A really simple TCP git daemon. In the default configuration it allows
read only access to repositories in /srv/git/ that contain the
'git-daemon-export-ok' file.
%package -n gitk
Summary:        Git revision tree visualiser
Group:          Development/Tools/Version Control
Requires:       git-core = %{version}
Requires:       tk >= 8.4
Supplements:    packageand(git-core:tk)

%description -n gitk
Grapical tool for visualization of revision trees of projects
maintained in the Git version control system. It name gitk indicates
that it's written using the Tk Widget set.

A simple Tk based graphical interface for common Git operations is
found in the package git-gui.

%package gui
Summary:        Grapical tool for common git operations
Group:          Development/Tools/Version Control
Requires:       git-core = %{version}
Requires:       tk >= 8.4
Supplements:    packageand(git-core:tk)

%description gui
A Tcl/Tk based graphical user interface to Git. git-gui focuses on
allowing users to make changes to their repository by making new
commits, amending existing ones, creating branches, performing local
merges, and fetching/pushing to remote repositories.

Unlike gitk, git-gui focuses on commit generation and single file
annotation, and does not show project history. It does however supply
menu actions to start a gitk session from within git-gui.

%package web
Summary:        Git Web Interface
Group:          Development/Tools/Version Control
Requires:       git-core = %{version}
Supplements:    packageand(git-core:apache2)

%description web
CGI script that allows browsing git repositories via web interface.

The apache2 configuration contained in this package installs a virtual
directory /git/ that calls the cgi script.

%package remote-helpers
Summary:        Python package for remote helper scripts
Group:          Development/Tools/Version Control
Requires:       git-core = %{version}
Requires:       python

%description remote-helpers
This package contains the building blocks for remote helpers written in Python.

%prep
%setup -q

%build
cat > .make <<'EOF'
#!/bin/bash
make %{?_smp_mflags} CFLAGS="%{optflags}" \
       GITWEB_CONFIG="/etc/gitweb.conf" \
       GITWEB_PROJECTROOT="/srv/git" \
       WITH_OWN_SUBPROCESS_PY=YesPlease \
       DESTDIR=%{buildroot} \
       NO_CROSS_DIRECTORY_HARDLINKS=1 \
       V=1 \
       prefix=%{_prefix} mandir=%{_mandir} \
       gitexecdir=%{gitexecdir} \
       htmldir=%{_docdir}/git-core \
       "$@"
EOF
#
chmod 755 .make
./.make all %{?_smp_mflags}

%check
make %{?_smp_mflags} test

%install
./.make install
###
(find %{buildroot}%{_bindir} -type f | grep -vE "archimport|svn|cvs|email|gitk|daemon|gui" | sed -e s@^%{buildroot}@@)                   > bin-man-doc-files
(find %{buildroot}%{gitexecdir} -mindepth 1 | grep -vE "archimport|svn|cvs|email|gitk|daemon|gui" | sed -e s@^%{buildroot}@@)               >> bin-man-doc-files
(find %{buildroot}%{_mandir} %{buildroot}/Documentation -type f | grep -vE "archimport|svn|git-cvs|email|gitk|daemon|gui" | sed -e s@^%{buildroot}@@ -e 's/$/*/' ) >> bin-man-doc-files
( pushd perl
  perl Makefile.PL
  make -f perl.mak DESTDIR=%{buildroot}  install_vendor
)
rm -rf %{buildroot}/usr/lib/perl5/site_perl
%perl_process_packlist
find %{buildroot}/%{_mandir} -type f -print0 | xargs -0 chmod 644
install -m 644 -D contrib/completion/git-completion.bash %{buildroot}%{_sysconfdir}/bash_completion.d/git.sh
%find_lang %{name}
cat %{name}.lang >>bin-man-doc-files
# use symlinks instead of hardlinks in sub-commands


rm -rf %{buildroot}/%{_datadir}/gitweb

%fdupes -s %{buildroot}


%files
%defattr(-,root,root)
%doc README

%files svn
%defattr(-,root,root)
%{gitexecdir}/*svn*
%doc Documentation/*svn*.txt

%files cvs
%defattr(-,root,root)
%doc Documentation/*git-cvs*.txt
%{_bindir}/git-cvs*
%{gitexecdir}/*cvs*

%files arch
%defattr(-,root,root)
%doc Documentation/git-archimport.txt
%{gitexecdir}/git-archimport

%files email
%defattr(-,root,root)
%doc Documentation/*email*.txt
%{gitexecdir}/*email*

%files daemon
%defattr(-,root,root)
%doc Documentation/*daemon*.txt
%{gitexecdir}/*daemon*

%files -n gitk
%defattr(-,root,root)
%doc Documentation/*gitk*.txt
%{_bindir}/gitk
/usr/share/gitk

%files gui
%defattr(-,root,root)
%doc Documentation/*gui*.txt
%{gitexecdir}/git-gui*
/usr/share/git-gui

%files remote-helpers
%defattr(-,root,root)
%python_sitelib/*

%files core -f bin-man-doc-files
%defattr(-,root,root)
%{_bindir}/git
%{_datadir}/git-core/
%dir %{gitexecdir}
%doc README COPYING Documentation/*.txt
%{perl_vendorlib}/Git.pm
%{perl_vendorlib}/Git/
%{perl_vendorlib}/Git/*.pm
%{perl_vendorarch}/auto/Git/
%{_sysconfdir}/bash_completion.d/git.sh

%changelog
