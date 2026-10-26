# see /home/andrei/My_Projects/Pythonanywhere_Website/django_app_before_04_02_2026/fractals/forms.py
from typing import Final

from django import forms 
from django.conf import settings
import sys
import math

from constant_state_detection.simple_axiliary import get_max_upload_file_size_kb

TEST = False

B_MULT_INITIAL = 0.5

form_attrs_bs5 = {'class': 'form-control',}
num_daisy_5_attrs = {'class': 'input input-bordered w-full'}

num_form_attrs = num_daisy_5_attrs

float_form_attrs = {'class': 'input input-bordered w-full max-w-none no-arrows',
            'placeholder': 'Enter a float number',}

form_attrs_daisy = {'class': 'input input-bordered w-full max-w-none',}

file_attr_daisy = {"class": "file-input file-input-primary",
                   "accept": ".csv"}

form_file_attr = file_attr_daisy

alg_name_simple: Final[str] = 'Algorithm without postprocessing'
alg_value_simple: Final[str] = 'awp'

alg_name_postprocessing: Final[str] = 'Postprocessing type 1'
alg_value_postprocessing: Final[str] = 'ap1'

algorithm_name_tuple = (
    (alg_value_postprocessing, alg_name_postprocessing ),
    (alg_value_simple, alg_name_simple),
)

DOUBLE_MIN_STEP = 5e-323
DOUBLE_MIN_AFTER_0 = sys.float_info.min
DOUBLE_MAX_BEFORE_1 = math.nextafter(1.0, 0.0)
DOUBLE_MAX = sys.float_info.max


# MathML
# https://developer.mozilla.org/en-US/docs/Web/MathML/Tutorials/For_beginners/Getting_started

def create_algo_type_field():
    algo_type = forms.ChoiceField(
        choices=algorithm_name_tuple,
          label='Choose the algorithm postprocessing type:',
          widget=forms.Select(
              attrs=form_attrs_daisy)
          )
    return algo_type


def create_beta_field():
    beta = forms.FloatField(min_value=-1.0, max_value=1.0,
                           step_size=DOUBLE_MIN_STEP,
                           initial=B_MULT_INITIAL, # 0.5
                           label='Choose the β value in range [-1, 1]:',
                           widget=forms.NumberInput(attrs=float_form_attrs)
        )
    return beta


def create_phi_field():
    phi = forms.FloatField(
        min_value=-1.0, max_value=1.0,
        step_size=DOUBLE_MIN_STEP,
        initial=0.5, # 0.5
        label='Choose the φ value in range [-1, 1]:',
        widget=forms.NumberInput(attrs=float_form_attrs)
        )
    return phi


def create_window_min_len_field():
    window_min_len = forms.IntegerField(
        min_value=2,
        max_value=settings.MAX_POINTS_CSD,
        step_size=1,
        initial=16, # 0.5
        label=f'Choose the minimal window length in range [2, '
                f'{settings.MAX_POINTS_CSD - 1}]:',
        widget=forms.NumberInput(attrs=num_form_attrs)
    )
    return window_min_len


def create_window_max_rel_height_field():
    window_max_height =  forms.FloatField(
        min_value=DOUBLE_MIN_AFTER_0, max_value=DOUBLE_MAX_BEFORE_1,
        step_size=DOUBLE_MIN_STEP,
        initial=0.16, # 0.5
        label='Choose the relative maximal window height in range '
         ']0, 1[:',
        widget=forms.NumberInput(attrs=float_form_attrs)
    )
    return window_max_height


def create_window_max_abs_height_field():
    window_max_height =  forms.FloatField(
        min_value=DOUBLE_MIN_AFTER_0, max_value=DOUBLE_MAX,
        step_size=DOUBLE_MIN_STEP,
        initial=0.16, # 0.5
        label=f'Choose the absolute maximal window height in range '
        f']0, {DOUBLE_MAX}]:',
        widget=forms.NumberInput(attrs=float_form_attrs)
    )
    return window_max_height



class CsdFormPreBase(forms.Form): 
   algo_type = create_algo_type_field()


class CsdFormBase(CsdFormPreBase): 

    beta = create_beta_field()
    phi = create_phi_field()
    window_min_len = create_window_min_len_field()


# input form for the constant state detection algorithm with
# relative min. window height, without user data uploading
class CsdModelFormRelWndH(CsdFormBase): 
    window_max_height = create_window_max_rel_height_field()


# input form for the constant state detection algorithm with
# absolute min. window height, without user data uploading
class CsdModelFormAbsWndH(CsdFormBase):
    window_max_height = create_window_max_abs_height_field()


class CsdUserdataFormBase(CsdFormPreBase):
    window_min_len = create_window_min_len_field()


class CsdUserdataFormAbsMinLenBase(CsdUserdataFormBase):
    window_max_height = create_window_max_abs_height_field()


class CsdUserdataFormRelMinLenBase(CsdUserdataFormBase):
    window_max_height = create_window_max_rel_height_field()


def create_file_field():
    file = forms.FileField(
        label=f"Choose your csv data file, "
              f"max. size {get_max_upload_file_size_kb()} kB, "
              f"{settings.MAX_POINTS_CSD} points max.",
        widget = forms.FileInput(attrs=form_file_attr)
    )
    return file


# django file form field
# https://docs.djangoproject.com/en/6.0/topics/http/file-uploads/

# django max file size
# https://docs.djangoproject.com/en/6.0/topics/http/file-uploads/
class CsdUserdataFormAbsWndH(CsdUserdataFormAbsMinLenBase):
    file = create_file_field()


class CsdUserdataFormRelWndH(CsdUserdataFormRelMinLenBase):
    file = create_file_field()