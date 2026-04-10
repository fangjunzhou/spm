import logging

from spm.package_manager import SlangPackageManager, packages
from package_a.package_a import PackageA
from package_b.package_b import PackageB
from package_c.package_c import PackageC

logger = logging.getLogger(__name__)


def test_package_manager_init_with_package_a_b_and_c():
    packages.clear()
    SlangPackageManager.register_package(PackageA)
    SlangPackageManager.register_package(PackageB)
    SlangPackageManager.register_package(PackageC)

    manager = SlangPackageManager()
    logger.info(f"SlangPackageManager device: {manager.device}")
    logger.info(f"SlangPackageManager module map: {manager.module_map}")
    assert (
        len(manager.module_map) == 3
    ), "Expected 3 packages to be registered in the module map."
