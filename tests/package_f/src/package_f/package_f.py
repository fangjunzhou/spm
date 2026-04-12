from pathlib import Path
import slangpy as spy

from spm_slang.package import SlangPackage
from spm_slang.package_manager import SlangPackageManager

SHADER_PATH = Path(__file__).parent / "slang"


class PackageF(SlangPackage):
    @staticmethod
    def name() -> str:
        return "PackageF"

    @staticmethod
    def shader_paths() -> list[str]:
        return [str(SHADER_PATH)]

    @staticmethod
    def dependencies() -> list[type[SlangPackage]]:
        from package_e.package_e import PackageE

        return [PackageE]

    def build(self) -> spy.Module:
        module = spy.Module.load_from_file(
            device=self._device,
            path="package_f.slang",
            link=self._dependencies,
        )
        return module


SlangPackageManager.register_package(PackageF)
