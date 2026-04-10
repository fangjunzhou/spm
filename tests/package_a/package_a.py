from pathlib import Path
import slangpy as spy

from spm.package import SlangPackage
from spm.package_manager import SlangPackageManager

SHADER_PATH = Path(__file__).parent / "slang"


class PackageA(SlangPackage):
    @staticmethod
    def name() -> str:
        return "PackageA"

    @staticmethod
    def shader_paths() -> list[str]:
        return [str(SHADER_PATH)]

    @staticmethod
    def dependencies() -> list[type[SlangPackage]]:
        return []

    def build(self) -> spy.Module:
        module = spy.Module.load_from_file(
            device=self._device,
            path="package_a.slang",
            link=self._dependencies,
        )
        return module


SlangPackageManager.register_package(PackageA)
