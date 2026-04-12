from pathlib import Path
import slangpy as spy

from spm_slang.package import SlangPackage
from spm_slang.package_manager import SlangPackageManager

SHADER_PATH = Path(__file__).parent / "slang"


class PackageE(SlangPackage):
    @staticmethod
    def name() -> str:
        return "PackageE"

    @staticmethod
    def shader_paths() -> list[str]:
        return [str(SHADER_PATH)]

    @staticmethod
    def dependencies() -> list[type[SlangPackage]]:
        from package_f.package_f import PackageF

        return [PackageF]

    def build(self) -> spy.Module:
        module = spy.Module.load_from_file(
            device=self._device,
            path="package_e.slang",
            link=self._dependencies,
        )
        return module


SlangPackageManager.register_package(PackageE)
