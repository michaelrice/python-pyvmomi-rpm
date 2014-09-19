%if 0%{?fedora}
%global _with_python3 1
%endif

%global pyvmomi_version 5.5.0-2014.1.1
%global pyvmomi_rpmversion %(echo %{pyvmomi_version} | tr "-" ".")

%{!?_licensedir:%global license %%doc}
%if 0%{?rhel} && 0%{?rhel} <= 6
%{!?__python2: %global __python2 /usr/bin/python2}
%{!?python2_sitelib: %global python2_sitelib %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%endif

Name:             python-pyvmomi
Version:          %{pyvmomi_rpmversion}
Release:          2%{?dist}
Summary:          VMware vSphere Python SDK
Group:            Development/Languages
License:          ASL 2.0
URL:              https://pypi.python.org/pypi/pyvmomi
Source0:          https://pypi.python.org/packages/source/p/pyvmomi/pyvmomi-%{pyvmomi_version}.tar.gz

BuildRequires:    python2-devel python-setuptools
Requires:         python-requests python-six
BuildArch:        noarch
# This patch is needed as a temporary workaround to keep files
# from being added to /usr Upstream has accepted this patch
# but is holding off on another bug release for now
# it also makes the rpmlint warnings about scripts being
# non executable go away by removing the #! line from the
# offending files.
Patch0:           setuppy.patch

%description
pyVmomi is the Python SDK for the VMware vSphere API that allows you to manage 
ESX, ESXi, and vCenter.


%if 0%{?_with_python3}
%package -n python3-pyvmomi
Summary:          VMware vSphere Python SDK
BuildRequires:    python3-devel python3-setuptools
Requires:         python3-requests python3-six

%description -n python3-pyvmomi
pyVmomi is the Python SDK for the VMware vSphere API that allows you to manage 
ESX, ESXi, and vCenter.
%endif


%prep
%setup -q -n pyvmomi-%{pyvmomi_version}
# Apply temp patch
%patch0 -p1
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

# Leaving this out until we get the vcrpy and contextdecorator deps
# packaged and added into fedora.
#%check
#%{__python2} setup.py test
#
#%if 0%{?_with_python3}
#pushd %{py3dir}
#%{__python3} setup.py test
#popd
#%endif # with_python3


%files
%defattr(-,root,root,-)
%license LICENSE.txt
%doc README.rst NOTICE.txt
%{python_sitelib}/*

%if 0%{?_with_python3}
%files -n python3-pyvmomi
%license LICENSE.txt
%doc README.rst NOTICE.txt
%{python3_sitelib}/*
%endif


%changelog
* Thu Sep 18 2014 Michael Rice <michael@michaelrice.org> - 5.5.0.2014.1.1-2
- Changes to spec from review suggestions

* Sun Aug 31 2014 Michael Rice <michael@michaelrice.org> - 5.5.0.2014.1.1-1
- Bugfix release from upstream.

* Fri Aug 22 2014 Michael Rice <michael@michaelrice.org> - 5.5.0.2014.1-2
- Changes to spec file based on bugzilla package review.

* Wed Aug 20 2014 Michael Rice <michael@michaelrice.org> - 5.5.0.2014.1-1
- Initial RPM build.
