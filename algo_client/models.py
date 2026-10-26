from pydantic import BaseModel
from enum import Enum

from typing import Annotated, Any, Final


MAX_CSD_POINTS_FREE = 256

LICENSE_TEXT: Final[Annotated[str, 'MIT License text']] = (
"""
Copyright (c) 2026 Andrei V. Keino

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

"""
)


class TestItem(BaseModel):
    name: str
    price: float
    message: str=''
    total_with_tax: float=-1.0
    os_name: str=''
    os_version: str=''
    os_release: str=''
    machine: str=''


class AlgorithmType(str, Enum):
    """
    the enumeration for the algorithm type 
    #
    values:
    #
    ALGO_WITHOUT_POSTPROCESSING means simplest algorithm 
    without postprocessing
    # 
    POSTPROCESSING_V1 means advanced algorithm 
    which chooses the 'best' constant state section
    with the minimal height from sections those that 
    have the maximal length from a continuous constant 
    state section series
    #    
    see also: 
    https://figshare.com/articles/preprint/The_effective_algorithm_for_constant_state_detection_in_time_series_V_2_3_/28375532?file=56562641
    """
    ALGO_WITHOUT_POSTPROCESSING = 'ALGO_WITHOUT_POSTPROCESSING'
    POSTPROCESSING_V1 = 'POSTPROCESSING_V1'


class WindowHeightType(str, Enum):
    """
    the enumeration to choose between two types of maximal window height
    values: 
    #
    Absolute:
    Means just the window height
    #
    Relative:
    maximal window height is calcukated as 
    <absolute window height> / (<max(time series>  - min(time series))
    #    
    see also: 
    https://figshare.com/articles/preprint/The_effective_algorithm_for_constant_state_detection_in_time_series_V_2_3_/28375532?file=56562641
    """
    Absolute = 'absolute'
    Relative = 'relative'


class CSD_Data(BaseModel):
    """
    class to hold the Constant State Detection algorithm data
    #
    values:
    # 
    csd_algo_input: 
        [in] input timeseries 
    # csd_algo_min_window_width: 
        [in] minimal window width
    # csd_algo_max_window_length: 
        [in] maximal window height
    # Algo_Type: 
        [in] AlgorithmType value
    # Window_Height_Type: 
        [in] WindowHeightType value
    # start: 
        [out] list of start constant section series indexes inclusive
    # finish: 
        [out] list of finish constant section series indexes inclusive
    # start_section_series: 
        [out] list of start continuous constant 
        state section indexes inclusive
    # finish_section_series: 
        [out] list of finish continuous constant 
        state section indexes inclusive
    # api_key: 
        [in] reserved for future use
    # csd_algo_info: 
        [out] list of information strings
    # csd_algo_warnings: 
        [out] list of warning strings
    # csd_algo_errors: 
        [out] list of error strings
    # 
    see also: 
    https://figshare.com/articles/preprint/The_effective_algorithm_for_constant_state_detection_in_time_series_V_2_3_/28375532?file=56562641

    """

    csd_algo_input: list[float]
    csd_algo_min_window_width: int
    csd_algo_max_window_height: float
    Algo_Type: AlgorithmType = AlgorithmType.POSTPROCESSING_V1
    Window_Height_Type: WindowHeightType = WindowHeightType.Relative
    start: list[int] = []
    finish: list[int] = []
    start_section_series: list[int] = []
    finish_section_series: list[int] = []
    api_key: str = ''
    csd_algo_info: list[str] = []
    csd_algo_warnings: list[str] = []
    csd_algo_errors: list[str] = []


def to_jsonable_dict(model: BaseModel) -> dict[str, Any]:
    """
    function returns the json representation of the Pydantic model
    """
    return model.model_dump(mode='json')
