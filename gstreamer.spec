%define _glib2		2.0.1
%define _libxml2	2.4.0

## exclude arches that don't work for now.
#ExcludeArch: x86_64 ia64 alpha s390 s390x

Name: gstreamer
Version: 0.6.0
# keep in sync with the VERSION.  gstreamer can append a .0.1 to CVS snapshots.
%define major  0.6

Release: 4
Summary: GStreamer streaming media framework runtime.
Group: Applications/Multimedia
License: LGPL
URL: http://gstreamer.net/
Source: http://gstreamer.net/releases/%{version}/src/%{name}-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-root
Patch: gstreamer-0.5.0-fixdocbook.patch
#Patch2: gstreamer-0.5.2-nowerror.patch

Requires: glib2 >= %_glib2
Requires: libxml2 >= %_libxml2
Requires: popt > 1.6

BuildRequires: glib2-devel >= %_glib2
BuildRequires: libxml2-devel >= %_libxml2
BuildRequires: bison
BuildRequires: gtk-doc >= 0.7
BuildRequires: zlib-devel
BuildRequires: gtk-doc >= 0.7
BuildRequires: popt > 1.6
Prereq: /sbin/ldconfig gstreamer-tools

### documentation requirements
BuildRequires: openjade
BuildRequires: python2
BuildRequires: docbook-style-dsssl docbook-dtd31-sgml docbook-style-xsl
BuildRequires: docbook-utils
BuildRequires: transfig xfig

%description
GStreamer is a streaming-media framework, based on graphs of filters which
operate on media data. Applications using this library can do anything
from real-time sound processing to playing videos, and just about anything
else media-related.  Its plugin-based architecture means that new data
types or processing capabilities can be added simply by installing new 
plugins.

%package devel
Summary: Libraries/include files for GStreamer streaming media framework.
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: glib2-devel >= %_glib2
Requires: libxml2-devel >= %_libxml2

%description devel
GStreamer is a streaming-media framework, based on graphs of filters which
operate on media data. Applications using this library can do anything
from real-time sound processing to playing videos, and just about anything
else media-related.  Its plugin-based architecture means that new data
types or processing capabilities can be added simply by installing new   
plugins.

This package contains the libraries and includes files necessary to develop
applications and plugins for GStreamer.

%package tools
Summary: tools for GStreamer streaming media framework.
Group: Applications/Multimedia

%description tools
GStreamer is a streaming-media framework, based on graphs of filters which
operate on media data. Applications using this library can do anything
from real-time sound processing to playing videos, and just about anything
else media-related.  Its plugin-based architecture means that new data
types or processing capabilities can be added simply by installing new
plugins.

This package contains the basic command-line tools used for GStreamer, like
gst-register and gst-launch.  It is split off to allow parallel-installability
in the future.

%prep
%setup -q
#%patch2 -p1 -b .nowerror

## x86_64 is x86 too!
perl -pi -e 's/xi\?86 \| k\?\)/xi?86 | k? | *86_64)/g' configure aclocal.m4
perl -pi -e 's/-Werror//g' configure libs/ext/cothreads/configure libs/ext/cothreads/configure.ac
%build

## FIXME should re-enable the docs build when it works
./autogen.sh
%configure --disable-plugin-builddir --disable-tests --disable-examples \
	--disable-docs-build --with-html-dir=$RPM_BUILD_ROOT%{_datadir}/gtk-doc/html \
	--enable-debug

make %{?_smp_mflags}

%install  
[ -n "$RPM_BUILD_ROOT" -a "$RPM_BUILD_ROOT" != / ] && rm -rf $RPM_BUILD_ROOT
# adding devhelp stuff here for now, need to integrate better
# when devhelp allows it
#mkdir -p $RPM_BUILD_ROOT/%{_datadir}/devhelp/specs
#cp $RPM_BUILD_DIR/%{name}-%{version}/docs/devhelp/*.devhelp $RPM_BUILD_ROOT/%{_datadir}/devhelp/specs

%makeinstall

/bin/rm -f $RPM_BUILD_ROOT%{_libdir}/gstreamer-%{major}/*.a
/bin/rm -f $RPM_BUILD_ROOT%{_libdir}/gstreamer-%{major}/*.la
/bin/rm -f $RPM_BUILD_ROOT%{_libdir}/*.la
/bin/rm -f $RPM_BUILD_ROOT%{_libdir}/libgstmedia-info*.so.0.0.0

%clean
[ -n "$RPM_BUILD_ROOT" -a "$RPM_BUILD_ROOT" != / ] && rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig
env DISPLAY= %{_bindir}/gst-register --gst-mask=0 > /dev/null 2> /dev/null

%post devel
# adding devhelp links to work around different base not working
#mkdir -p %{_datadir}/devhelp/books
#ln -sf %{_datadir}/gtk-doc/html/gstreamer %{_datadir}/devhelp/books
#ln -sf %{_datadir}/gtk-doc/html/gstreamer-libs %{_datadir}/devhelp/books

%postun -p /sbin/ldconfig

%postun devel
#rm -f %{_datadir}/devhelp/books/gstreamer
#rm -f %{_datadir}/devhelp/books/gstreamer-libs

%files
%defattr(-, root, root)
%doc AUTHORS COPYING README TODO COPYING.LIB ABOUT-NLS REQUIREMENTS DOCBUILDING RELEASE 
%dir %{_libdir}/gstreamer-%{major}
%{_libdir}/gstreamer-%{major}/*.so*
%{_libdir}/libgstreamer-%{major}.so
%{_libdir}/libgstcontrol-%{major}.so
%{_libdir}/*.a
%{_libdir}/*.so.*

%files devel
%defattr(-, root, root)
%dir %{_includedir}/%{name}-%{major}
%{_includedir}/%{name}-%{major}/*
%{_libdir}/pkgconfig/gstreamer*.pc
#%{_datadir}/devhelp/specs/%{name}-%{major}.devhelp
#%{_datadir}/devhelp/specs/%{name}-libs-%{major}.devhelp
#%{_datadir}/gtk-doc/html/gstreamer-%{major}/*html
#%{_datadir}/gtk-doc/html/gstreamer-%{major}/index.sgml
#%{_datadir}/gtk-doc/html/gstreamer-libs-%{major}/*html
#%{_datadir}/gtk-doc/html/gstreamer-libs-%{major}/index.sgml


## FIXME disabled due to --disable-docs-build
##%{_datadir}/gtk-doc/html/*
##%{_datadir}/devhelp/specs/gstreamer.devhelp
##%{_datadir}/devhelp/specs/gstreamer-libs.devhelp

%files tools
%defattr(-, root, root)
%{_bindir}/gst-complete
%{_bindir}/gst-compprep
%{_bindir}/gst-feedback
%{_bindir}/gst-inspect
%{_bindir}/gst-launch
%{_bindir}/gst-md5sum
%{_bindir}/gst-register
%{_bindir}/gst-xmllaunch
%{_mandir}/man1/gst-complete.*
%{_mandir}/man1/gst-compprep.*
%{_mandir}/man1/gst-feedback.*
%{_mandir}/man1/gst-inspect.*
%{_mandir}/man1/gst-launch.*
%{_mandir}/man1/gst-md5sum.*
%{_mandir}/man1/gst-register.*
%{_mandir}/man1/gst-xmllaunch.*

%changelog
* Wed Feb 12 2003 Bill Nottingham <notting@redhat.com> 0.6.0-4
- fix group

* Tue Feb 11 2003 Bill Nottingham <notting@redhat.com> 0.6.0-3
- prereq, not require, gstreamer-tools

* Tue Feb 11 2003 Jonathan Blandford <jrb@redhat.com> 0.6.0-2
- unset the DISPLAY when running gst-register

* Mon Feb  3 2003 Jonathan Blandford <jrb@redhat.com> 0.6.0-1
- yes it is needed.  Readding

* Sat Feb 01 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- remove "tools" sub-rpm, this is not needed at all

* Thu Jan 30 2003 Jonathan Blandford <jrb@redhat.com> 0.5.2-7
- stopped using %configure so we need to pass in all the args

* Mon Jan 27 2003 Jonathan Blandford <jrb@redhat.com>
- remove -Werror explicitly as the configure macro isn't working.

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Thu Dec 19 2002 Elliot Lee <sopwith@redhat.com> 0.5.0-10
- Add patch1 to fix C++ plugins on ia64

* Wed Dec 18 2002 Jonathan Blandford <jrb@redhat.com>
- %post -p was wrong

* Tue Dec 17 2002 Jonathan Blandford <jrb@redhat.com> 0.5.0-7
- explicitly add %{_libdir}/libgstreamer-{major}.so
- explicitly add %{_libdir}/libgstcontrol-{major}.so

* Mon Dec 16 2002 Jonathan Blandford <jrb@redhat.com>
- bump release

* Fri Dec 13 2002 Jonathan Blandford <jrb@redhat.com>
- move .so files out of -devel

* Tue Dec 10 2002 Jonathan Blandford <jrb@redhat.com>
- new version 0.5.0
- require docbook-style-xsl
- add gstreamer-tools package too
- New patch to use the right docbook prefix.

* Tue Dec 10 2002 Jonathan Blandford <jrb@redhat.com>
- downgrade to a release candidate.  Should work better on other arches
- build without Werror

* Mon Dec  9 2002 Jonathan Blandford <jrb@redhat.com>
- update to new version.  Remove ExcludeArch

* Tue Dec  3 2002 Havoc Pennington <hp@redhat.com>
- excludearch some arches

* Mon Dec  2 2002 Havoc Pennington <hp@redhat.com>
- import into CVS and build "officially"
- use smp_mflags
- temporarily disable docs build, doesn't seem to work

* Thu Nov  7 2002 Jeremy Katz <katzj@redhat.com>
- 0.4.2

* Mon Sep 23 2002 Jeremy Katz <katzj@redhat.com>
- 0.4.1

* Sun Sep 22 2002 Jeremy Katz <katzj@redhat.com>
- minor cleanups

* Sat Jun 22 2002 Thomas Vander Stichele <thomas@apestaart.org>
- moved header location

* Mon Jun 17 2002 Thomas Vander Stichele <thomas@apestaart.org>
- added popt
- removed .la

* Fri Jun 07 2002 Thomas Vander Stichele <thomas@apestaart.org>
- added release of gstreamer to req of gstreamer-devel
- changed location of API docs to be in gtk-doc like other gtk-doc stuff
- reordered SPEC file

* Mon Apr 29 2002 Thomas Vander Stichele <thomas@apestaart.org>
- moved html docs to gtk-doc standard directory

* Tue Mar 5 2002 Thomas Vander Stichele <thomas@apestaart.org>
- move version defines of glib2 and libxml2 to configure.ac
- add BuildRequires for these two libs

* Sun Mar 3 2002 Thomas Vander Stichele <thomas@apestaart.org>
- put html docs in canonical place, avoiding %doc erasure
- added devhelp support, current install of it is hackish

* Sat Mar 2 2002 Christian Schaller <Uraeus@linuxrising.org>
- Added documentation to build

* Mon Feb 11 2002 Thomas Vander Stichele <thomas@apestaart.org>
- added libgstbasicscheduler
- renamed libgst to libgstreamer

* Fri Jan 04 2002 Christian Schaller <Uraeus@linuxrising.org>
- Added configdir parameter as it seems the configdir gets weird otherwise

* Thu Jan 03 2002 Thomas Vander Stichele <thomas@apestaart.org>
- split off gstreamer-editor from core
- removed gstreamer-gnome-apps

* Sat Dec 29 2001 Rodney Dawes <dobey@free.fr>
- Cleaned up the spec file for the gstreamer core/plug-ins split
- Improve spec file

* Sat Dec 15 2001 Christian Schaller <Uraeus@linuxrising.org>
- Split of more plugins from the core and put them into their own modules
- Includes colorspace, xfree and wav
- Improved package Require lines
- Added mp3encode (lame based) to the SPEC

* Wed Dec 12 2001 Christian Schaller <Uraeus@linuxrising.org>
- Thomas merged mpeg plugins into one
* Sat Dec 08 2001 Christian Schaller <Uraeus@linuxrising.org>
- More minor cleanups including some fixed descriptions from Andrew Mitchell

* Fri Dec 07 2001 Christian Schaller <Uraeus@linuxrising.org>
- Added logging to the make statement

* Wed Dec 05 2001 Christian Schaller <Uraeus@linuxrising.org>
- Updated in preparation for 0.3.0 release

* Fri Jun 29 2001 Christian Schaller <Uraeus@linuxrising.org>
- Updated for 0.2.1 release
- Split out the GUI packages into their own RPM
- added new plugins (FLAC, festival, quicktime etc.)

* Sat Jun 09 2001 Christian Schaller <Uraeus@linuxrising.org>
- Visualisation plugins bundled out togheter
- Moved files sections up close to their respective descriptions

* Sat Jun 02 2001 Christian Schaller <Uraeus@linuxrising.org>
- Split the package into separate RPMS, 
  putting most plugins out by themselves.

* Fri Jun 01 2001 Christian Schaller <Uraeus@linuxrising.org>
- Updated with change suggestions from Dennis Bjorklund

* Tue Jan 09 2001 Erik Walthinsen <omega@cse.ogi.edu>
- updated to build -devel package as well

* Sun Jan 30 2000 Erik Walthinsen <omega@cse.ogi.edu>
- first draft of spec file

