# tutorial for git submodules

[git submodules](https://git-scm.com/book/en/v2/Git-Tools-Submodules)

```bash
mkdir extern
cd extern
git submodule add  https://github.com/pybind/pybind11.git
git checkout -b stable origin/stable
```

# tutorial for pybind11

[pybind11](https://pybind11.readthedocs.io/en/stable/installing.html)

## install 

```bash
pip install pybind11

brew install pybind11
```

## compile the test cases in git repository

```bash
cd extern/pybind11/
mkdir build
cd build
cmake ..
make check -j 4
```

## create a cpp file
```cpp
#include <pybind11/pybind11.h>
namespace py = pybind11;

int add(int i, int j) {
    return i + j;
}

// example: module name
PYBIND11_MODULE(example, m) {
    m.doc() = "pybind11 example plugin"; // optional module docstring

    // exposed API
    m.def("add", &add, "A function which adds two numbers");
}
```

## generate a .so file for python to import

```bash
# -o example.XXX 
# example : module name for import, must be equal to PYBIND11_MODULE(example, m)
c++ -O3 -Wall -shared -std=c++11 -undefined dynamic_lookup -fPIC $(python3-config --includes) -I ../extern/pybind11/include pybind11_test.cpp -o example$(python3-config --extension-suffix)
```

## import so file in python

```python
import example # assume .so and .py file in the same dir

a = example.add(1,2)
print(a)
```
