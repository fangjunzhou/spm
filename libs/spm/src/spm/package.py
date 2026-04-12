from __future__ import annotations
from typing import List
import slangpy as spy


class SlangPackage:
    """Base class for Slang packages."""

    def __init__(self, device: spy.Device, dependencies: List[spy.Module]) -> None:
        self._device = device
        self._dependencies = dependencies
        self._module = self.build()

    @staticmethod
    def name() -> str:
        """The unique name of the package.

        :return: The name of the package. This method should be implemented by subclasses to return the name of the package.
        """
        raise NotImplementedError(
            "Subclasses must implement the name method to return the package name."
        )

    @staticmethod
    def shader_paths() -> List[str]:
        """The shader_paths device should include.

        :return: A list of file paths to the shader files that should be included in the package.
        """
        raise NotImplementedError(
            "Subclasses must implement the shader_paths method to return a list of shader file paths."
        )

    @staticmethod
    def dependencies() -> List[type[SlangPackage]]:
        """The dependencies of this package.

        :return: A list of SlangPackage classes that this package depends on. This method should be implemented by subclasses to specify the dependencies of the package.
        """
        return []

    def build(self) -> spy.Module:
        """Build the Slang module for this package.

        :return: A Slang module that represents the package. This method should be implemented by subclasses to define the contents of the package.
        """
        raise NotImplementedError("Subclasses must implement the build method.")
