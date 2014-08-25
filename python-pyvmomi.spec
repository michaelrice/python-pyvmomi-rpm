%if 0%{?fedora}
%global _with_python3 1
%endif

%if 0%{?rhel} && 0%{?rhel} <= 6
%{!?__python2: %global __python2 /usr/bin/python2}
%{!?python2_sitelib: %global python2_sitelib %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%{!?python2_sitearch: %global python2_sitearch %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}
%endif

Name:       python-pyvmomi
Version:    5.5.0.2014.1
Release:    1%{?dist}
Summary:    VMware vSphere Python SDK

Group:      Development/Languages
License:    ASL 2.0
URL:        https://pypi.python.org/pypi/pyvmomi
Source0:    https://pypi.python.org/packages/source/p/pyvmomi/pyvmomi-5.5.0-2014.1.tar.gz

BuildRequires:  python2-devel python-setuptools
Requires:   python-requests python-six
BuildArch:      noarch

%description
pyVmomi is the Python SDK for the VMware vSphere API that allows you to manage 
ESX, ESXi, and vCenter.


%if 0%{?_with_python3}
%package -n python3-pyvmomi
Summary: VMware vSphere Python SDK
BuildRequires:  python3-devel python3-setuptools
Requires: python3-requests python3-six

%description -n python3-pyvmomi
pyVmomi is the Python SDK for the VMware vSphere API that allows you to manage 
ESX, ESXi, and vCenter.
%endif


%prep
%setup -q -n pyvmomi-5.5.0-2014.1
%if 0%{?_with_python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
%endif # with_python3

%build
%if 0%{?_with_python3}
pushd %{py3dir}
%{__python3} setup.py build
popd
%endif
%{__python2} setup.py build

%install
rm -rf $RPM_BUILD_ROOT
%if 0%{?_with_python3}
pushd %{py3dir}
%{__python3} setup.py install --skip-build --root $RPM_BUILD_ROOT
popd
%endif

%{__python2} setup.py install --skip-build --root $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc README.md
%{python_sitelib}/*.egg-info
%dir %{python_sitelib}/pyVmomi
%dir %{python_sitelib}/pyVim
%{python_sitelib}/pyVmomi/*
%{python_sitelib}/pyVim/*

%if 0%{?_with_python3}
%files -n python3-pyvmomi
%doc README.md
%{python3_sitelib}/*.egg-info
%{python3_sitelib}/pyVmomi/*
%{python3_sitelib}/pyVim/*
%endif



%changelog
* Wed Aug 20 2014 Michael Rice <michael@michaelrice.org> - 5.5.0-2014.1-1
- Initial RPM build
