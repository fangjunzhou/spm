import logging

from spm.package_manager import SlangPackageManager, packages
from package_a.package_a import PackageA

logger = logging.getLogger(__name__)


def test_package_manager_init_with_package_a_only():
    packages.clear()
    SlangPackageManager.register_package(PackageA)

    manager = SlangPackageManager()
    logger.info(f"SlangPackageManager device: {manager.device}")
    logger.info(f"SlangPackageManager module map: {manager.module_map}")
    assert (
        len(manager.module_map) == 1
    ), "Expected 1 package to be registered in the module map."
