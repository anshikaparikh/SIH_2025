import os
import json
from web3 import Web3
from web3.middleware import geth_poa_middleware

# expects environment variables: WEB3_PROVIDER, CONTRACT_ADDRESS, CONTRACT_ABI_PATH (optional)
WEB3_PROVIDER = os.getenv('WEB3_PROVIDER', 'http://127.0.0.1:8545')
CONTRACT_ADDRESS = os.getenv('CONTRACT_ADDRESS', None)
CONTRACT_ABI_PATH = os.getenv('CONTRACT_ABI_PATH', 'contracts/CertificateRegistry.abi.json')

def _load_abi(path):
    with open(path, 'r') as f:
        return json.load(f)

def get_contract():
    w3 = Web3(Web3.HTTPProvider(WEB3_PROVIDER))
    # If using a PoA chain like ganache or some testnets, add middleware
    try:
        w3.middleware_onion.inject(geth_poa_middleware, layer=0)
    except Exception:
        pass
    abi = _load_abi(CONTRACT_ABI_PATH)
    contract = w3.eth.contract(address=Web3.to_checksum_address(CONTRACT_ADDRESS), abi=abi)
    return w3, contract

def register_hash(cert_hash_hex: str, private_key: str) -> dict:
    w3, contract = get_contract()
    acct = w3.eth.account.from_key(private_key)
    nonce = w3.eth.get_transaction_count(acct.address)
    tx = contract.functions.registerCertificate(Web3.to_bytes(hexstr=cert_hash_hex)).build_transaction({
        'from': acct.address,
        'nonce': nonce,
        'gas': 300000,
        'gasPrice': w3.to_wei('20', 'gwei')
    })
    signed = acct.sign_transaction(tx)
    tx_hash = w3.eth.send_raw_transaction(signed.rawTransaction)
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    return {'tx_hash': tx_hash.hex(), 'receipt': dict(receipt)}

def is_registered(cert_hash_hex: str) -> bool:
    w3, contract = get_contract()
    return contract.functions.isRegistered(Web3.to_bytes(hexstr=cert_hash_hex)).call()
