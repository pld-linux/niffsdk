Summary:	-
Summary(pl):	-
Name:		niffsdk
Version:	1.02
Release:	1
License:	Public Domain
Group:		Libraries
Source0:	http://www.musique.umontreal.ca/personnel/Belkin/N/%{name}-%{version}.tar
URL:		http://www.musique.umontreal.ca/personnel/Belkin/NIFF.doc.html
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description

%description -l pl

%prep
%setup -q -n %{name}%{version}

%build
%configure2_13
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
