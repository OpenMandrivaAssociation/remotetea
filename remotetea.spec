%define gcj_support	0

Name:		remotetea
Summary:	A fully fledged implementation of the ONC/RPC protocol in Java
Version:	1.0.7
Release:	4
Group:		Development/Java
License:	LGPLv2+
URL:		https://remotetea.sourceforge.net/
Source:		remotetea-src-%{version}.zip
%if %{gcj_support}
BuildRequires:	java-gcj-compat-devel
%else
BuildArch:	noarch
BuildRequires:	java-devel
%endif
BuildRequires:	ant
BuildRequires:	locales-en

%description
Remote Tea implements the complete ONC/RPC protocol for the TCP/IP and
UDP/IP transports according to RFC 1831. In particular:
    *  100% Java,
    * complete client functionality, including portmapper access,
    * complete server functionality,
    * a protocol compiler for .x files (rpcgen-compatible, Java-based),
      The protocol compiler jrpcgen from this package is compatible with
      Sun's rpcgen for SunOS 4.1 – with the only exceptions that no
      preprocessor and no "%" directives are available. However, multiple
      parameters in procedures are supported.
    * a Java-based portmapper,
      ...for whatever this could be good for...
    * comprehensive documentation both as Javadoc and commented source,
      Go and find the jokes and sarcastic comments...
    * Open Source (GNU LGPL) gives you the security to be able to know
      what is inside and what is not inside. And yes, the eCommunist
      FUD newspaper, the Wallstreak Journal, and the Infrigenancial Times
      (kind of The Financial Sun when it comes to properly researched
      articles) are all right: Open Source is viral and infects you with
      true freedom - freedom still means to respect rights, especially
      the rights of others.

%prep
%setup -q -n %name
find . -name '*.jar' -name '*.class' -exec %{__rm} -f {} \;
%{__mkdir} build
%{__cat} > build.xml <<EOF
<project name="aTunes" basedir="." default="build-jar">
	<target name="build-jar">
		<javac srcdir="src" destdir="build">
			<classpath>
				<fileset dir="%{_javadir}" includes="*.jar"/>
			</classpath>
		</javac>
		<copy todir="build">
			<fileset dir="src" />
		</copy>
		<jar basedir="build" destfile="jrpcgen-%{version}.jar">
			<fileset dir="build" includes="*/*.*"/>
		</jar>
	</target>
</project>
EOF

%build
export LC_ALL=ISO-8859-1
ant build-jar
%{__ln_s} jrpcgen-%{version}.jar jrpcgen.jar

%install
%{__mkdir_p} %{buildroot}%{_javadir}
%{__cp} -a jrpcgen-%{version}.jar jrpcgen.jar %{buildroot}%{_javadir}
%{__ln_s} %{_javadir}/jrpcgen.jar %{buildroot}%{_javadir}/oncrpc.jar

%if %{gcj_support}
%{_bindir}/aot-compile-rpm
%endif

%if %{gcj_support}
%post
%{update_gcjdb}

%postun
%{clean_gcjdb}
%endif

%files
%doc changelog.html readme.html docstyle.css COPYING.LIB
%{_javadir}/jrpcgen-%{version}.jar
%{_javadir}/jrpcgen.jar
%{_javadir}/oncrpc.jar
%if %{gcj_support}
%dir %{_libdir}/gcj/%{name}
%{_libdir}/gcj/%{name}/*
%endif


%changelog
* Tue Sep 15 2009 Thierry Vignaud <tvignaud@mandriva.com> 1.0.7-2mdv2010.0
+ Revision: 442676
- rebuild

* Thu Feb 19 2009 Nicolas Vigier <nvigier@mandriva.com> 1.0.7-1mdv2009.1
+ Revision: 342912
- version 1.0.7
- disable gcj support
- add oncrpc.jar symlink
- fix description
- import remotetea

  + Thierry Vignaud <tvignaud@mandriva.com>
    - fix no-buildroot-tag


