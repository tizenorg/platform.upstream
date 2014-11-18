%define gitexecdir %{_libexecdir}/git

Name:           git
Version:        2.0.1
Release:        0
License:        GPL-2.0
Summary:        Fast, scalable, distributed revision control system
Url:            http://git-scm.com
Group:          Platform Development/Utilities
Source:         %{name}-%{version}.tar.gz
Source1001: 	git.manifest
BuildRequires:  asciidoc
BuildRequires:  curl
BuildRequires:  expat-devel
BuildRequires:  fdupes
BuildRequires:  gettext-tools
BuildRequires:  libcurl-devel
BuildRequires:  libopenssl-devel
BuildRequires:  perl-Error
BuildRequires:  python
BuildRequires:  xmlto
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
Group:          Platform Development/Utilities
Requires:       less
Requires:       openssh
Requires:       perl-Error
Requires:       perl = %{perl_version}
Requires:       rsync

%description core
Git is a fast, scalable, distributed revision control system with an
unusually rich command set that provides both high-level operations and
full access to internals.

These are the core tools with minimal dependencies.

%package svn
Summary:        Git tools for importing Subversion repositories
Group:          Platform Development/Utilities
Requires:       git-core = %{version}
Requires:       subversion
Requires:       subversion-perl

%description svn
Tools for importing Subversion repositories to the Git version control
system.

%package cvs
Summary:        Git tools for importing CVS repositories
Group:          Platform Development/Utilities
Requires:       cvs
Requires:       cvsps
Requires:       git-core = %{version}
Requires:       perl-DBD-SQLite

%description cvs
Tools for importing CVS repositories to the Git version control system.

%package arch
Summary:        Git tools for importing Arch repositories
Group:          Platform Development/Utilities
Requires:       git-core = %{version}
# Requires:       tla

%description arch
Tools for importing GNU Arch repositories to the GIT version control
system.

%package email
Summary:        Git tools for sending email
Group:          Platform Development/Utilities
Requires:       git-core = %{version}
# For sending mails over secure SMTP:
Recommends:     perl-Authen-SASL
Recommends:     perl-Net-SMTP-SSL

%description email
Email interface for the GIT version control system.

%package daemon
Summary:        Simple Server for Git Repositories
Group:          Platform Development/Utilities
Requires(pre):  /usr/sbin/useradd
Requires:       git-core = %{version}

%description daemon
A really simple TCP git daemon. In the default configuration it allows
read only access to repositories in /srv/git/ that contain the
'git-daemon-export-ok' file.
%package -n gitk
Summary:        Git revision tree visualiser
Group:          Platform Development/Utilities
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
Group:          Platform Development/Utilities
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
Group:          Platform Development/Utilities
Requires:       git-core = %{version}
Supplements:    packageand(git-core:apache2)

%description web
CGI script that allows browsing git repositories via web interface.

The apache2 configuration contained in this package installs a virtual
directory /git/ that calls the cgi script.


%prep
%setup -q
cp %{SOURCE1001} .


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
./.make doc

%check
make %{?_smp_mflags} test


%install
./.make install install-doc
###
(find %{buildroot}%{_bindir} -type f | grep -vE "archimport|svn|cvs|email|gitk|daemon|gui" | sed -e s@^%{buildroot}@@)				> bin-man-doc-files
(find %{buildroot}%{gitexecdir} -mindepth 1 | grep -vE "archimport|svn|cvs|email|gitk|daemon|gui" | sed -e s@^%{buildroot}@@)		>> bin-man-doc-files
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
rm -rf %{buildroot}/Documentation/*.html
rm -rf %{buildroot}/Documentation/*.txt

%fdupes -s %{buildroot}/%{_prefix}


%files
%manifest %{name}.manifest
%doc README

%files svn
%manifest %{name}.manifest
%{gitexecdir}/*svn*
%{_mandir}/man1/*svn*.1*

%files cvs
%manifest %{name}.manifest
%{_bindir}/git-cvs*
%{gitexecdir}/*cvs*
%{_mandir}/man1/*cvs*.1*

%files arch
%manifest %{name}.manifest
%{gitexecdir}/git-archimport
%{_mandir}/man1/git-archimport.1*

%files email
%manifest %{name}.manifest
%{gitexecdir}/*email*
%{_mandir}/man1/*email*.1*

%files daemon
%manifest %{name}.manifest
%{gitexecdir}/*daemon*
%{_mandir}/man1/*daemon*.1*

%files -n gitk
%manifest %{name}.manifest
%{_bindir}/gitk
%{_datadir}/gitk
%{_mandir}/man1/*gitk*.1*

%files gui
%manifest %{name}.manifest
%{gitexecdir}/git-gui*
%{_datadir}/git-gui
%{_mandir}/man1/*gui*.1*

%files core -f bin-man-doc-files
%manifest %{name}.manifest
%license COPYING
%{_bindir}/git
%{_datadir}/git-core/
%dir %{gitexecdir}
%{perl_vendorlib}/Git.pm
%{perl_vendorlib}/Git/
%{perl_vendorlib}/Git/*.pm
%{perl_vendorarch}/auto/Git/
%attr(0644, root, root) %config %{_sysconfdir}/bash_completion.d/git.sh
