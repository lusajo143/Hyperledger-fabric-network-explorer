from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from django.contrib import messages


from .scripts import base
from .scripts.blocks import Blocks
import json


class Ops:

    def __init__(self):

        self.org = 'org1.example.com'
        self.orgNum = 1
        self.peer = 'peer0.org1.example.com'
        channels = base.getChannels(self.org, self.peer)

        # channels = str(channels).replace('channels ','')
        # channels = channels.replace('channel_id','"channel_id"')
        # channels = json.loads(channels)
        # self.channels = channels['channel_id']
        self.channels = channels
        self.channel = channels[0]['channel_id']

        self.ca_url = 'https://ca.org1.example.com:7054'
        self.causer = 'admin'
        self.capwd = 'adminpw'

        self.blockStructure = Blocks()

    '''
    Home section
    '''

    def home(self, request):

        infos = []
        for channel in self.channels:
            resp = base.getInfo(Channel_name=channel['channel_id'],
                                org=self.org, peer=self.peer)
            infos.append(
                {'name': channel['channel_id'], 'blocks': resp.height})

        parts = base.getParticipants(Channel_name=self.channel)
        # blocks = base.get4Blocks(Channel_name=self.channels, current=resp.height)

        # All users
        users = base.getAllUsers(
            self.org, self.ca_url, self.causer, self.capwd, self.orgNum)

        identities = users['result']['identities']

        idData = {}

        for identity in identities:
            try:
                idData[identity['type']] += 1
            except:
                idData[identity['type']] = 1

        keys = []
        for key in idData.keys():
            keys.append(key)

        values = []
        for value in idData.values():
            values.append(value)

        context = {
            "org": self.org,
            "users": len(identities),
            "userKeys": keys,
            "userValues": values,
            "currentHash": resp.currentBlockHash,
            "prevHash": resp.previousBlockHash,
            "orgs": len(parts["orgs"]),
            "peers": len(parts["peers"]),
            "orderers": len(parts["orderers"]),
            "channels": infos
        }
        return render(request, "dash/home.htm", context)

    '''
    Block section
    '''

    def blocks(self, request):

        if request.method == 'POST':
            channel = request.POST['channel']
            self.channel = channel

        info = base.getInfo(Channel_name=self.channel,
                            org=self.org, peer=self.peer)

        # channels = str(channels).replace('channels ','')
        # channels = channels.replace('channel_id','"channel_id"')
        # channels = json.loads(channels)

        # blocks = base.get4Blocks(Channel_name=channels['channel_id'], current=info.height)
        blocks = base.get4Blocks(
            Channel_name=self.channel, current=info.height, org=self.org, peer=self.peer)

        response = []
        latest = {}
        for block in blocks:
            response.append(self.blockStructure.oneBlock(block))
            latest = self.blockStructure.oneBlock(block)

        # Get latest block

        context = {"org": self.org, 'blocks': response, 'total': info.height,
                   'latest': latest, 'channels': self.channels, 'channel_selected': self.channel}

        return render(request, 'blocks/blocks.htm', context)

    '''
    Get side block data
    '''

    def getBlockRaw(self, request):
        if request.method == 'POST':
            block = base.getRaw(
                self.channel, request.POST['number'], self.org, self.peer)

            return HttpResponse(str(self.blockStructure.oneBlock(block)).replace('\'', '"'))
        else:
            return HttpResponse('Invalid request')

    '''
    Get Transactions from block number
    '''

    def getTransactions(self, request):
        if request.method == 'GET':
            # Fetch Block transactions

            number = request.GET.get('xaby')

            block = base.getRaw(self.channel, number, self.org, self.peer)

            transactions = self.blockStructure.transactions(block)

            # print(transactions)

            return render(request, 'blocks/transactions.htm', {"org": self.org, 'transactions': transactions, 'blockNo': number})
        else:
            return HttpResponse('Invalid request')

    '''
    Channels
    '''

    def chan(self, request):

        channels = base.getChannels(self.org, self.peer)

        chan = []

        for channel in channels:
            info = base.getInfo(
                Channel_name=channel['channel_id'], org=self.org, peer=self.peer)
            channel['blocks'] = info.height
            parts = base.getParticipants(Channel_name=channel['channel_id'])
            channel['orgs'] = base.getKeys(parts['orgs'])

            chan.append(channel)

        print()
        print(chan)
        print()

        context = {
            "org": self.org, 'channels': chan
        }

        return render(request, 'channels/channels.htm', context)

    def new_channel(self, request):
        if request.method == 'POST':
            print('@@@@@@@@@@@@@@@@@@@@@')
            try:
                File = request.FILES['config']

                ext = File.name.split('.')[-1]

                if ext == 'yaml' or ext == 'yml':
                    channel_name = request.POST['channel']
                    profile = request.POST['profile']
                    orderer = request.POST['orderer']
                    fs = FileSystemStorage()
                    fs.save('configtx.'+ext, File)
                    print()
                    print()
                    if base.createChannel(Org=self.org, channel_name=channel_name, orderer=orderer, profile=profile):
                        messages.success(
                            request, f'Channel is {channel_name} created successfully.')
                        return redirect('ops-channel')
                    else:
                        messages.warning(request, 'Channel creation failed')
                        return redirect('ops-channel')
                    print()
                    print()

                else:
                    messages.warning(request, 'Unsupported file')
                    return redirect('ops-channel')
            except Exception as e:
                print(e)
                messages.warning(request, 'Server error occured')
                return redirect('ops-channel')

    def join_channel(self, request):
        if request.method == 'POST':
            channel_name = request.POST['channel']
            orderer = request.POST['orderer']

            resp = base.joinChannel(Org=self.org, channel_name=channel_name, peers=['peer0.org1.example.com',
                                                                                    'peer1.org1.example.com'], orderer=orderer)

            if len(resp) == 2:
                messages.success(request, 'Joined channel successfully')
                return redirect('ops-channel')
            else:
                messages.warning(request, 'Failed to join channel')
                return redirect('ops-channel')

            return HttpResponse(resp)

        else:
            messages.warning(request, 'Failed to join channel')
            return redirect('ops-channel')
        return True

    '''
    Identities
    '''
    def identities(self, request):

        # All users
        users = base.getAllUsers(
            self.org, self.ca_url, self.causer, self.capwd, self.orgNum)
        
        return render(request, 'identities/identities.htm', { "orgs": self.org, "ids": users['result']['identities'] })

    '''
    Chaincode view
    '''
    def chaincode(self, request):
        return render(request, 'chaincode/chaincode.htm',{"org": self.org,})
