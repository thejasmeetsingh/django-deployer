from enum import Enum


class Choices(Enum):
    @classmethod
    def get_values(cls):
        return tuple(x.value for x in cls)


class PlanType(Choices):
    B = ('B', 'Bronze')
    S = ('S', 'Silver')
    G = ('G', 'Gold')


class InstanceType(Choices):
    N = ('nano', 'Nano')
    M = ('micro', 'Micro')
    S = ('small', 'Small')
    MD = ('medium', 'Medium')
    L = ('large', 'Large')
    XL = ('xlarge', 'xLarge')
    DXL = ('2xlarge', '2xLarge')


class InstanceTier(Choices):
    T2 = ('t2', 't2')
    T3 = ('t3', 't3')
    T3A = ('t3a', 't3a')
    T4G = ('t4g', 't4g')
