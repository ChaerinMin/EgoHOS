# Copyright (c) OpenMMLab. All rights reserved.
from unittest.mock import patch

import pytest
import torch

from submodules.EgoHOS.mmsegmentation.mmseg.models.decode_heads.decode_head import BaseDecodeHead
from .utils import to_cuda


@patch.multiple(BaseDecodeHead, __abstractmethods__=set())
def test_decode_head():

    with pytest.raises(AssertionError):
        # default input_transform doesn't accept multiple inputs
        BaseDecodeHead([32, 16], 16, num_classes=19)

    with pytest.raises(AssertionError):
        # default input_transform doesn't accept multiple inputs
        BaseDecodeHead(32, 16, num_classes=19, in_index=[-1, -2])

    with pytest.raises(AssertionError):
        # supported mode is resize_concat only
        BaseDecodeHead(32, 16, num_classes=19, input_transform='concat')

    with pytest.raises(AssertionError):
        # in_channels should be list|tuple
        BaseDecodeHead(32, 16, num_classes=19, input_transform='resize_concat')

    with pytest.raises(AssertionError):
        # in_index should be list|tuple
        BaseDecodeHead([32],
                       16,
                       in_index=-1,
                       num_classes=19,
                       input_transform='resize_concat')

    with pytest.raises(AssertionError):
        # len(in_index) should equal len(in_channels)
        BaseDecodeHead([32, 16],
                       16,
                       num_classes=19,
                       in_index=[-1],
                       input_transform='resize_concat')

    # test default dropout
    head = BaseDecodeHead(32, 16, num_classes=19)
    assert hasattr(head, 'dropout') and head.dropout.p == 0.1

    # test set dropout
    head = BaseDecodeHead(32, 16, num_classes=19, dropout_ratio=0.2)
    assert hasattr(head, 'dropout') and head.dropout.p == 0.2

    # test no input_transform
    inputs = [torch.randn(1, 32, 45, 45)]
    head = BaseDecodeHead(32, 16, num_classes=19)
    if torch.cuda.is_available():
        head, inputs = to_cuda(head, inputs)
    assert head.in_channels == 32
    assert head.input_transform is None
    transformed_inputs = head._transform_inputs(inputs)
    assert transformed_inputs.shape == (1, 32, 45, 45)

    # test input_transform = resize_concat
    inputs = [torch.randn(1, 32, 45, 45), torch.randn(1, 16, 21, 21)]
    head = BaseDecodeHead([32, 16],
                          16,
                          num_classes=19,
                          in_index=[0, 1],
                          input_transform='resize_concat')
    if torch.cuda.is_available():
        head, inputs = to_cuda(head, inputs)
    assert head.in_channels == 48
    assert head.input_transform == 'resize_concat'
    transformed_inputs = head._transform_inputs(inputs)
    assert transformed_inputs.shape == (1, 48, 45, 45)

    # test multi-loss, loss_decode is dict
    with pytest.raises(TypeError):
        # loss_decode must be a dict or sequence of dict.
        BaseDecodeHead(3, 16, num_classes=19, loss_decode=['CrossEntropyLoss'])

    inputs = torch.randn(2, 19, 8, 8).float()
    target = torch.ones(2, 1, 64, 64).long()
    head = BaseDecodeHead(
        3,
        16,
        num_classes=19,
        loss_decode=dict(
            type='CrossEntropyLoss', use_sigmoid=False, loss_weight=1.0))
    if torch.cuda.is_available():
        head, inputs = to_cuda(head, inputs)
        head, target = to_cuda(head, target)
    loss = head.losses(seg_logit=inputs, seg_label=target)
    assert 'loss_ce' in loss

    # test multi-loss, loss_decode is list of dict
    inputs = torch.randn(2, 19, 8, 8).float()
    target = torch.ones(2, 1, 64, 64).long()
    head = BaseDecodeHead(
        3,
        16,
        num_classes=19,
        loss_decode=[
            dict(type='CrossEntropyLoss', loss_name='loss_1'),
            dict(type='CrossEntropyLoss', loss_name='loss_2')
        ])
    if torch.cuda.is_available():
        head, inputs = to_cuda(head, inputs)
        head, target = to_cuda(head, target)
    loss = head.losses(seg_logit=inputs, seg_label=target)
    assert 'loss_1' in loss
    assert 'loss_2' in loss

    # 'loss_decode' must be a dict or sequence of dict
    with pytest.raises(TypeError):
        BaseDecodeHead(3, 16, num_classes=19, loss_decode=['CrossEntropyLoss'])
    with pytest.raises(TypeError):
        BaseDecodeHead(3, 16, num_classes=19, loss_decode=0)

    # test multi-loss, loss_decode is list of dict
    inputs = torch.randn(2, 19, 8, 8).float()
    target = torch.ones(2, 1, 64, 64).long()
    head = BaseDecodeHead(
        3,
        16,
        num_classes=19,
        loss_decode=(dict(type='CrossEntropyLoss', loss_name='loss_1'),
                     dict(type='CrossEntropyLoss', loss_name='loss_2'),
                     dict(type='CrossEntropyLoss', loss_name='loss_3')))
    if torch.cuda.is_available():
        head, inputs = to_cuda(head, inputs)
        head, target = to_cuda(head, target)
    loss = head.losses(seg_logit=inputs, seg_label=target)
    assert 'loss_1' in loss
    assert 'loss_2' in loss
    assert 'loss_3' in loss

    # test multi-loss, loss_decode is list of dict, names of them are identical
    inputs = torch.randn(2, 19, 8, 8).float()
    target = torch.ones(2, 1, 64, 64).long()
    head = BaseDecodeHead(
        3,
        16,
        num_classes=19,
        loss_decode=(dict(type='CrossEntropyLoss', loss_name='loss_ce'),
                     dict(type='CrossEntropyLoss', loss_name='loss_ce'),
                     dict(type='CrossEntropyLoss', loss_name='loss_ce')))
    if torch.cuda.is_available():
        head, inputs = to_cuda(head, inputs)
        head, target = to_cuda(head, target)
    loss_3 = head.losses(seg_logit=inputs, seg_label=target)

    head = BaseDecodeHead(
        3,
        16,
        num_classes=19,
        loss_decode=(dict(type='CrossEntropyLoss', loss_name='loss_ce')))
    if torch.cuda.is_available():
        head, inputs = to_cuda(head, inputs)
        head, target = to_cuda(head, target)
    loss = head.losses(seg_logit=inputs, seg_label=target)
    assert 'loss_ce' in loss
    assert 'loss_ce' in loss_3
    assert loss_3['loss_ce'] == 3 * loss['loss_ce']
