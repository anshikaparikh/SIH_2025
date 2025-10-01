import json
from web3 import Web3

def validate_against_local_labels(cert_hash: str, labels_json_path: str) -> dict:
    try:
        with open(labels_json_path, 'r') as f:
            data = json.load(f)
        entry = data.get(cert_hash)
        if not entry:
            return {'found': False}
        return {'found': True, 'entry': entry}
    except FileNotFoundError:
        return {'found': False, 'error': 'labels file not found'}

def validate_against_blockchain(cert_hash: str, provider_uri: str, contract_address: str, abi: list) -> dict:
    w3 = Web3(Web3.HTTPProvider(provider_uri))
    contract = w3.eth.contract(address=Web3.to_checksum_address(contract_address), abi=abi)
    is_reg = contract.functions.isRegistered(Web3.to_bytes(hexstr=cert_hash)).call()
    owner = None
    if is_reg:
        owner = contract.functions.getOwner(Web3.to_bytes(hexstr=cert_hash)).call()
    return {'registered': is_reg, 'owner': owner}
