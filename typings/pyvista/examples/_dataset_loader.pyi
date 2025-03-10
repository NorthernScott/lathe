"""
This type stub file was generated by pyright.
"""

import pyvista as pv
from abc import abstractmethod
from typing import Any, Generic, Protocol, Sequence, TYPE_CHECKING, Tuple, Type, TypeVar, Union, final, runtime_checkable
from pyvista.core._typing_core import NumpyArray
from collections.abc import Callable

"""Abstraction layer for downloading, reading, and loading dataset files.

The classes and methods in this module define an API for working with either
a single file or multiple files which may be downloaded and/or loaded as an
example dataset.

Many datasets have a straightforward input to output mapping:
    file -> read -> dataset

However, some file formats require multiple input files for reading (e.g.
separate data and header files):
    (file1, file1) -> read -> dataset

Or, a dataset may be combination of two separate datasets:
    file1 -> read -> dataset1 ┬─> combined_dataset
    file2 -> read -> dataset2 ┘

In some cases, the input may be a folder instead of a file (e.g. DICOM):
    folder -> read -> dataset

In addition, there may be a need to customize the reading function to read
files with specific options enabled (e.g. set a time value), or perform
post-read processing to modify the dataset (e.g. set active scalars).

This module aims to serve these use cases and provide a flexible way of
downloading, reading, and processing files with a generic mapping:
    file or files or folder -> fully processed dataset(s) in any form

"""
if TYPE_CHECKING:
    ...
_FilePropStrType_co = TypeVar('_FilePropStrType_co', str, Tuple[str, ...], covariant=True)
_FilePropIntType_co = TypeVar('_FilePropIntType_co', int, Tuple[int, ...], covariant=True)
DatasetObject = Union[pv.DataSet, pv.Texture, NumpyArray[Any], pv.MultiBlock]
DatasetType = Union[Type[pv.DataSet], Type[pv.Texture], Type[NumpyArray[Any]], Type[pv.MultiBlock],]
class _BaseFilePropsProtocol(Generic[_FilePropStrType_co, _FilePropIntType_co]):
    @property
    @abstractmethod
    def path(self) -> _FilePropStrType_co:
        """Return the path(s) of all files."""
        ...
    
    @property
    def num_files(self) -> int:
        """Return the number of files from path or paths.

        If a path is a folder, the number of files contained in the folder is returned.
        """
        ...
    
    @property
    def unique_extension(self) -> str | tuple[str, ...]:
        """Return the unique file extension(s) from all files."""
        ...
    
    @property
    @abstractmethod
    def total_size(self) -> str:
        """Return the total size of all files formatted as a string."""
        ...
    
    @property
    def unique_reader_type(self) -> type[pv.BaseReader] | tuple[type[pv.BaseReader], ...] | None:
        """Return unique reader type(s) from all file readers."""
        ...
    


class _SingleFilePropsProtocol(_BaseFilePropsProtocol[str, int]):
    """Define file properties of a single file."""
    ...


class _MultiFilePropsProtocol(_BaseFilePropsProtocol[Tuple[str, ...], Tuple[int, ...]]):
    """Define file properties of multiple files."""
    ...


@runtime_checkable
class _Downloadable(Protocol[_FilePropStrType_co]):
    """Class which downloads file(s) from a source."""
    @property
    @abstractmethod
    def source_name(self) -> _FilePropStrType_co:
        """Return the name of the download relative to the base url."""
        ...
    
    @property
    @abstractmethod
    def base_url(self) -> _FilePropStrType_co:
        """Return the base url of the download."""
        ...
    
    @property
    def source_url_raw(self) -> _FilePropStrType_co:
        """Return the raw source of the download.

        This is the full URL used to download the data directly.
        """
        ...
    
    @property
    def source_url_blob(self) -> _FilePropStrType_co:
        """Return the blob source of the download.

        This URL is useful for linking to the source webpage for
        a human to open on a browser.
        """
        ...
    
    @property
    @abstractmethod
    def path(self) -> _FilePropStrType_co:
        """Return the file path of downloaded file."""
        ...
    
    @abstractmethod
    def download(self) -> _FilePropStrType_co:
        """Download and return the file path(s)."""
        ...
    


class _DatasetLoader:
    """Load a dataset."""
    def __init__(self, load_func: Callable[..., DatasetObject]) -> None:
        ...
    
    @property
    @final
    def dataset(self) -> DatasetObject | None:
        """Return the loaded dataset object(s)."""
        ...
    
    def load(self, *args, **kwargs) -> DatasetObject:
        """Load and return the dataset."""
        ...
    
    @final
    def load_and_store_dataset(self) -> DatasetObject:
        """Load the dataset and store it."""
        ...
    
    @final
    def clear_dataset(self): # -> None:
        """Clear the stored dataset object from memory."""
        ...
    
    @property
    @final
    def dataset_iterable(self) -> tuple[DatasetObject, ...]:
        """Return a tuple of all dataset object(s), including any nested objects.

        If the dataset is a MultiBlock, the MultiBlock itself is also returned as the first
        item. Any nested MultiBlocks are not included, only their datasets.

        E.g. for a composite dataset:
            MultiBlock -> (MultiBlock, Block0, Block1, ...)
        """
        ...
    
    @property
    @final
    def unique_dataset_type(self) -> DatasetType | tuple[DatasetType, ...] | None:
        """Return unique dataset type(s) from all datasets."""
        ...
    
    @property
    @final
    def unique_cell_types(self) -> tuple[pv.CellType, ...]:
        """Return unique cell types from all datasets."""
        ...
    


class _SingleFile(_SingleFilePropsProtocol):
    """Wrap a single file."""
    def __init__(self, path) -> None:
        ...
    
    @property
    def path(self) -> str:
        ...
    
    @property
    def total_size(self) -> str:
        ...
    


class _SingleFileDatasetLoader(_SingleFile, _DatasetLoader):
    """Wrap a single file for loading.

    Specify the read function and/or load functions for reading and processing the
    dataset. The read function is called on the file path first, then, if a load
    function is specified, the load function is called on the output from the read
    function.

    Parameters
    ----------
    path
        Path of the file to be loaded.

    read_func
        Specify the function used to read the file. Defaults to :func:`pyvista.read`.
        This can be used for customizing the reader's properties, or using another
        read function (e.g. :func:`pyvista.read_texture` for textures). The function
        must have the file path as the first argument and should return a dataset.
        If default arguments are required by your desired read function, consider
        using :class:`functools.partial` to pre-set the arguments before passing it
        as an argument to the loader.

    load_func
        Specify the function used to load the file. Defaults to `None`. This is typically
        used to specify any processing of the dataset after reading. The load function
        typically will accept a dataset as an input and return a dataset.

    """
    def __init__(self, path: str, read_func: Callable[[str], DatasetType] | None = ..., load_func: Callable[[DatasetType], Any] | None = ...) -> None:
        ...
    
    @property
    def path_loadable(self) -> str:
        ...
    
    def load(self): # -> DatasetType | UnstructuredGrid | pyvista_ndarray | type[DataSet] | type[Texture] | type[ndarray[Any, dtype[Any]]] | type[MultiBlock] | None:
        ...
    


class _DownloadableFile(_SingleFile, _Downloadable[str]):
    """Wrap a single file which must be downloaded.

    If downloading a file from an archive, set the filepath of the zip as
    ``path`` and set ``target_file`` as the file to extract. If the path is
    a zip file and no target file is specified, the entire archive is downloaded
    and extracted and the root directory of the path is returned.

    """
    def __init__(self, path: str, target_file: str | None = ...) -> None:
        ...
    
    @property
    def source_name(self) -> str:
        ...
    
    @property
    def base_url(self) -> str:
        ...
    
    def download(self) -> str:
        ...
    


class _SingleFileDownloadableDatasetLoader(_SingleFileDatasetLoader, _DownloadableFile):
    """Wrap a single file which must first be downloaded and which can also be loaded.

    .. warning::

       ``download()`` should be called before accessing other attributes. Otherwise,
       calling ``load()`` or ``path`` may fail or produce unexpected results.

    """
    def __init__(self, path: str, read_func: Callable[[str], DatasetType] | None = ..., load_func: Callable[[DatasetType], DatasetType] | None = ..., target_file: str | None = ...) -> None:
        ...
    


class _MultiFileDatasetLoader(_DatasetLoader, _MultiFilePropsProtocol):
    """Wrap multiple files for loading.

    Some use cases for loading multi-file examples include:

    1. Multiple input files, and each file is read/loaded independently
       E.g.: loading two separate datasets for the example
       See ``download_bolt_nut`` for a reference implementation.

    2. Multiple input files, but only one is read or loaded directly
       E.g.: loading a single dataset from a file format where data and metadata are
       stored in separate files, such as ``.raw`` and ``.mhd``.
       See ``download_head`` for a reference implementation.

    3. Multiple input files, all of which make up part of the loaded dataset
       E.g.: loading six separate image files for cubemaps
       See ``download_sky_box_cube_map`` for a reference implementation.

    Parameters
    ----------
    files_func
        Specify the function which will return a sequence of :class:`_SingleFile`
        objects required for loading the dataset. Alternatively, a directory can be
        specified, in which case a separate single-file dataset loader is created
        for each file with a default reader.

    load_func
        Specify the function used to load the files. By default, :meth:`load()` is called
        on all the files (if loadable) and a tuple containing the loaded datasets is returned.

    """
    def __init__(self, files_func: str | Callable[[], Sequence[_SingleFileDatasetLoader | _DownloadableFile]], load_func: Callable[[Sequence[_SingleFileDatasetLoader]], Any] | None = ...) -> None:
        ...
    
    @property
    def path(self) -> tuple[str, ...]:
        ...
    
    @property
    def path_loadable(self) -> tuple[str, ...]:
        ...
    
    @property
    def total_size(self) -> str:
        ...
    
    def load(self): # -> DatasetObject:
        ...
    


class _MultiFileDownloadableDatasetLoader(_MultiFileDatasetLoader, _Downloadable[Tuple[str, ...]]):
    """Wrap multiple files for downloading and loading."""
    @property
    def source_name(self) -> tuple[str, ...]:
        ...
    
    @property
    def base_url(self) -> tuple[str, ...]:
        ...
    
    def download(self) -> tuple[str, ...]:
        ...
    


_ScalarType = TypeVar('_ScalarType', int, str, pv.BaseReader)
