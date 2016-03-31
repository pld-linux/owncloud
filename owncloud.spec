#TODO:
#	use system-wide ca-certificates instead of resources/ca-bundle.crt
#
Summary:	Private file sync and share server
Name:		owncloud
Version:	8.2.2
Release:	1
License:	AGPL v3, MIT
Group:		Applications/WWW
Source0:	http://download.owncloud.org/community/%{name}-%{version}.tar.bz2
# Source0-md5:	f5732baa2c0a5a44db3cf76775fe0c4f
Source1:	config.php
Source2:	apache.conf
Source3:	lighttpd.conf
URL:		http://owncloud.org
BuildRequires:	rpmbuild(macros) >= 1.268
Requires:	getid3
Requires:	php(core) >= 5.4
Requires:	php(ctype)
Requires:	php(curl)
Requires:	php(dom)
Requires:	php(filter)
Requires:	php(gd)
Requires:	php(iconv)
Requires:	php(json)
Requires:	php(mbstring)
Requires:	php(pdo)
Requires:	php(posix)
Requires:	php(session)
Requires:	php(simplexml)
#Requires:	php(spl)
Requires:	php(xml)
Requires:	php(xmlwriter)
Requires:	php(zip)
Requires:	php(zlib)
#Requires:	php-When
# bundled in 3rdparty/pear
#Requires:	php-pear-Archive_Tar
#Requires:	php-pear-Console_Getopt
#Requires:	php-pear-PEAR-core
#Requires:	php-sabredav-Sabre_CalDAV
#Requires:	php-sabredav-Sabre_CardDAV
Requires:	webapps
Requires:	webserver(access)
Requires:	webserver(alias)
Requires:	webserver(php)
Requires:	webserver(rewrite)
Suggests:	php(bz2)
Suggests:	php(exif)
Suggests:	php(fileinfo)
Suggests:	php(imagick)
Suggests:	php(intl)
Suggests:	php(mcrypt)
Suggests:	php(openssl)
# uses one of of the PDO drivers
Suggests:	php(pdo-mysql)
Suggests:	php(mysql)
Suggests:	php(pdo-pgsql)
Suggests:	php(pgsql)
Suggests:	php(pdo-sqlite)
Suggests:	php(sqlite)
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_appdir		%{_datadir}/%{name}
%define		_webapps	/etc/webapps
%define		_webapp		%{name}
%define		_sysconfdir	%{_webapps}/%{_webapp}

%description
ownCloud Server provides you a private file sync and share cloud. Host
this server to easily sync business or private documents across all
your devices, and share those documents with other users of your
ownCloud server on their devices.

%prep
%setup -q -n %{name}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir}/config,%{_appdir}}

cp -pdR robots.txt index.html *.php db_structure.xml 3rdparty apps core l10n lib ocs ocs-provider resources settings themes $RPM_BUILD_ROOT%{_appdir}
ln -s %{_sysconfdir}/config $RPM_BUILD_ROOT%{_appdir}/config
cp -p %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/config/config.php

cp -p %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/apache.conf
cp -p %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/httpd.conf
cp -p %{SOURCE3} $RPM_BUILD_ROOT%{_sysconfdir}/lighttpd.conf

install -d $RPM_BUILD_ROOT%{_localstatedir}/lib/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%triggerin -- apache1 < 1.3.37-3, apache1-base
%webapp_register apache %{_webapp}

%triggerun -- apache1 < 1.3.37-3, apache1-base
%webapp_unregister apache %{_webapp}

%triggerin -- apache-base
%webapp_register httpd %{_webapp}

%triggerun -- apache-base
%webapp_unregister httpd %{_webapp}

%triggerin -- lighttpd
%webapp_register lighttpd %{_webapp}

%triggerun -- lighttpd
%webapp_unregister lighttpd %{_webapp}

%files
%defattr(644,root,root,755)
%doc AUTHORS COPYING-AGPL .htaccess .mailmap .user.ini indie.json occ config/config.sample.php
%dir %attr(750,root,http) %{_sysconfdir}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/apache.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/httpd.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/lighttpd.conf
%dir %attr(750,http,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/config
%attr(640,http,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/config/*.php
%{_appdir}
%dir %attr(750,http,http) %{_localstatedir}/lib/%{name}
