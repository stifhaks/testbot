import json

from web3 import Web3, HTTPProvider
# from web3 import

import config
from crypto import promoRaffleABI
from database.db_keys import user_table, k_addres
from routs.routs_key import db_helper

f_private_key = "0x97073fa8005435c6fb0b27738519c0934ebbd8915b4b0afed30fdcaaf3cfb383"
f_adress = "0xb36d18D463cF028D50b47Ee2A379758d3820e2b7"

# connection = Web3(HTTPProvider(f'https://mainnet.infura.io/v3/{config.REACT_APP_INFURA_ID}'))
# print ("Latest Ethereum block number", connection.eth.block_number)
# f_adres = config.PromoRaffle
# f_Abi = json.loads(promoRaffleABI.ABI)
# f_contract = connection.eth.contract(address=f_adres, abi= f_Abi)
# f_tx = f_contract.functions.enterRaffle().call()
# f_latest = f_contract.functions.getLatestTimestamp().transact()
# print(f_contract.functions)

polygon_net = 'https://polygon.llamarpc.com'
poligon_id = '137'
test_adress = '0x4E23c2451b639Cc6e27C22EEC1700dc56c06bf37'
priv_key = 'ea16d4f63750ff54534a2ee74a583065369437151d79850c89504aa19560ba66'

test_my_adress = '0x75dE145da9A60764B67D88646b3f8008CA6789eF'

from web3 import Web3

binance_testnet_rpc_url = polygon_net
web3 = Web3(Web3.HTTPProvider(binance_testnet_rpc_url))
print(f"Is connected: {web3.is_connected()}")  # Is connected: True
# С подключением вас 🥳


print(f"gas price: {web3.eth.gas_price} BNB")  # кол-во Wei за единицу газа
print(f"current block number: {web3.eth.block_number}")
print(f"number of current chain is {web3.eth.chain_id}")  # 97

balance = web3.eth.get_balance(test_adress)
print(f"balance of {test_adress}={balance}")
# InvalidAddress: Web3.py only accepts checksum addresses

matic_balance = Web3.from_wei(balance, 'ether')
print(f'matic balance {matic_balance}')


def build_txn(
        *,
        web3: Web3,
        from_address: str,  # checksum адрес
        to_address: str,  # checksum адрес
        amount: float,  # например, 0.1 BNB
) -> dict[str, int | str]:
    # цена газа
    gas_price = web3.eth.gas_price

    # количество газа
    gas = 22_000  # ставим побольше
    total_gas = gas_price*gas
    print(f'total gas {total_gas}')
    print(f'gas in matic {Web3.from_wei(total_gas, "ether")}')
    # 0.00210144
    # 0.00196253952594
    # MATIC

    # число подтвержденных транзакций отправителя
    nonce = web3.eth.get_transaction_count(from_address)

    txn = {
        'chainId': web3.eth.chain_id,
        'from': from_address,
        'to': to_address,
        'value': int(Web3.to_wei(amount, 'ether')),
        'nonce': nonce,
        'gasPrice': gas_price,
        'gas': gas,
    }
    return txn

def send_matic(amount,user_id):
    print(f'sending {amount} MATIC to {user_id}')
    f_user_adress = db_helper.get_cell(user_table, k_addres, user_id)
    f_user_adress = '0x'+f_user_adress
    transaction = build_txn(
        web3=web3,
        from_address=config.admin_matic_adress,
        to_address=f_user_adress,
        amount=amount,
    )

    print(transaction)
    try:
        # 2. Подписываем транзакцию с приватным ключом
        signed_txn = web3.eth.account.sign_transaction(transaction, config.admin_matic_key)
        #
        # # 3. Отправка транзакции
        txn_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
        #
        # # Получаем хэш транзакции
        # # Можно посмотреть статус тут https://testnet.bscscan.com/
        print(txn_hash.hex())
    except Exception as e:
        print(e)
        return False
    return True
