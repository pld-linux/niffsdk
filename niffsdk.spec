Summary:	NIFF SDK libraries
Summary(pl):	Biblioteki NIFF SDK
Name:		niffsdk
Version:	1.02
Release:	1
License:	Public Domain
Group:		Libraries
Source0:	http://www.musique.umontreal.ca/personnel/Belkin/N/%{name}-%{version}.tar
Patch0:		%{name}-make.patch
Patch1:		%{name}-shared.patch
URL:		http://www.musique.umontreal.ca/personnel/Belkin/NIFF.doc.html
BuildRequires:	autoconf
BuildRequires:	automake
# because of makedepend
BuildRequires:	imake
BuildRequires:	libtool >= 1:1.4.2-9
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_includedir	%{_prefix}/include/niff

%description
The NIFF SDK is a free, public domain, platform independent Software
Developer's Kit (SDK) for software developers implementing the
Notation Interchange File Format (NIFF). It is a collection of
software libraries and tools to support reading, writing, and
navigating NIFF files. NIFF documentation, sample code, and sample
NIFF files are included. The NIFF SDK makes it possible for a software
developer to add NIFF reading and writing capabilities to an existing
program without writing the housekeeping functions that would
otherwise be required.

This package contains NIFF shared libraries.

%description -l pl
NIFF SDK to darmowy, bêd±cy w³asno¶ci± publiczn±, niezale¿ny od
platformy zestaw programistyczny dla programistów korzystaj±cych z
plików w formacie NIFF (Notation Interchange File Format). Jest to
zestaw bibliotek i narzêdzi obs³uguj±cych odczyt, zapis i poruszanie
siê po plikach NIFF. Do³±czone s± tak¿e dokumentacja, przyk³adowy
kod i przyk³adowe pliki NIFF. NIFF SDK umo¿liwia programistom dodanie
mo¿liwo¶ci odczytu i zapisu plików NIFF do istniej±cego programu bez
pisania samemu obs³uguj±cych te operacje funkcji.

Ten pakiet zawiera biblioteki wspó³dzielone NIFF.

%package devel
Summary:	NIFF SDK header files and development documentation
Summary(pl):	Pliki nag³ówkowe i dokumentacja programisty NIFF SDK
Group:		Development/Libraries
Requires:	%{name} = %{version}

%description devel
NIFF SDK header files and development documentation.

%description devel -l pl
Pliki nag³ówkowe i dokumentacja programisty NIFF SDK.

%package static
Summary:	NIFF SDK static libraries
Summary(pl):	Statyczne biblioteki NIFF SDK
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}

%description static
NIFF SDK static libraries.

%description static -l pl
Statyczne biblioteki NIFF SDK.

%prep
%setup -q -n %{name}%{version}
%patch0 -p1
%patch1 -p1

# propagate mk fixes (cannot symlink, because generated top.mks differ)
cp -a mk/* niff/mk
cp -a mk/* niffio/mk
cp -a mk/* riffio/mk

%build
%{__autoconf}
cd niff
%{__autoconf}
cd ../niffio
%{__libtoolize}
%{__aclocal}
%{__autoconf}
cd ../riffio
%{__libtoolize}
%{__aclocal}
%{__autoconf}
cd ..
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install DESTDIR=$RPM_BUILD_ROOT

# missing in makefiles
install niff/include/niff.h $RPM_BUILD_ROOT%{_includedir}

# prepare docs
install -d html-doc/{niffio,riffio}
cp -rf niffio/doc/htm/* html-doc/niffio
cp -rf riffio/doc/htm/* html-doc/riffio

linkman() {
# linkman source dest-man [man-links]
	basename=$2
	install $1 $RPM_BUILD_ROOT%{_mandir}/man3/$2
	shift 2
	for l in $* ; do
		echo ".so $basename" > $RPM_BUILD_ROOT%{_mandir}/man3/$l
	done
}
# use only programs and functions docs in man format, the rest is in HTML
install -d $RPM_BUILD_ROOT%{_mandir}/man{1,3}
install riffio/doc/man/riffdump.man $RPM_BUILD_ROOT%{_mandir}/man1/riffdump.1
install riffio/doc/man/riffio.man $RPM_BUILD_ROOT%{_mandir}/man3/riffio.3
linkman riffio/doc/man/chunks.man RIFFIOChunk.3 \
	RIFFIOChunkCreate.3 RIFFIOChunkFinalize.3 \
	RIFFIOChunkDescend.3 RIFFIOChunkAscend.3 \
	RIFFIOChunkDataEnd.3 RIFFIOChunkEnd.3 \
	RIFFIOChunkDataOffset.3 RIFFIOChunkSeekData.3 \
	RIFFIOChunkIsList.3
linkman riffio/doc/man/error.man RIFFIOError.3 \
	RIFFIOInstallErrorHandler.3
linkman riffio/doc/man/fcc.man RIFFIOFOURCC.3 \
	RIFFIOFOURCCIsValid.3 RIFFIOFOURCCToString.3
linkman riffio/doc/man/rfile.man RIFFIOFile.3 \
	RIFFIOFileNew.3 RIFFIOFileInit.3 RIFFIOFileDelete.3 \
	RIFFIOFileGetFormType.3 \
	RIFFIORead.3 RIFFIOWrite.3 RIFFIOSeek.3 RIFFIOTell.3
linkman riffio/doc/man/rwbytes.man RIFFIORW.3 \
	RIFFIORead8.3 RIFFIORead16.3 RIFFIORead32.3 RIFFIOReadFOURCC.3 \
	RIFFIOWrite8.3 RIFFIOWrite16.3 RIFFIOWrite32.3 RIFFIOWriteFOURCC.3
linkman riffio/doc/man/stack.man RIFFIOChunkStack.3 \
	RIFFIOChunkStackNew.3 RIFFIOChunkStackDelete.3 \
	RIFFIOChunkStackPush.3 RIFFIOChunkStackPop.3 \
	RIFFIOChunkStackTop.3 RIFFIOChunkStackIsEmpty.3
linkman riffio/doc/man/stdcriff.man STDCRIFF.3 \
	STDCRIFFRead.3 STDCRIFFWrite.3 STDCRIFFSeek.3 STDCRIFFTell.3
linkman riffio/doc/man/table.man RIFFIOFCCTable.3 \
	RIFFIOFCCTableNew.3 RIFFIOFCCTableDelete.3 \
	RIFFIOFCCTableMakeEntry.3 RIFFIOFCCTableLookup.3 RIFFIOFCCTableCount.3 \
	RIFFIOFCCTableCreateArray.3 RIFFIOFCCTableFreeEntries.3 \
	RIFFIOFCCTableForEachEntry.3 RIFFIOFCCTableDump.3

install niffio/doc/man/nif001.man $RPM_BUILD_ROOT%{_mandir}/man1/nif001.1
install niffio/doc/man/niffdump.man $RPM_BUILD_ROOT%{_mandir}/man1/niffdump.1
install niffio/doc/man/niffio.man $RPM_BUILD_ROOT%{_mandir}/man3/niffio.3
linkman niffio/doc/man/clt.man NIFFIOCLT.3 \
	NIFFIOCLTNew.3 NIFFIOCLTDelete.3 \
	NIFFIOCLTMakeEntry.3 NIFFIOCLTMakeDefaultEntries.3 \
	NIFFIOCLTLookup.3 NIFFIOCLTCount.3 NIFFIOCompareFOURCC.3
linkman niffio/doc/man/inherit.man NIFFIORW.3 \
	NIFFIOFileGetFormType.3 \
	NIFFIORead.3 NIFFIOWrite.3 NIFFIOSeek.3 NIFFIOTell.3 \
	NIFFIOChunkCreate.3 NIFFIOChunkFinalize.3 \
	NIFFIOChunkDescend.3 NIFFIOChunkAscend.3 \
	NIFFIOChunkDataSeek.3 NIFFIOChunkDataEnd.3 NIFFIOChunkEnd.3 \
	NIFFIOWrite8.3 NIFFIOWrite16.3 NIFFIOWrite32.3 NIFFIOWriteFOURCC.3 \
	NIFFIORead8.3 NIFFIORead16.3 NIFFIORead32.3 NIFFIOReadFOURCC.3
linkman niffio/doc/man/names.man NIFFIOName.3 \
	NIFFIONameListType.3 NIFFIONameChunkId.3 NIFFIONameTagId.3 \
	NIFFIOSymbolTS.3 NIFFIOSymbolBAREXT.3 NIFFIOSymbolBARTYPE.3 \
	NIFFIOSymbolCLEFSHAPE.3 NIFFIOSymbolCLEFOCT.3 NIFFIOSymbolNOTESHAPE.3 \
	NIFFIOSymbolREST.3 NIFFIOSymbolLOGPLACEV.3 NIFFIOSymbolLOGPLACEPROX.3
linkman niffio/doc/man/nfile.man NIFFIOFile.3 \
	NIFFIOFileNew.3 NIFFIOFileNewSTDC.3 \
	NIFFIOFileInit.3 NIFFIOFileDelete.3 \
	NIFFIOFileGetCLT.3 NIFFIOFileReadCLT.3 NIFFIOFileAdoptCLT.3 \
	NIFFIOFileSeekChunkTags.3
linkman niffio/doc/man/parse.man NIFFIOParser.3 \
	NIFFIOParserNew.3 NIFFIOParserDelete.3 \
	NIFFIOParserSetTracing.3 NIFFIOParserGetTracing.3 \
	NIFFIOParseFile.3
linkman niffio/doc/man/register.man NIFFIORegister.3 \
	NIFFIORegisterDefaultList.3 NIFFIORegisterDefaultChunk.3 \
	NIFFIORegisterDefaultAtomicChunk.3 NIFFIORegisterDefaultTag.3 \
	NIFFIORegisterForm.3 NIFFIORegisterList.3 NIFFIORegisterAtomicChunk.3 \
	NIFFIORegisterListXXX.3 NIFFIORegisterChunkXXX.3 NIFFIORegisterTagXXX.3
linkman niffio/doc/man/rwniff.man NIFFIORWniff.3 \
	NIFFIOWriteniffXXX.3 NIFFIOReadniffXXX.3
linkman niffio/doc/man/rwtypes.man NIFFIORWtypes.3 \
	NIFFIOReadBYTE.3 NIFFIOReadCHAR.3 NIFFIOReadSIGNEDBYTE.3 \
	NIFFIOReadSHORT.3 NIFFIOReadLONG.3 NIFFIOReadRATIONAL.3 \
	NIFFIOReadSTROFFSET.3 NIFFIOReadFONTIDX.3 \
	NIFFIOWriteBYTE.3 NIFFIOWriteCHAR.3 NIFFIOWriteSIGNEDBYTE.3 \
	NIFFIOWriteSHORT.3 NIFFIOWriteLONG.3 NIFFIOWriteRATIONAL.3 \
	NIFFIOWriteSTROFFSET.3 NIFFIOWriteFONTIDX.3
linkman niffio/doc/man/stbl.man NIFFIOStblWrite.3
linkman niffio/doc/man/store.man NIFFIOStorage.3 \
	NIFFIOStorageNew.3 NIFFIOStorageInit.3 \
	NIFFIOStorageNewSTDC.3 NIFFIOStorageDelete.3 \
	NIFFIOStorageGetCurrent.3 NIFFIOStorageSetCurrent.3 \
	NIFFIOStorageGetFile.3 NIFFIOStorageIsListPending.3 \
	NIFFIOStorageIsChunkPending.3 NIFFIOStorageIsTagPending.3 \
	NIFFIOStoragePendingList.3 NIFFIOStoragePendingChunk.3 \
	NIFFIOStoragePendingTag.3 \
	NIFFIOStorageListStart.3 NIFFIOStorageListEnd.3 \
	NIFFIOStorageChunkStart.3 NIFFIOStorageChunkEnd.3 \
	NIFFIOStorageTagStart.3 NIFFIOStorageTagEnd.3 \
	NIFFIOStoreStbl.3 NIFFIOStoreCLT.3 NIFFIOStoreDefaultCLT.3
linkman niffio/doc/man/storenif.man NIFFIOstore.3 \
	NIFFIOStartXXX.3 NIFFIOEndXXX.3 NIFFIOchunkXXX.3 NIFFIOtagXXX.3
linkman niffio/doc/man/tags.man NIFFIOTag.3 \
	NIFFIOTagCreate.3 NIFFIOTagFinalize.3 \
	NIFFIOTagDescend.3 NIFFIOTagAscend.3

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc doc/htm/*.htm
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_libdir}/lib*.so.*.*.*
%{_mandir}/man1/*

%files devel
%defattr(644,root,root,755)
%doc html-doc/*
%attr(755,root,root) %{_libdir}/lib*.so
%{_libdir}/*.la
%{_includedir}
%{_mandir}/man3/*

%files static
%defattr(644,root,root,755)
%{_libdir}/*.a
