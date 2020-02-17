PyTorch implementation of Sparse Shift Layer(SSL)(currently for 4D tensors HxCxHxW) from "All You Need is a Few Shifts: Designing Efficient Convolutional Neural Networks
for Image Classification" (https://arxiv.org/pdf/1903.05285.pdf) 

Shift operation: shifts tensor data(in memory) by indexes. Value and direction of shift are learnable and different between channels.
It might be considered as Zero-FLOP replacement of DepthWise Convolution, wiht 4.5x less memory consumption(in compare wiht 3x3 DepthWise ConvD).

Sparse Shift Layer is quantized and sparse version of Active Shift(https://arxiv.org/pdf/1806.07370.pdf), which in turn learnable version of the GroupedShift(https://arxiv.org/pdf/1711.08141.pdf)

![alt text](https://github.com/DeadAt0m/ActiveSparseShifts-PyTorch/raw/master/shifts.png "Shifts evolution")


Note: by default shift is not circular, it's filling stayed out values(after shift) by 0.

## Requirements:
    PyTorch >= 1.4.0

## Instalation:
    1. Run *python setup.py build_ext* - this builds cpp extensions for CPU and GPU(if detected)
    2. *python setup.py install*  - for install.
    
## Using:
    
    from torchshifts import Shift2D
    shift_layer = Shift2D(in_channels=3)

There is additional options for shift layer:

    padding(str) - Padding added to the input during bilinear interpolation(currently, during backward pass).
                   Allowed: ['zeros', 'border']. Default: 'zeros'.
    init_stride(float) - Border for uniform initialization of weights(shifts): [-init_stride;init_stride]. Default: 1.
    sparsity_term(float) - Strength of sparsity. Default: 5e-4.


## Further plans:
  1. Add tests
  2. Shift1D - layer for 3D tensor
  3. Forward/backward without rounding approximation as in(https://arxiv.org/abs/1806.07370)
