# TODO:
# - webapps
# - R: & BR:
#
%define		version_major	0.5.4
%define		version_minor	1
#
Summary:	Cyrus-IMAP based mail accounts managment system
Summary(pl.UTF-8):   System zarządzania kontami pocztowymi oparty o Cyrus-IMAP
Name:		web-cyradm
Version:	%{version_major}.%{version_minor}
Release:	0.1
Epoch:		0
License:	GPL
Group:		Applications
Source0:	http://www.web-cyradm.org/%{name}-%{version_major}-%{version_minor}.tar.gz
Source1:	%{name}-apache.conf
Patch0:		%{name}-locale.patch
# Source0-md5:	d06dc16899680c29b94a5460709b5fe0
URL:		http://www.web-cyradm.org/
BuildRequires:	rpmbuild(macros) >= 1.228
Requires:	apache >= 2.0
Requires:	php(gettext)
Requires:	php-pear-DB
Requires:	webserver(php)
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Web-cyradm is a software that glues topnotch mailing technologies
together. The software on which web-cyradm relies on is completely
free and opensource software. Web-cyradm is continously developed
further to expand its functionality and usability.

Features:
 - Administer multiple virtual domains
 - Manage user-accounts
 - Map useraccounts to emailadresses
 - Create, delete and rename cyrus-imap mailboxes
 - Setting of quotas for users and domains
 - Delegation of some tasks to domain adminstrators
 - Resetting password for accountusers by its domainadmins and
   superusers
 - Sieve functions like forwarding single e-mail adresses and
   out-of-office replies
 - Enable/Disable different services like imap, pop, sieve and smtp for
   particular users
 - Support for MySQL and PostgreSQL databases
 - Storing passwords in crypt, md5 or MySQL passwd compatible format

%description -l pl.UTF-8
Web-cyradm jest oprogramowaniem sklejającym wiele technologii Open
Source w jeden duży system pocztowy.

Możliwości:
 - Administrowanie wieloma wirtualnymi domenami
 - Zarządzanie kontami użytkowników
 - Mapowanie kont użytkowników na adresy e-mail
 - Tworzenie, usuwanie i zmiana nazwy skrzynek pocztwowych
 - Ustawianie limitów dla użytkowników i domen
 - Delegacja zadań do administratorów domen
 - Resetowanie haseł użytkownikom przez administratorów domen
 - Funkcje Sieve, takie jak przekazywanie pojedynczych adresów e-mail
   czy automatyczne odpowiedzi o nieobecności
 - Włączanie i wyłączanie usług (imap, pop, sieve, smtp) dla
   poszczególnych użytkowników
 - Obsluga baz MySQL i PostgreSQL
 - Obsługa haseł w formacie MD5, Crypt i MySQL PASSWORD()

%prep
%setup -q -n %{name}-%{version_major}-%{version_minor}
%patch0 -p1

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_sysconfdir}/{%{name},httpd}
install -d $RPM_BUILD_ROOT%{_datadir}/%{name}/{css,images,lib}
install -d $RPM_BUILD_ROOT%{_localstatedir}/log/%{name}

install	config/conf.php.dist	\
	$RPM_BUILD_ROOT%{_sysconfdir}/%{name}/conf.php

install	%{SOURCE1}	$RPM_BUILD_ROOT%{_sysconfdir}/httpd/%{name}.conf

install	*.php		$RPM_BUILD_ROOT%{_datadir}/%{name}
install	css/*		$RPM_BUILD_ROOT%{_datadir}/%{name}/css
install images/*	$RPM_BUILD_ROOT%{_datadir}/%{name}/images
install lib/*		$RPM_BUILD_ROOT%{_datadir}/%{name}/lib

ln -s %{_sysconfdir}/%{name} $RPM_BUILD_ROOT%{_datadir}/%{name}/config

for i in locale/?? locale/??_??; do
    install -d $RPM_BUILD_ROOT%{_datadir}/$i/LC_MESSAGES
    install $i/LC_MESSAGES/*.mo $RPM_BUILD_ROOT%{_datadir}/$i/LC_MESSAGES
done

touch $RPM_BUILD_ROOT%{_localstatedir}/log/%{name}/%{name}-login.log

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%triggerin -- apache >= 2.0.0
%apache_config_install -v 2 -c %{_sysconfdir}/httpd/%{name}.conf

%triggerun -- apache >= 2.0.0
%apache_config_uninstall -v 2

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc ChangeLog COPYRIGHT INSTALL README README.translations TO-BE-DONE migrate.php-dist doc/* scripts
%dir %{_sysconfdir}/%{name}
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/*
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/httpd/%{name}.conf
%ghost %{_localstatedir}/log/%{name}/*.log
%{_datadir}/%{name}
