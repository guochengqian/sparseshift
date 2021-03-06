from torch import nn
import torch
from torchshifts.functional import shift1d_func, shift2d_func, shift3d_func

paddings_dict = {'zeros':0, 'border':1, 'periodic':2, 'reflect':3, 'symmetric':4}


class _Shiftnd(nn.Module):
    """
        Arguments:
            in_channels(int) – Number of channels in the input image.
            padding(str) - Padding added to the input during shift.
                           Allowed: ['zeros', 'border', 'periodic', 'reflect', 'symmetric']. Default: 'zeros'.
            init_shift(float) - Border for uniform initialization of weights(shifts): [-init_stride;init_stride]. Default: 1.
            sparsity_term(float) - Strength of sparsity. Default: 5e-4.
            active_shift(bool) - Compute forward pass via bilinear interpolation. Default: False.
    """
    def __init__(self, in_channels, padding='zeros',
                 init_shift = 1,
                 sparsity_term=5e-4,
                 active_flag=False):
        super(_Shiftnd, self).__init__()
        assert padding.lower() in paddings_dict.keys(), f'incorrect padding option: {padding}'
        self.padding = paddings_dict[padding]
        self.sparsity_term = sparsity_term
        self.in_channels = in_channels
        self._init_weights(init_shift)
        self.__active_flag = active_flag
        self.__shift_func = self._init_shift_fn()

    def _init_shift_fn(self):
        raise NotImplemented
        
    def _init_weights(self, init_shift):
        self.weight = nn.Parameter(torch.Tensor(self.in_channels, self.dim))
        self.reset_parameters(init_shift)

    def reset_parameters(self, init_shift):
        self.weight.data.uniform_(-abs(init_shift), abs(init_shift))
    
    def _compute_weight_loss(self):
        return self.sparsity_term * torch.sum(torch.abs(self.weight))
                
    def forward(self, input):
        loss = self._compute_weight_loss() if bool(self.sparsity_term) else None
        return self.__shift_func(input, self.weight, self.padding, self.__active_flag), loss
    
    def extra_repr(self):
        pad = dict(zip(paddings_dict.values(),paddings_dict.keys()))[self.padding]
        active = f'Active shift on forward pass: {"Yes" if self.__active_flag else "No"}'
        sp = f'Sparse shift: {"Yes - sparsity strength: {}".format(self.sparsity_term) if bool(self.sparsity_term) else "No"}'
        return f'in_channels={self.in_channels}, padding_method={pad}, {active}, {sp}'


    
class Shift1d(_Shiftnd):
    """
        Performs (index)shift operation under 3D tensor. Zero-FLOPs replacement of Depth-Wise convolution.
        

        Notes: 
            - Shift values and directions is learnable for each channel.
            - Forward method is always return the two terms: output and loss
            - loss is None if sparsity_term  is greater than zero


        Arguments:
            in_channels(int) – Number of channels in the input image.
            padding(str) - Padding added to the input during shift.
                           Allowed: ['zeros', 'border', 'periodic', 'reflect', 'symmetric']. Default: 'zeros'.
            init_shift(float) - Border for uniform initialization of weights(shifts): [-init_stride;init_stride]. Default: 1.
            sparsity_term(float) - Strength of sparsity. Default: 5e-4.
            active_shift(bool) - Compute forward pass via bilinear interpolation. Default: False.
    """
    def __init__(self, in_channels, padding='zeros',
                 init_shift = 1, sparsity_term=5e-4, active_flag=False):
        self.dim = 1
        super(Shift1d, self).__init__(in_channels, padding, init_shift, sparsity_term, active_flag)
    
    def _init_shift_fn(self):
        return shift1d_func
    
class Shift2d(_Shiftnd):
    """
        Performs (index)shift operation under 4D(by h and w axes) tensor. Zero-FLOPs replacement of Depth-Wise convolution.
        

        Notes: 
            - Shift values and directions is learnable for each channel.
            - Forward method is always return the two terms: output and loss
            - loss is None if sparsity_term  is greater than zero


        Arguments:
            in_channels(int) – Number of channels in the input image.
            padding(str) - Padding added to the input during shift.
                           Allowed: ['zeros', 'border', 'periodic', 'reflect', 'symmetric']. Default: 'zeros'.
            init_stride(float) - Border for uniform initialization of weights(shifts): [-init_stride;init_stride]. Default: 1.
            sparsity_term(float) - Strength of sparsity. Default: 5e-4.
            active_shift(bool) - Compute forward pass via bilinear interpolation. Default: False.
    """
    def __init__(self, in_channels, padding='zeros',
                 init_shift = 1, sparsity_term=5e-4, active_flag=False):
        self.dim = 2
        super(Shift2d, self).__init__(in_channels, padding, init_shift, sparsity_term, active_flag)
    
    def _init_shift_fn(self):
        return shift2d_func
    

class Shift3d(_Shiftnd):
    """
        Performs (index)shift operation under 5D(by h, w and d axes) tensor. Zero-FLOPs replacement of Depth-Wise convolution.
        

        Notes: 
            - Shift values and directions is learnable for each channel.
            - Forward method is always return the two terms: output and loss
            - loss is None if sparsity_term  is greater than zero


        Arguments:
            in_channels(int) – Number of channels in the input image.
            padding(str) - Padding added to the input during shift.
                           Allowed: ['zeros', 'border', 'periodic', 'reflect', 'symmetric']. Default: 'zeros'.
            init_stride(float) - Border for uniform initialization of weights(shifts): [-init_stride;init_stride]. Default: 1.
            sparsity_term(float) - Strength of sparsity. Default: 5e-4.
            active_shift(bool) - Compute forward pass via bilinear interpolation. Default: False.
    """
    def __init__(self, in_channels, padding='zeros',
                 init_shift = 1, sparsity_term=5e-4, active_flag=False):
        self.dim = 3
        super(Shift3d, self).__init__(in_channels, padding, init_shift, sparsity_term, active_flag)
    
    def _init_shift_fn(self):
        return shift3d_func
    
