import pytest

from spm_slang.package_manager import SlangPackageManager, packages
from package_e.package_e import PackageE
from package_f.package_f import PackageF


def test_package_manager_circular_dependencies():
    packages.clear()
    SlangPackageManager.register_package(PackageE)
    SlangPackageManager.register_package(PackageF)

    with pytest.raises(ValueError, match="Cyclic dependency detected among packages"):
        SlangPackageManager()
