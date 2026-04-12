from pathlib import Path
import slangpy as spy

from spm.package import SlangPackage
from spm.package_manager import SlangPackageManager
from package_a.package_a import PackageA
from package_b.package_b import PackageB

SHADER_PATH = Path(__file__).parent / "slang"


class PackageC(SlangPackage):
    @staticmethod
    def name() -> str:
        return "PackageC"

    @staticmethod
    def shader_paths() -> list[str]:
        return [str(SHADER_PATH)]

    @staticmethod
    def dependencies() -> list[type[SlangPackage]]:
        return [PackageA, PackageB]

    def build(self) -> spy.Module:
        module = spy.Module.load_from_file(
            device=self._device,
            path="package_c.slang",
            link=self._dependencies,
        )
        return module


SlangPackageManager.register_package(PackageC)
