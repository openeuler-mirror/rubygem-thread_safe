%global gem_name thread_safe
Name:                rubygem-%{gem_name}
Version:             0.3.6
Release:             2
Summary:             Thread-safe collections and utilities for Ruby
License:             ASL 2.0 and Public Domain
URL:                 https://github.com/ruby-concurrency/thread_safe
Source0:             https://rubygems.org/gems/thread_safe-%{version}.gem
BuildRequires:       ruby(release) rubygems-devel ruby rubygem(concurrent-ruby) rubygem(rspec)
BuildArch:           noarch
%description
A collection of data structures and utilities to make thread-safe
programming in Ruby easier.

%package help
Summary:             Documentation for %{name}
Requires:            %{name} = %{version}-%{release}
BuildArch:           noarch
Provides:            %{name}-doc = %{version}-%{release}
Obsoletes:           %{name}-doc < %{version}-%{release}
%description help
Documentation for %{name}.

%prep
gem unpack %{SOURCE0}
%setup -q -D -T -n  %{gem_name}-%{version}
gem spec %{SOURCE0} -l --ruby > %{gem_name}.gemspec

%build
gem build %{gem_name}.gemspec
%gem_install

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/
sed -i -e 's|^#!/usr/bin/env ruby|#!/usr/bin/ruby|' \
  %{buildroot}%{gem_instdir}/examples/bench_cache.rb

%check
pushd ./%{gem_instdir}
sed -i "/^require 'simplecov'/ s/^/#/" spec/spec_helper.rb
sed -i "/^SimpleCov.formatter/,/^end$/ s/^/#/" spec/spec_helper.rb
sed -i "/^require 'coveralls'/ s/^/#/" spec/spec_helper.rb
sed -i "/logger/ s/^/#/" spec/spec_helper.rb
rspec -Ilib spec

%files
%dir %{gem_instdir}
%exclude %{gem_instdir}/.*
%license %{gem_instdir}/LICENSE
%exclude %{gem_instdir}/ext
%{gem_libdir}
%exclude %{gem_instdir}/thread_safe.gemspec
%exclude %{gem_cache}
%{gem_spec}

%files help
%doc %{gem_docdir}
%{gem_instdir}/Gemfile
%doc %{gem_instdir}/README.md
%{gem_instdir}/Rakefile
%{gem_instdir}/examples
%{gem_instdir}/spec
%exclude %{gem_instdir}/spec/.gitignore
%exclude %{gem_instdir}/spec/support/.gitignore
%exclude %{gem_instdir}/spec/thread_safe/.gitignore
%{gem_instdir}/tasks
%{gem_instdir}/yard-template

%changelog
* Mon Feb 28 2021 huanghaitao <huanghaitao8@huawei.com> - 0.3.6-2
- Switch concurrent-ruby to disable atomic

* Sat Aug 22 2020 liyanan <liyanan32@huawei.com> - 0.3.6-1
- package init
