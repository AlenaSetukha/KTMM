from setuptools import Extension, setup
from Cython.Build import cythonize
import numpy


ext_modules = [Extension('c_verle4',
    sources=['c_verle4.pyx'], language='c++',
    extra_compile_args=['-fopenmp'], 
    extra_link_args=['-fopenmp'])]

setup(name = 'c_verle4', package_dir={'solvers.solver4': ''},
    ext_modules=cythonize(ext_modules), include_dirs=[numpy.get_include()])