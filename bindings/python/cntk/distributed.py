# Copyright (c) Microsoft. All rights reserved.
# Licensed under the MIT license. See LICENSE.md file in the project root
# for full license information.
# ==============================================================================

from . import cntk_py
from . import trainer
from .utils import typemap

__doc__= '''\
Distributed trainers manage trainers in distributed environment.
'''

class WorkerDescriptor(cntk_py.DistributedWorkerDescriptor):
    '''
    Distributed worker descriptor, returned by :class:`Communicator` instance.
    '''

    @property
    def global_rank(self):
        '''
        The global rank of the worker.
        '''
        return super(WorkerDescriptor, self).m_global_rank

    @property
    def host_id(self):
        '''
        The host id of the worker.
        '''
        return super(WorkerDescriptor, self).m_host_id

class Communicator(cntk_py.DistributedCommunicator):
    '''
    A communicator interface exposing communication primitives that serve as building blocks 
    for distributed training.
    '''

    @typemap
    def workers(self):
        '''
        Returns workers in this communicator.
        
        Returns:
            (`list`) of :class:`WorkerDescriptor`: workers in this communicator.
        '''
        return super(Communicator, self).workers()

    @typemap
    def current_worker(self):
        '''
        Returns worker descriptor of current process.
        
        Returns:
            :class:`WorkerDescriptor`: descriptor of current process.
        '''
        return super(Communicator, self).current_worker()

    def barrier(self):
        '''
        sync point to make sure all workers reach the same state
        '''
        super(Communicator, self).barrier()
        
    @staticmethod
    def finalize():
        cntk_py.DistributedCommunicator.finalize();

class QuantizedCommunicator(Communicator, cntk_py.QuantizedDistributedCommunicator):
    '''
    A communicator interface exposing communication primitives that serve as building blocks 
    for distributed training.
    '''

@typemap
def mpi_communicator():
    '''
    Creates a mpi communicator

    Returns:
        :class:`Communicator`: a distributed communicator
    '''
    return cntk_py.mpicommunicator()

@typemap
def quantized_mpi_communicator(num_quantization_bits):
    '''
    Creates a quantized mpi communicator

    Args:
        num_quantization_bits (`int`): num_quantization_bits

    Returns:
        :class:`QuantizedCommunicator`: a quantized distributed communicator
    '''
    return cntk_py.quantized_mpicommunicator(True, True, num_quantization_bits)

def data_parallel_distributed_trainer(communicator, use_async_buffered_parameter_update):
    '''
    Creates a data parallel distributed trainer using `communicator` with
    option `use_async_buffered_parameter_update`.

    Args:
        communicator: a communicator or a quantized communicator
        use_async_buffered_parameter_update (`bool`): use async buffered parameter update

    Returns:
        a distributed trainer instance
    '''
    if (isinstance(communicator, QuantizedCommunicator)):
        return cntk_py.create_quantized_data_parallel_distributed_trainer(communicator, use_async_buffered_parameter_update)
    else:
        return cntk_py.create_data_parallel_distributed_trainer(communicator, use_async_buffered_parameter_update)
