Name:           sspcpp999
Version:        1.0
Release:        1%{?dist}
Summary:        A simple demonstration that uses C++14 features

License:        CC-BY-3.0

BuildRequires:  gcc-c++

%description
A package demonstrating C++14 library features as listed at
https://en.cppreference.com/w/cpp/14

%prep
cat <<EOF > %{name}.cc
// https://en.cppreference.com/w/cpp/thread/shared_timed_mutex
#include <mutex>
#include <shared_mutex>

class R
{
    mutable std::shared_timed_mutex mut;
    /* data */
public:
    R& operator=(const R& other)
    {
        // requires exclusive ownership to write to *this
        std::unique_lock<std::shared_timed_mutex> lhs(mut, std::defer_lock);
        // requires shared ownership to read from other
        std::shared_lock<std::shared_timed_mutex> rhs(other.mut, std::defer_lock);
        std::lock(lhs, rhs);
        /* assign data */
        return *this;
    }
};

int main()
{
    R r;
}
EOF

%build
g++ -o %{name} %{name}.cc

%install
mkdir -p $RPM_BUILD_ROOT/%{_bindir}
cp %{name} $RPM_BUILD_ROOT/%{_bindir}

%files
%{_bindir}/%{name}

%changelog
* Tue Dec 31 2024 John W. O'Brien <john@saltant.com> - 1.0-1
- Initial sspcpp999 package
