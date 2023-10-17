# from secrets import token_bytes
# from coincurve import PublicKey
# # from sha3 import keccak_256
# import hashlib
# from Crypto.Hash import keccak


from web3.auto import w3

def getNewKey():
    acct = w3.eth.account.create('KEYSMASH FJAFJKLDSKF7JKFDJ 1530')
    print(acct.address)

    print(acct._private_key.hex())
    return (acct._private_key.hex(), acct.address)


# 'b25c7db31feed9122727bf0939dc769a96564b2de4c4726d035b36ecf1e5b364'
# 0xb36d18D463cF028D50b47Ee2A379758d3820e2b7
#
# k = keccak.new(digest_bits=256)
# private_key = k.digest()
# print(private_key)
# # hashlib.(token_bytes(32)).digest()
# 0x9cce34F7aB185c7ABA1b7C8140d620B4BDA941d6
# 0xdcc703c0e500b653ca82273b7bfad8045d85a470
#
# public_key = PublicKey.from_valid_secret(private_key).format(compressed=False)[1:]
# print(public_key)
#
# addr = k.digest()[-20:]
#
# print('private_key:', private_key.hex())
# print('eth addr: 0x' + addr.hex())