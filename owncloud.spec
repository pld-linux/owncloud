#TODO:
# - make package for libs from 3rdparty dir:
#  - aws-sdk http://aws.amazon.com/sdkforphp
#  - dropbox-php http://www.dropbox-php.com/
#  - jquery-minicolors https://github.com/claviska/jquery-miniColors/
#  - phpMyID http://siege.org/projects/phpMyID
#  - php-pear-OS_Guess
#  - phpass http://www.openwall.com/phpass/
#  - php-cloudfiles https://github.com/rackspace/php-cloudfiles
#  - simpletest http://simpletest.org/en/download.html
#  - smb4php http://www.phpclasses.org/smb4php
#  - jquery-timepicker http://fgelinas.com/code/timepicker
#  - sabredav - https://code.google.com/p/sabredav/
%define		beta	beta4
Summary:	Private file sync and share server
Name:		owncloud
Version:	6.0.0
Release:	0.%{beta}.1
License:	AGPL v3, MIT
Group:		Applications/WWW
Source0:	http://download.owncloud.org/community/testing/%{name}-%{version}%{beta}.tar.bz2
# Source0-md5:	d1c193fa49c3a16c2da0cef5fedeca12
Source1:	config.php
Source2:	apache.conf
Source3:	lighttpd.conf
Patch1:		pear-not-strict.patch
URL:		http://owncloud.org
BuildRequires:	rpmbuild(macros) >= 1.268
Requires:	getid3
Requires:	php(core) >= 5.3
Requires:	php(ctype)
Requires:	php(dom)
Requires:	php(filter)
Requires:	php(gd)
Requires:	php(iconv)
Requires:	php(json)
Requires:	php(mbstring)
Requires:	php(pdo)
Requires:	php(posix)
Requires:	php(session)
Requires:	php(spl)
Requires:	php(xml)
Requires:	php(zip)
Requires:	php(zlib)
#Requires:	php-When
Requires:	php-pear-Archive_Tar
Requires:	php-pear-Console_Getopt
Requires:	php-pear-MDB2
Requires:	php-pear-MDB2_Schema
Requires:	php-pear-PEAR-core
Requires:	php-pear-XML_Parser
Requires:	php-phpmailer >= 5.2
#Requires:	php-sabredav-Sabre_CalDAV
#Requires:	php-sabredav-Sabre_CardDAV
Requires:	webapps
Requires:	webserver(access)
Requires:	webserver(alias)
Requires:	webserver(php)
Requires:	webserver(rewrite)
# uses one of of the MDB2 drivers
Suggests:	php-pear-MDB2_Driver_mysql
Suggests:	php-pear-MDB2_Driver_pgsql
Suggests:	php-pear-MDB2_Driver_sqlite
Suggests:	php-pear-MDB2_Driver_sqlite3
Conflicts:	apache-base < 2.4.0-1
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
%patch1 -p1

# remove bundled 3rdparty libs
%{__rm} -r 3rdparty/{class.phpmailer.php,class.smtp.php,getid3,Archive,Console,MDB2,MDB2.php,XML}
# PEAR-core
%{__rm} -r 3rdparty/{PEAR.php,PEAR5.php,System.php,PEAR}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir}/config,%{_appdir}}

cp -pdR robots.txt index.html *.php db_structure.xml 3rdparty apps core l10n lib ocs search settings themes $RPM_BUILD_ROOT%{_appdir}
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
%doc AUTHORS COPYING-AGPL 
%dir %attr(750,root,http) %{_sysconfdir}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/apache.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/httpd.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/lighttpd.conf
%dir %attr(750,http,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/config
%attr(640,http,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/config/*.php
%{_appdir}
%dir %attr(750,http,http) %{_localstatedir}/lib/%{name}
