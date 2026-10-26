import math
from enum import IntEnum
from typing import Any, Union
import numpy as np
from django.conf import settings
from django.contrib import messages
import requests
from django.core.files.uploadedfile import UploadedFile
from django.http import HttpRequest
from django.shortcuts import render
from algo_client.models import CSD_Data, WindowHeightType, to_jsonable_dict, AlgorithmType
from algorithm_website_project.settings import URL_CSD_ALGO
from constant_state_detection.file_upload_handlers import AbortUploadHandler
from constant_state_detection.forms import CsdModelFormAbsWndH, CsdModelFormRelWndH, CsdUserdataFormAbsWndH, \
    CsdUserdataFormRelWndH, alg_value_simple
from constant_state_detection.simple_axiliary import get_max_upload_file_size_kb, get_max_upload_file_size_bytes


class AlgorithmTypeInner(IntEnum):
    ALGO_WITHOUT_POSTPROCESSING = 1
    ALGO_POSTPROCESSING_V1 = 2

def insert_abort_upload_handler(request: HttpRequest):
    request.upload_handlers.insert(0, AbortUploadHandler(
        request, get_max_upload_file_size_bytes()))


def add_settings_vals_to_context(d: dict[str, Any]):
    d['MAX_POINTS_CSD'] = settings.MAX_POINTS_CSD
    d['MAX_POINTS_CSD_1'] = settings.MAX_POINTS_CSD_1
    d['max_upload_file_size_kb'] = f'{get_max_upload_file_size_kb()} kB'


def download_and_read_csd_file(request: HttpRequest) -> np.ndarray | None:
    # here

    # django upload file by chunks size limit
    # https://docs.djangoproject.com/en/6.0/topics/http/file-uploads/
    # https://docs.djangoproject.com/en/6.0/ref/settings/#file-upload-settings
    # django MultiValueDict' object has no attribute 'chunks'
    # MAX_FILE_SIZE = get_max_upload_file_size()
    #
    # request.upload_handlers.insert(0, AbortUploadHandler(
    #     request, get_max_upload_file_size()))

    form_file: UploadedFile | list[object] = request.FILES['file']

    ba = bytearray()
    for chunk in form_file.chunks():
        # print(f'type(chunk) = {type(chunk)}')
        ba += chunk

    arr_str = ba.decode(encoding="utf-8")
    # print(f'arr_str = {arr_str}')
    arr = None
    try:
        s = arr_str.split('\n')
        ss = []

        for i in range(len(s)):
            if len(s[i]):
                ss.append(float(s[i]))
        arr = np.asarray(ss, dtype=np.float64)
        if arr.dtype != np.float64:
            raise ValueError('Downloaded file should have float64 type')

        lines = arr.shape[0]
        if lines > settings.MAX_POINTS_CSD:
            msg = (f'Error: csv file data point count should be '
                   f' less or equal than {settings.MAX_POINTS_CSD}, '
                   f'but your file has {lines} data points'
                   )
            messages.error(request, msg)

    except Exception as e:
        messages.error(
            request,
            f'Error reading your file: {str(e)}')
    # print('arr eee = ', arr)
    return arr


def get_all_csd_form_data(
        form: Union[CsdModelFormAbsWndH,
        CsdModelFormRelWndH,
        CsdUserdataFormAbsWndH,
        CsdUserdataFormRelWndH,],
        # form_file: UploadedFile | list[object] | None,
        request: HttpRequest | None,
        ):
    file_data_arr: np.ndarray | None = None
    if request:
        file_data_arr = download_and_read_csd_file(request)

    data = form.cleaned_data
    if not request:
        beta = float(data['beta'])
        phi = float(data['phi'])
    else:
        beta = 0.0
        phi = 0.0

    window_min_len = int(data['window_min_len'])
    window_max_height = float(data['window_max_height'])
    algo_type_str = form.cleaned_data['algo_type']
    algo_type = AlgorithmTypeInner.ALGO_POSTPROCESSING_V1
    # if algo_type_str == 'awp':
    if algo_type_str == alg_value_simple:
        algo_type = AlgorithmTypeInner.ALGO_WITHOUT_POSTPROCESSING

    # print(f'algo_type = {algo_type}')
    return (beta, phi, window_min_len, window_max_height, algo_type,
            file_data_arr)


def calc_algo_output(file_data_arr: np.ndarray|None,
                     b: float,
                     phi: float,
                     max_win_height: float,
                     min_win_len: int,
                     algo_type,
                     win_height_relative: bool
                     # True if window height is relative
                     ):
    ex_str: str = ''
    periods = 1
    points_cnt = int(periods * settings.MAX_POINTS_CSD)
    phase = phi * math.pi
    y: np.ndarray|None = file_data_arr
    x = None
    if y is not None:
        x = np.arange(y.shape[0])

    (ret, start, finish,
    start_section_series, finish_section_series,
     y_min, y_max) = (
        None, None, None, None, None, None, None)

    try:
        if file_data_arr is None:
            points = int(periods * points_cnt)
            x = np.arange(points)
            y = np.sin(2.0 * np.pi * periods * x / points)
            # y: np.ndarray = np.zeros([points], np.float64)
            sin2 = b * np.sin(4.0 * np.pi * periods * x / points + phase)
            # print(f'len(y) = {len(y)}, len(sin2) = {len(sin2)}')
            y += sin2
            file_data_arr = y

        csd_data = CSD_Data(csd_algo_input=file_data_arr.tolist(),
                                csd_algo_min_window_width=min_win_len,
                                csd_algo_max_window_height=max_win_height)
        if not win_height_relative:
            csd_data.Window_Height_Type = WindowHeightType.Absolute

        if algo_type == AlgorithmTypeInner.ALGO_WITHOUT_POSTPROCESSING:
            csd_data.Algo_Type = AlgorithmType.ALGO_WITHOUT_POSTPROCESSING


        y_min = np.amin(y)
        y_max = np.amax(y)

        try:
            jsn = to_jsonable_dict(csd_data)
            print(f'jsn = {jsn["Algo_Type"]}')
            response = requests.post(URL_CSD_ALGO,
                                     json=jsn)
            out_data = CSD_Data.model_validate(response.json())
            return ('',
                x.tolist(),
                out_data.csd_algo_input,
                0,
                out_data.start,
                out_data.finish,
                out_data.start_section_series,
                out_data.finish_section_series,
                y_min,
                y_max)

        except Exception as e:
            return ('Server error',
                    [],
                    [],
                    ret,
                    [],
                    [],
                    [],
                    [],
                    0.0,
                    0.0)

    except Exception as e:
        ex_str = str(e)

    return (ex_str, x.tolist(), y.tolist(), ret, start, finish,
            start_section_series, finish_section_series,
            y_min, y_max)


def add_csd_diff_tbl_to_ctx(ct, start, finish, key_name):
    out_arr = []
    for i in range(len(start)):
        out_arr.append(
            {
                'start': start[i],
                'finish': finish[i],
                'diff_len': finish[i] - start[i] + 1,
            }
        )

    ct[key_name] = out_arr


def render_algo_response(request, ctx):
    # print('in render_algo_response')
    response = render(request,
                      'csd_form_page.html#form-container',
                      ctx)
    return response
