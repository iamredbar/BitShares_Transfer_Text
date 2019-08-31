from pprint import pprint
from bitshares.account import Account
from bitshares.blockchain import Blockchain
from bitshares.asset import Asset
from bitshares import BitShares
from twilio.rest import Client

# User Inputs
ACCOUNT_WATCHING = ''
BOT_PHONE_NUMBER = ''
YOUR_PHONE_NUMBER = ''

account_sid = ''
auth_token = ''
client = Client(account_sid, auth_token)

bitshares = BitShares(
                        node=[
                            "wss://na.openledger.info/ws",
                            "wss://kc-us-dex.xeldal.com/ws"
                        ]
            )

blockchain = Blockchain(
                        blockchain_instance=bitshares,
                        mode='head'
)

for op in blockchain.stream(['transfer']):
    payee = Account(op['to']).name
    if payee == ACCOUNT_WATCHING:
        from_account = Account(op['from']).name
        asset_symbol = Asset(op['amount']['asset_id']).symbol
        asset_precision = int(Asset(op['amount']['asset_id']).precision)
        amount = int(op['amount']['amount']) / (10**asset_precision)
        Asset.clear_cache()
        body = '{} sent {} {} {} in block {}.'.format(
                                                    from_account,
                                                    payee,
                                                    amount,
                                                    asset_symbol,
                                                    op['block_num']
                                                    )
        message = client.messages.create(
                                        body=body,
                                        from_=BOT_PHONE_NUMBER,
                                        to=YOUR_PHONE_NUMBER
                                        )
        pprint(message.sid)   
    Account.clear_cache()
