%define		gstreamer	gstreamer
%define		majorminor	0.10

%define 	_glib2		2.8.3
%define 	_libxml2	2.4.0

Name: 		%{gstreamer}
Version: 	0.10.1
Release: 	1
Summary: 	GStreamer streaming media framework runtime

Group: 		Applications/Multimedia
License: 	LGPL
URL:		http://gstreamer.freedesktop.org/
Source: 	http://gstreamer.freedesktop.org/src/gstreamer/gstreamer-%{version}.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Requires:	gstreamer-tools >= %{version}

BuildRequires: 	glib2-devel >= %{_glib2}
BuildRequires: 	libxml2-devel >= %{_libxml2}
BuildRequires: 	bison
BuildRequires: 	flex
BuildRequires: 	m4
BuildRequires: 	check-devel
BuildRequires: 	gtk-doc >= 1.3
BuildRequires:	gettext

# because AM_PROG_LIBTOOL was used in configure.ac
BuildRequires:	gcc-c++

### documentation requirements
BuildRequires:  python2
BuildRequires:  openjade
BuildRequires:  jadetex
BuildRequires:	libxslt
BuildRequires:  docbook-style-dsssl
BuildRequires:  docbook-style-xsl
BuildRequires:  docbook-utils
BuildRequires:	transfig
BuildRequires:  xfig
BuildRequires:  netpbm-progs
BuildRequires:  tetex-dvips
BuildRequires:  ghostscript
BuildRequires:  PyXML

%description
GStreamer is a streaming media framework, based on graphs of filters which
operate on media data. Applications using this library can do anything
from real-time sound processing to playing videos, and just about anything
else media-related.  Its plugin-based architecture means that new data
types or processing capabilities can be added simply by installing new 
plugins.

%package devel
Summary: 	Libraries/include files for GStreamer streaming media framework
Group: 		Development/Libraries

Requires: 	%{name} = %{version}-%{release}
Requires: 	glib2-devel >= %{_glib2}
Requires: 	libxml2-devel >= %{_libxml2}

%description devel
GStreamer is a streaming media framework, based on graphs of filters which
operate on media data. Applications using this library can do anything
from real-time sound processing to playing videos, and just about anything
else media-related.  Its plugin-based architecture means that new data
types or processing capabilities can be added simply by installing new   
plugins.

This package contains the libraries and includes files necessary to develop
applications and plugins for GStreamer, as well as general and API
documentation.

%package -n gstreamer-tools
Summary: 	common tools and files for GStreamer streaming media framework
Group: 		Applications/Multimedia

%description -n gstreamer-tools
GStreamer is a streaming media framework, based on graphs of filters which
operate on media data. Applications using this library can do anything
from real-time sound processing to playing videos, and just about anything
else media-related.  Its plugin-based architecture means that new data
types or processing capabilities can be added simply by installing new   
plugins.

This package contains wrapper scripts for the command-line tools that work
with different major/minor versions of GStreamer.

%prep
%setup -q -n gstreamer-%{version}

%build
# 0.10.0: manuals do not build due to an openjade error; disable for now
%configure \
  --with-package-name='Fedora Core gstreamer package' \
  --with-package-origin='http://download.fedora.redhat.com/fedora' \
  --enable-debug \
  --enable-gtk-doc --disable-docbook \
  --disable-tests --disable-examples

#make %{?_smp_mflags}
# FIXME: docs building doesn't work with smp yet
make

%install  
rm -rf $RPM_BUILD_ROOT

# Install doc temporarily in order to be included later by rpm
%makeinstall docdir="`pwd`/installed-doc"

%find_lang gstreamer-%{majorminor}
# Clean out files that should not be part of the rpm. 
mkdir -p $RPM_BUILD_ROOT%{_localstatedir}/cache/gstreamer-%{majorminor}
rm -f $RPM_BUILD_ROOT%{_libdir}/gstreamer-%{majorminor}/*.la
rm -f $RPM_BUILD_ROOT%{_libdir}/gstreamer-%{majorminor}/*.a
rm -f $RPM_BUILD_ROOT%{_libdir}/*.a
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la
# Create empty cache directory
mkdir -p $RPM_BUILD_ROOT%{_localstatedir}/cache/gstreamer-%{majorminor}

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files -f gstreamer-%{majorminor}.lang
%defattr(-, root, root, -)
%doc AUTHORS COPYING NEWS README RELEASE TODO
%{_libdir}/libgstreamer-%{majorminor}.so.*
%{_libdir}/libgstbase-%{majorminor}.so.*
%{_libdir}/libgstcontroller-%{majorminor}.so.*
%{_libdir}/libgstdataprotocol-%{majorminor}.so.*
%{_libdir}/libgstnet-%{majorminor}.so.*

%dir %{_libdir}/gstreamer-%{majorminor}
%{_libdir}/gstreamer-%{majorminor}/libgstcoreelements.so
%{_libdir}/gstreamer-%{majorminor}/libgstcoreindexers.so

%{_bindir}/gst-feedback-%{majorminor}
%{_bindir}/gst-inspect-%{majorminor}
%{_bindir}/gst-launch-%{majorminor}
%{_bindir}/gst-md5sum-%{majorminor}
%{_bindir}/gst-typefind-%{majorminor}
%{_bindir}/gst-xmlinspect-%{majorminor}
%{_bindir}/gst-xmllaunch-%{majorminor}
%{_mandir}/man1/gst-feedback-%{majorminor}.*
%{_mandir}/man1/gst-inspect-%{majorminor}.*
%{_mandir}/man1/gst-launch-%{majorminor}.*
%{_mandir}/man1/gst-md5sum-%{majorminor}.*
%{_mandir}/man1/gst-typefind-%{majorminor}.*
%{_mandir}/man1/gst-xmlinspect-%{majorminor}.*
%{_mandir}/man1/gst-xmllaunch-%{majorminor}.*

%files -n gstreamer-tools
%defattr(-, root, root, -)
%{_bindir}/gst-feedback
%{_bindir}/gst-inspect
%{_bindir}/gst-launch
%{_bindir}/gst-md5sum
%{_bindir}/gst-typefind
%{_bindir}/gst-xmlinspect
%{_bindir}/gst-xmllaunch

%files devel
%defattr(-, root, root, -)
# %doc installed-doc/*
%dir %{_includedir}/gstreamer-%{majorminor}
%dir %{_includedir}/gstreamer-%{majorminor}/gst
%{_includedir}/gstreamer-%{majorminor}/gst/*.h

%{_includedir}/gstreamer-%{majorminor}/gst/base
%{_includedir}/gstreamer-%{majorminor}/gst/check
%{_includedir}/gstreamer-%{majorminor}/gst/controller
%{_includedir}/gstreamer-%{majorminor}/gst/dataprotocol
%{_includedir}/gstreamer-%{majorminor}/gst/net

%{_libdir}/libgstreamer-%{majorminor}.so
%{_libdir}/libgstdataprotocol-%{majorminor}.so
%{_libdir}/libgstbase-%{majorminor}.so
%{_libdir}/libgstcheck-%{majorminor}.so*
%{_libdir}/libgstcontroller-%{majorminor}.so
%{_libdir}/libgstnet-%{majorminor}.so

%{_datadir}/aclocal/gst-element-check-%{majorminor}.m4
%{_libdir}/pkgconfig/gstreamer-%{majorminor}.pc
%{_libdir}/pkgconfig/gstreamer-base-%{majorminor}.pc
%{_libdir}/pkgconfig/gstreamer-controller-%{majorminor}.pc
%{_libdir}/pkgconfig/gstreamer-check-%{majorminor}.pc
%{_libdir}/pkgconfig/gstreamer-dataprotocol-%{majorminor}.pc
%{_libdir}/pkgconfig/gstreamer-net-%{majorminor}.pc

%doc %{_datadir}/gtk-doc/html/gstreamer-%{majorminor}/*
%doc %{_datadir}/gtk-doc/html/gstreamer-libs-%{majorminor}/*
%doc %{_datadir}/gtk-doc/html/gstreamer-plugins-%{majorminor}/*

%changelog
* Fri Jan 06 2006 John (J5) Palmieri <johnp@redhat.com> - 0.10.1-1
- New upstream version

* Fri Dec 16 2005 Thomas Vander Stichele <thomas at apestaart dot org>
- 0.10.0-1
- rebuilt for Fedora Core Development

* Wed Dec 14 2005 Thomas Vander Stichele <thomas at apestaart dot org>
- 0.10.0-0.gst.2
- rebuilt against newer GLib and friends

* Mon Dec 05 2005 Thomas Vander Stichele <thomas at apestaart dot org>
- 0.10.0-0.gst.1
- new release

* Thu Dec 01 2005 Thomas Vander Stichele <thomas at apestaart dot org>
- 0.9.7-0.gst.1
- new release, with 0.10 majorminor
- removed compprep and complete
- added plugins docs
- renamed libgstcorelements, libgstcoreindexers
- added libgstnet

* Sat Nov 12 2005 Thomas Vander Stichele <thomas at apestaart dot org>
- 0.9.5-0.gst.1
- new release

* Mon Oct 24 2005 Thomas Vander Stichele <thomas at apestaart dot org>
- 0.9.4-0.gst.1
- new release

* Mon Oct 03 2005 Thomas Vander Stichele <thomas at apestaart dot org>
- 0.9.3-0.gst.1
- new release

* Thu Sep 08 2005 Thomas Vander Stichele <thomas at apestaart dot org>
- 0.9.2-0.gst.1
- added libgstcheck
- new release

* Thu Jun 09 2005 Thomas Vander Stichele <thomas at apestaart dot org>
- 0.9.1-0.gst.1
- first development series release

* Tue May 03 2005 Thomas Vander Stichele <thomas at apestaart dot org>
- 0.8.10-0.gst.1
- new release
- up glib2 to 2.4 because disting on 2.4 builds marshalling code needing 2.4

* Mon May 02 2005 Thomas Vander Stichele <thomas at apestaart dot org>
- 0.8.9.2-0.gst.1
- new prerelease

* Tue Feb 08 2005 Thomas Vander Stichele <thomas at apestaart dot org>
- 0.8.9-0.gst.1
- new release
- switch back to the gst tag since fedora.us is gone

* Thu Feb 03 2005 Thomas Vander Stichele <thomas at apestaart dot org>
- 0.8.8.2-0.fdr.1
- new prerelease

* Thu Dec 23 2004 Thomas Vander Stichele <thomas at apestaart dot org>
- 0.8.8-0.fdr.1
- new upstream release

* Fri Dec 17 2004 Thomas Vander Stichele <thomas at apestaart dot org>
- 0.8.7.2-0.fdr.1
- new prerelease
- added fair gthread scheduler

* Wed Oct 06 2004 Thomas Vander Stichele <thomas at apestaart dot org>
- 0.8.7-0.fdr.1
- update for new GStreamer release

* Tue Oct 05 2004 Thomas Vander Stichele <thomas at apestaart dot org>
- 0.8.6-0.fdr.1
- update for new GStreamer release

* Sun Sep 26 2004 Thomas Vander Stichele <thomas at apestaart dot org>
- 0.8.5.3-0.fdr.1
- update for new GStreamer prerelease

* Sun Sep 12 2004 Thomas Vander Stichele <thomas at apestaart dot org>
- 0.8.5.2-0.fdr.1
- update for new GStreamer prerelease

* Mon Aug 16 2004 Thomas Vander Stichele <thomas at apestaart dot org>
- 0.8.5-0.fdr.1
- update for new GStreamer release

* Thu Aug 12 2004 Thomas Vander Stichele <thomas at apestaart dot org>
- 0.8.4.2-0.fdr.1
- update for new GStreamer prerelease
- set package name and origin

* Tue Jul 20 2004 Thomas Vander Stichele <thomas at apestaart dot org>
- 0.8.4-0.fdr.1
- update for new GStreamer release
- unbreak the postun script by not removing the cache dir

* Tue Jul 20 2004 Thomas Vander Stichele <thomas at apestaart dot org>
- 0.8.3.3-0.fdr.1: update for new GStreamer prerelease

* Fri Jul 16 2004 Thomas Vander Stichele <thomas at apestaart dot org>
- 0.8.3.2-0.fdr.1: update for new GStreamer prerelease

* Sat Jun 05 2004 Thomas Vander Stichele <thomas at apestaart dot org>
- 0.8.3-0.fdr.1: update for new GStreamer release

* Fri Jun 04 2004 Thomas Vander Stichele <thomas at apestaart dot org>
- 0.8.2-0.fdr.1: update for new GStreamer release

* Thu Apr 15 2004 Thomas Vander Stichele <thomas at apestaart dot org>
- 0.8.1-0.fdr.1: update for new GStreamer release

* Thu Apr 15 2004 Thomas Vander Stichele <thomas at apestaart dot org>
- add entry schedulers, clean up scheduler file section

* Tue Mar 16 2004 Thomas Vander Stichele <thomas at apestaart dot org>
- 0.8.0-0.fdr.1: update for new GStreamer release, renamed base to gstreamer

* Tue Mar 09 2004 Thomas Vander Stichele <thomas at apestaart dot org>
- 0.7.6-0.fdr.1: updated for new GStreamer release, with maj/min set to 0.8

* Mon Mar 08 2004 Thomas Vander Stichele <thomas at apestaart dot org>
- 0.7.5-0.fdr.3: fix postun script

* Fri Mar 05 2004 Thomas Vander Stichele <thomas at apestaart dot org>
- 0.7.5-0.fdr.2: new release

* Wed Feb 11 2004 Thomas Vander Stichele <thomas at apestaart dot org>
- 0.7.4-0.fdr.1: synchronize with Matthias's package

* Sat Feb 07 2004 Thomas Vander Stichele <thomas at apestaart dot org>
- make the package name gstreamer07 since this is an unstable release

* Wed Feb 04 2004 Thomas Vander Stichele <thomas at apestaart dot org>
- put versioned tools inside base package, and put unversioned tools in tools

* Mon Dec 01 2003 Thomas Vander Stichele <thomas at apestaart dot org>
- changed documentation buildrequires

* Sun Nov 09 2003 Christian Schaller <Uraeus@gnome.org>
- Fix spec to handle new bytestream library 

* Sun Aug 17 2003 Christian Schaller <uraeus@gnome.org>
- Remove docs build from RPM as the build is broken
- Fix stuff since more files are versioned now
- Remove wingo schedulers
- Remove putbits stuff

* Sun May 18 2003 Thomas Vander Stichele <thomas at apestaart dot org>
- devhelp files are now generated by gtk-doc, changed accordingly

* Sun Mar 16 2003 Christian F.K. Schaller <Uraeus@gnome.org>
- Add gthread scheduler

* Sat Dec 07 2002 Thomas Vander Stichele <thomas at apestaart dot org>
- define majorminor and use it everywhere
- full parallel installability

* Tue Nov 05 2002 Christian Schaller <Uraeus@linuxrising.org>
- Add optwingo scheduler
* Sat Oct 12 2002 Christian Schaller <Uraeus@linuxrising.org>
- Updated to work better with default RH8 rpm
- Added missing unspeced files
- Removed .a and .la files from buildroot

* Sat Sep 21 2002 Thomas Vander Stichele <thomas@apestaart.org>
- added gst-md5sum

* Tue Sep 17 2002 Thomas Vander Stichele <thomas@apestaart.org>
- adding flex to buildrequires

* Fri Sep 13 2002 Christian F.K. Schaller <Uraeus@linuxrising.org>
- Fixed the schedulers after the renaming
* Sun Sep 08 2002 Thomas Vander Stichele <thomas@apestaart.org>
- added transfig to the BuildRequires:

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

