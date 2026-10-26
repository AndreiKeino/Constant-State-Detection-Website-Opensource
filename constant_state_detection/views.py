import io
from typing import Any, Dict, List, Tuple, Union

import pandas as pd
from django.core.files.uploadhandler import StopUpload
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, FileResponse
from django.views.decorators.csrf import csrf_exempt, csrf_protect

from constant_state_detection.file_upload_handlers import AbortUploadHandler
from constant_state_detection.forms import (CsdModelFormAbsWndH,
                                            CsdModelFormRelWndH, CsdUserdataFormAbsWndH, CsdUserdataFormRelWndH)
from django.conf import settings
from django.contrib import messages
from constant_state_detection.view_axiliary import calc_algo_output, AlgorithmTypeInner, add_settings_vals_to_context, \
    add_csd_diff_tbl_to_ctx, get_all_csd_form_data, render_algo_response, get_max_upload_file_size_bytes, \
    insert_abort_upload_handler

from django.contrib.staticfiles import finders


def upload_file():
    pass

def csd_index(request: HttpRequest):

    ctx = {}
    add_settings_vals_to_context(ctx)
    return render (request,
                   'constant_state_detection.html',
                   ctx)

@csrf_protect
def csd_form_renderer(request: HttpRequest,
                          form_class_type: type,
                          page_header: str,
                          win_height_relative: bool,
                          has_user_data: bool
                      ) -> HttpResponse:

    ctx = {'page_header_text': page_header}
    add_settings_vals_to_context(ctx)
    # add the file input id to context
    if has_user_data:
        ctx['file_input_id'] = "id_file"

    # print(f"ctx['hx_target'] = {ctx['hx_target']}")
    form = form_class_type(
        request.POST or None,
        request.FILES or None,)
    ctx['form'] = form
    # ctx['test'] = [1, 2, 3]
    # print(f'type of ctx = {type(ctx)}')
    if request.method == "POST":
        # print('if request.method == "POST":')
        if form.is_valid():
            # print("if form.is_valid():")

            # print(f'has_user_data = {has_user_data}')

            try:
                (beta, phi, window_min_len,
                 window_max_height, algo_type,
                 file_data_arr) = get_all_csd_form_data(
                    form,
                    request if has_user_data else None)
                    # form_file=(request.FILES['file'] if user_data_form else None))
            except StopUpload as e:
                pass
                # print('Exception while : ', e)

            (ex_str, x, y, ret, start, finish,
             start_section_series,
             finish_section_series,
             y_min, y_max) = calc_algo_output(
                file_data_arr,
                beta, phi, window_max_height,
                window_min_len, algo_type,
                win_height_relative=win_height_relative)

            if ex_str:
                # print('if ex_str:')
                msg = f'Error <strong>\"{ex_str}\"</strong>'
                messages.error(request, msg)

            else:
                # print('if not ex_str:')
                ct = {}
                (ct['x'], ct['y'], ct['ret'],
                 ct['start'], ct['finish'],
                ct['start_section_series'],
                ct['finish_section_series'],
                 ct['y_min'], ct['y_max']) = (
                    x, y, ret, start,
                    finish, start_section_series,
                    finish_section_series,
                    y_min, y_max,
                )

                add_csd_diff_tbl_to_ctx(ct, start, finish,
                                        'csd_sections')

                add_csd_diff_tbl_to_ctx(ct, start_section_series,
                                        finish_section_series,
                                        'csd_regions')


                ctx['algo_output'] = ct
            # else:
            #     # not if (type(form_class_type) is type(CsdModelFormAbsWndH)
            #     # or
            #     # type(form_class_type) is type(CsdModelFormRelWndH)):
            #     # this one if of UserData form

        else:
            # print('if not form_is_valid:')
            form_errors = []
            for field, errors in form.errors.items():
                for error in errors:
                    msg = f"Error in <strong>\"{form[field].label}\"</strong> input; {error}"
                    messages.error(request, msg)

        return render_algo_response(request, ctx)

    else:
        return render(request,
                            'csd_form_page.html',
                            ctx)


def csd_model_abs_wnd_h(request: HttpRequest) -> HttpResponse:
    return csd_form_renderer(
        request=request,
         form_class_type= CsdModelFormAbsWndH,
         page_header='''Constant state detection algorithm 
                        for the model data for the absolute 
                        window minimal height''',
         win_height_relative=False,
        has_user_data=False)


def csd_model_rel_wnd_h(request: HttpRequest):

    return csd_form_renderer(
        request=request,
         form_class_type= CsdModelFormRelWndH,
         page_header='''Constant state detection algorithm for the 
                        model data for the relative window minimal 
                        height''',
         win_height_relative=True,
        has_user_data=False)


@csrf_exempt
def csd_userdata_abs_wnd_h(request: HttpRequest):

    insert_abort_upload_handler(request)
    return csd_form_renderer(
        request=request,
         form_class_type= CsdUserdataFormAbsWndH,
         page_header='''Constant state detection algorithm for a
                        user data for the absolute window
                        minimal height''',
         win_height_relative=False,
        has_user_data=True)


@csrf_exempt
def csd_userdata_rel_wnd_h(request: HttpRequest):

    insert_abort_upload_handler(request)
    return csd_form_renderer(
        request=request,
         form_class_type= CsdUserdataFormRelWndH,
         page_header='''Constant state detection algorithm for a user 
                        data for the relative window minimal height''',
         win_height_relative=True,
        has_user_data=True)


def csd_download_csv_example(request: HttpRequest):
    # https://github.com/dakixr/htmx-download/tree/main
    filepath = str(finders.find('csv/csd_app/256_points_1_periods.csv'))
    # searched_locations = finders.searched_locations

    with open(filepath, "rb") as fh:
        buf = io.BytesIO(fh.read())

    filename = "data_example.csv"
    return FileResponse(buf,
                        as_attachment=True,
                        filename=filename)

