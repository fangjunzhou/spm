import logging
import sys

from spm.package_manager import SlangPackageManager, packages

logger = logging.getLogger(__name__)


def test_package_manager_init_with_package_c_only():
    packages.clear()

    # Force a fresh import so PackageC transitively registers PackageA and PackageB.
    sys.modules.pop("package_a.package_a", None)
    sys.modules.pop("package_b.package_b", None)
    sys.modules.pop("package_c.package_c", None)

    import package_c.package_c

    manager = SlangPackageManager()
    logger.info(f"SlangPackageManager device: {manager.device}")
    logger.info(f"SlangPackageManager module map: {manager.module_map}")
    assert (
        len(manager.module_map) == 3
    ), "Expected importing package_c to register packages A, B, and C."
