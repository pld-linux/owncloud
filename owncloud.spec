Summary:	Private file sync and share server
Name:		owncloud
Version:	4.0.7
Release:	0.1
License:	AGPL v3, MIT
Group:		Applications/WWW
Source0:	http://owncloud.org/releases/%{name}-%{version}.tar.bz2
# Source0-md5:	7fdbe0113621730a6787afdc7ebb529f
Source1:	config.php
Patch0:		system-pear.patch
URL:		http://owncloud.org
BuildRequires:	rpmbuild(macros) >= 1.268
Requires:	php(core)
Requires:	php(gd)
Requires:	php(mbstring)
Requires:	php(pdo)
Requires:	php(pdo-sqlite)
Requires:	php(posix)
Requires:	php(sqlite3)
Requires:	php(xml)
Requires:	php(zip)
#Requires:	php-When
Requires:	php-pear-Archive_Tar
Requires:	php-pear-Console_Getopt
Requires:	php-pear-Crypt_Blowfish
Requires:	php-pear-MDB2
Requires:	php-pear-MDB2_Driver_mysql
Requires:	php-pear-MDB2_Driver_pgsql
Requires:	php-pear-MDB2_Driver_sqlite
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
Suggests:	php(mysql)
Suggests:	php(pdo-mysql)
Suggests:	php(pdo-pgsql)
Suggests:	php(pgsql)
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
%patch0 -p1

cat > apache.conf <<'EOF'
Alias /%{name} %{_appdir}
<Directory %{_appdir}>
	Allow from all
</Directory>
EOF

cat > lighttpd.conf <<'EOF'
alias.url += (
    "/%{name}" => "%{_appdir}",
)
EOF

# remove bundled 3rdparty libs
%{__rm} -r 3rdparty/{class.phpmailer.php,class.smtp.php,Archive,Console,Crypt_Blowfish,MDB2,MDB2.php,XML}
# PEAR-core
%{__rm} -r 3rdparty/{PEAR.php,PEAR5.php,System.php,PEAR}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir}/config,%{_appdir}}

cp -pdR *.php db_structure.xml 3rdparty apps core files l10n lib ocs search settings themes $RPM_BUILD_ROOT/%{_appdir}
ln -s %{_sysconfdir}/config $RPM_BUILD_ROOT%{_appdir}/config
cp -p %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/config/config.php

cp -p apache.conf $RPM_BUILD_ROOT%{_sysconfdir}/apache.conf
cp -p apache.conf $RPM_BUILD_ROOT%{_sysconfdir}/httpd.conf
cp -p lighttpd.conf $RPM_BUILD_ROOT%{_sysconfdir}/lighttpd.conf

install -d $RPM_BUILD_ROOT%{_localstatedir}/lib/%{name}

%triggerin -- apache1 < 1.3.37-3, apache1-base
%webapp_register apache %{_webapp}

%triggerun -- apache1 < 1.3.37-3, apache1-base
%webapp_unregister apache %{_webapp}

%triggerin -- apache < 2.2.0, apache-base
%webapp_register httpd %{_webapp}

%triggerun -- apache < 2.2.0, apache-base
%webapp_unregister httpd %{_webapp}

%triggerin -- lighttpd
%webapp_register lighttpd %{_webapp}

%triggerun -- lighttpd
%webapp_unregister lighttpd %{_webapp}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS COPYING-AGPL COPYING-README README
%dir %attr(750,root,http) %{_sysconfdir}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/apache.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/httpd.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/lighttpd.conf
%dir %attr(750,http,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/config
%attr(640,http,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/config/*.php
%{_appdir}
%dir %attr(750,http,http) %{_localstatedir}/lib/%{name}
