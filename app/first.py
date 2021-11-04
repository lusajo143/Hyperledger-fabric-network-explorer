# from hfc.fabric import Client
# import asyncio

# loop = asyncio.get_event_loop()
# cli = Client(net_profile="network.json")

# cli.setChannel(channel_name='secdoc')
# # print(cli.organizations)  # orgs in the network
# # print(cli.peers)  # peers in the network
# # print(cli.orderers)  # orderers in the network
# # print(cli.CAs) 


for x in range(5, 10):
    print(x)




# org1_admin = cli.get_user(org_name='org1.example.com', name='Admin')
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













# response = loop.run_until_complete(cli.query_info(
#                requestor=org1_admin,
#                channel_name="secdoc",
#                peers=['peer0.org1.example.com'],
#                decode=True
#                ))

# hash = response.currentBlockHash

# response = loop.run_until_complete(cli.query_block_by_hash(
#                requestor=org1_admin,
#                channel_name='secdoc',
#                peers=['peer0.org1.example.com'],
#                block_hash=hash,
#                decode=True
#                ))


# config_tx_file = './configtx.yaml'

# orderer_admin = cli.get_user(org_name='orderer.example.com', name='Admin')
# loop.run_until_complete(cli.channel_update(
#         orderer='orderer.example.com',
#         channel_name='secdoc',
#         requestor=orderer_admin,
#         config_tx=config_tx_file))

# file = open('block.json', 'w')
# file.write(str(response))
# file.close()

print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@\n')
print(response)


# from hfc.fabric_ca.caservice import ca_service

# casvc = ca_service(target="https://ca.org1.example.com:7054", ca_certs_path="cryptos/peerOrgs/org1/tls-ca/ca.pem")
# adminEnrollment = casvc.enroll("admin", "adminpw") # now local will have the admin enrollment
# secret = adminEnrollment.register("user22") # register a user to ca
# print('#######################################\n')
# print('secret: '+secret)
# user1Enrollment = casvc.enroll("user22", secret) # now local will have the user enrollment
# print('#######################################\n')
# print(user1Enrollment)
# user1ReEnrollment = casvc.reenroll(user1Enrollment) # now local will have the user reenrolled object
# RevokedCerts, CRL = adminEnrollment.revoke("user1")