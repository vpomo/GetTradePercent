import pytest
from brownie import config

@pytest.fixture
def busd_whale(accounts):
    yield accounts.at('0x58f876857a02d6762e0101bb5c46a8c1ed44dc16', force=True)

@pytest.fixture
def BUSD(interface):
    yield interface.ERC20('0xe9e7cea3dedca5984780bafc599bd69add087d56')

@pytest.fixture
def wbnb_whale(accounts):
    yield accounts.at('0x0ed7e52944161450477ee417de9cd3a859b14fd0', force=True)

@pytest.fixture
def WBNB(interface):
    yield interface.ERC20('0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c')

@pytest.fixture
def pancakeRouter(interface):
    yield interface.PancakeRouter('0x10ed43c718714eb63d5aa57b78b54704e256024e')

@pytest.fixture
def pancakeFactory(interface):
    yield interface.PancakeFactory('0xca143ce32fe78f1f7019d7d551a6402fc5350c73')


