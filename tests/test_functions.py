from brownie import Wei, reverts
import brownie
from datetime import datetime
import time

def test_main(accounts, interface, pancakeRouter, WBNB):
    print('='*20 + ' running ... ' + '='*20)
    timestamp = int(time.time())
    timestampWork = timestamp + 60*60*100

    decimals = 1e18

    tokenAdrdess = ['0x530fea77c0857ea3d1354d3569d819438272426b', '0xcd929f47ce8eb0dc88d30abac83d002a4c000142',
                    '0x5f02c4dcb270999282b850caa47af749ce49fe00']

    tokenHolder = [accounts.at('0xad696683329fd826ab5a1bf9b6ef2e59893879b8', force=True),
                   accounts.at('0xda83445fff927c2bf134e42c4eab7d285f52ac82', force=True),
                   accounts.at('0x6fda0806618c3981a8a7b3075e2ee7887a648acf', force=True)
                   ]

    buyAmount = []
    sellAmount = []
    tokenSymbol = []

    length = len(tokenAdrdess)
    print('count tokens', length)
    print("\n" + 'starting process ...' + "\n")

    tokenOneAmount = 1000
    tokenTwoAmount = 100000000
    tokenAmount = 0

    weiAmount = Wei('30 ether')

    forApprove = 1000000000000000 * decimals

    for i in range(0, length):
        currentToken = interface.ERC20(tokenAdrdess[i])
        print('token name: ', currentToken.symbol())
        tokenSymbol.append(currentToken.symbol())
        print('token decimals: ', currentToken.decimals())
        currentDecimals = 10 ** currentToken.decimals()

        if currentToken.decimals() < 18:
            tokenAmount = tokenTwoAmount * currentDecimals
        else:
            tokenAmount = tokenOneAmount * currentDecimals

        currentToken.approve(pancakeRouter, forApprove, {'from': tokenHolder[i]})

        pathsToBNB = [tokenAdrdess[i], WBNB]
        pathsToToken = [WBNB, tokenAdrdess[i]]

        pathsToBNBAmount = pancakeRouter.getAmountsOut(tokenAmount, pathsToBNB)
        #print('Before purchase: ', pathsToBNBAmount[1]/decimals)
        beforeBalance = tokenHolder[i].balance()
        resultTokenToBNB = pancakeRouter.swapExactTokensForETHSupportingFeeOnTransferTokens(tokenAmount, 0, pathsToBNB, tokenHolder[i], timestampWork, {'from': tokenHolder[i]})
        afterBalance = tokenHolder[i].balance()

        sellPercent = 100 - 100*(afterBalance-beforeBalance)/pathsToBNBAmount[1]
        print('sellPercent % :', sellPercent)
        sellAmount.append(sellPercent)
        #print('(amount BNB for ' + str(tokenAmount/currentDecimals) + ' tokens ' + currentToken.symbol() + ') = ', (afterBalance-beforeBalance)/decimals)

        pathsToTokenAmount = pancakeRouter.getAmountsOut(weiAmount, pathsToToken)
        #print('Before purchase: ', pathsToTokenAmount[1]/currentDecimals)
        beforeTokenBalance = currentToken.balanceOf(accounts[i+1])
        resultBNBToToken = pancakeRouter.swapExactETHForTokens(0, pathsToToken, accounts[i+1], timestampWork, {'from': accounts[i+1], 'value': weiAmount})
        afterTokenBalance = currentToken.balanceOf(accounts[i+1])

        buyPercent = 100 - 100*(afterTokenBalance-beforeTokenBalance)/pathsToTokenAmount[1]
        print('buyPercent %:', buyPercent)
        buyAmount.append(buyPercent)
        #print('(amount token ' + currentToken.symbol() + ' for 30 BNB) = ', (afterTokenBalance-beforeTokenBalance)/currentDecimals)
        print("\n")

    print('end of process ...')

    saveToFile(tokenSymbol, buyAmount, sellAmount, length)

    print('='*20 + ' running ... ' + '='*20)


def saveToFile(tokenSymbol, buyAmount, sellAmount, length):
    now = datetime.now()
    fileName = './files/' + now.strftime("%d-%m-%Y-%H_%M_%S") + '.csv'
    file = open(fileName,"w")

    for i in range(0, length):
        file.writelines(tokenSymbol[i] + ', ' + str(sellAmount[i]) + ', ' + str(buyAmount[i]) + "\n")
    file.close()


