from hfc.fabric import Client
import asyncio

from hfc.fabric_ca.caservice import ca_service

'''
Get keys from dict
'''
def getKeys(dictionary):
    keys = []
    for key in dictionary.keys():
        keys.append(key)
    return keys



'''
Get participants i.e number
'''
def getParticipants(Channel_name):
    loop = asyncio.SelectorEventLoop()
    asyncio.set_event_loop(loop)

    cli = Client(net_profile="ops/scripts/network.json")
    cli.setChannel(Channel_name)
    return {'orgs':cli.organizations, 'peers': cli.peers, 'orderers':cli.orderers}


"""
Function to get number of blocks, current hash and prev hash
"""
def getInfo(Channel_name, org, peer):
    loop = asyncio.SelectorEventLoop()
    asyncio.set_event_loop(loop)

    cli = Client(net_profile="ops/scripts/network.json")

    cli.setChannel(channel_name=Channel_name)
    org1_admin = cli.get_user(org_name=org, name='Admin')

    response = loop.run_until_complete(cli.query_info(
               requestor=org1_admin,
               channel_name=Channel_name,
               peers=[peer],
               decode=True
               ))
    return response


'''
Query 4 Blocks
'''
def get4Blocks(Channel_name, current, org, peer):
    loop = asyncio.SelectorEventLoop()
    asyncio.set_event_loop(loop)

    cli = Client(net_profile="ops/scripts/network.json")

    cli.setChannel(channel_name=Channel_name)
    org1_admin = cli.get_user(org_name='org1.example.com', name='Admin')

    resp = []

    fromBlock = 0
    if current >= 4:
        fromBlock = current - 4
    else:
        fromBlock = 0 

    for num in range(fromBlock, current):
        response = loop.run_until_complete(cli.query_block(
                requestor=org1_admin,
                channel_name=Channel_name,
                peers=[peer],
                block_number=str(num),
                decode=True
                ))
        resp.append(response)
    
    return resp

'''
Query Raw data
'''
def getRaw(Channel_name, num, org, peer):
    loop = asyncio.SelectorEventLoop()
    asyncio.set_event_loop(loop)

    cli = Client(net_profile='ops/scripts/network.json')
    cli.setChannel(channel_name=Channel_name)
    org_admin = cli.get_user(org_name=org, name='Admin')
    # casvc = ca_service(target='https://ca.org1.example.com:7054', ca_certs_path='ops/cryptos/peerOrgs/org1/tls-ca/ca.pem')
    # org_admin = casvc.enroll("admin", "adminpw")

    print()
    print()
    
    print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
    print()
    print()
    
    response = loop.run_until_complete(cli.query_block(
        requestor=org_admin,
        channel_name=Channel_name,
        peers=[peer],
        block_number=str(num),
        decode=True
    ))
    # print(response)

    return response


'''
Query for all channels in org
'''
def getChannels(Org, peer):
    loop = asyncio.SelectorEventLoop()
    asyncio.set_event_loop(loop)

    cli = Client(net_profile="ops/scripts/network.json")

    org_admin = cli.get_user(org_name=Org, name='Admin')

    response = loop.run_until_complete(cli.query_channels(
               requestor=org_admin,
               peers=[peer],
               decode=True
               ))

    return response

'''
Create New Channel
'''
def createChannel(Org, channel_name, orderer, profile):
    loop = asyncio.SelectorEventLoop()
    asyncio.set_event_loop(loop)

    cli = Client(net_profile="ops/scripts/network.json")

    org_admin = cli.get_user(org_name=Org, name='Admin')

    response = loop.run_until_complete(cli.channel_create(
            orderer=orderer,
            channel_name=channel_name,
            requestor=org_admin,
            config_yaml='ops/config',
            channel_profile=profile
            ))

    return response

'''
Join channel
'''
def joinChannel(Org, channel_name, peers, orderer):
    loop = asyncio.SelectorEventLoop()
    asyncio.set_event_loop(loop)

    cli = Client(net_profile="ops/scripts/network.json")

    org_admin = cli.get_user(org_name=Org, name='Admin')
    cli.setChannel(channel_name)

    responses = loop.run_until_complete(cli.channel_join(
               requestor=org_admin,
               channel_name=channel_name,
               peers=peers,
               orderer=orderer
               ))

    return responses


'''
Get All Users
'''
def getAllUsers(Org, Url, user, pwd, orgNum):
    cas = ca_service(target=Url, ca_certs_path='ops/cryptos/peerOrgs/org'+str(orgNum)+'/tls-ca/ca.pem')

    identityService = cas.newIdentityService()

    return identityService.getAll(cas.enroll(user, pwd))

# class Operation:
#     def __init__(self, Channel_name, Org_name, User, peer):
#         self.channel_name = Channel_name
#         self.Org_name = Org_name
#         self.peer = peer
#         self.cli = Client(net_profile="ops/scripts/network.json")
#         self.cli.setChannel(channel_name=self.Channel_name)
#         self.User = self.cli.get_user(org_name=self.Org_name, name=User)

#     def getInfo(self):
#         loop = asyncio.SelectorEventLoop()
#         asyncio.set_event_loop(loop)

#         response = loop.run_until_complete(self.cli.query_info(
#             requestor=self.User,
#             channel_name=self.Channel_name,
#             peers=[self.peer],
#             decode=True
#         ))

#         loop.close()
#         return response















# # print(org1_admin)

# response = loop.run_until_complete(cli.query_installed_chaincodes(
#     requestor=org1_admin,
#     peers=['peer0.org1.example.com'],
#     decode=True
# ))

# response = loop.run_until_complete(cli.generate_channel_tx(
#                requestor=org1_admin,
#                channel_name='secdoc',
#                peers=['peer0.org1.example.com'],
#                decode=True
#                ))
# Create a New Channel, the response should be true if succeed


# response = loop.run_until_complete(cli.get_channel_config(
#                requestor=org1_admin,
#                channel_name='secdoc',
#                peers=['peer0.org1.example.com'],
#                decode=True
#                ))


