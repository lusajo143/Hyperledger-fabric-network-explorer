class Blocks:
    def __init__(self):
        print('Blocks')
    
    '''
    Structure data, blockNumber, current hash & prev hash
    '''
    def oneBlock(self, data):
        
        prev = str(data['header']['previous_hash'], 'utf-8')
        curr = str(data['header']['data_hash'], 'utf-8')

        resp = {
            'number': data['header']['number'],
            'previous_hash': prev,
            'data_hash': curr,
            'transactions': len(data['data']['data'])
        }

        return resp

    '''
    Block Details
    '''
    def detailsBlock(self, data):
        prev = str(data['header']['previous_hash'], 'utf-8')
        curr = str(data['header']['data_hash'], 'utf-8')

        f = open('ss.json','w')
        f.write(str(data))
        f.close()

        resp = {
            'number': data['header']['number'],
            'previous_hash': prev,
            'data_hash': curr,
        }

        return resp

    def transactions(self, data):
        data = data['data']['data']

        transactions = []

        for transaction in data:
            trans = {}
            print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')
            
            '''
            Header Section
            '''
            header = transaction['payload']['header']['channel_header'] 

            signature_header = transaction['payload']['header']['signature_header'] 
            nonce = str(signature_header['nonce'], 'utf-8') 

            '''
            Data section
            '''
            _dataSection = []  
            try:
                actions = transaction['payload']['data']['actions']

                # For each action
                for action in actions:
                    inputs = action['payload']['chaincode_proposal_payload']['input']

                    proposal = action['payload']['action']['proposal_response_payload']
                    
                    proposal_hash = str(proposal['proposal_hash'], 'utf-8') 

                    rwset = proposal['extension']['results']['ns_rwset']

                    _rwset = []                                                         
                    # for each namespace (channels)
                    for _set in rwset:
                        if _set['namespace'] != '_lifecycle':
                            _namespace = _set['namespace']

                            read_set = _set['rwset']['reads']
                            write_set = _set['rwset']['writes']
                            
                            _read_set = []                                                         ##########

                            # for each read
                            for read in read_set:
                                _read = {
                                    'key': read['key'],
                                    'from_block': read['version']['block_num']
                                } 
                                _read_set.append(_read)

                            _write_set = []

                            # for each write
                            for write in write_set:
                                if write['is_delete'] == True:
                                    is_delete = 'True'
                                else:
                                    is_delete = 'False'
                                _write = {
                                    'key': write['key'],
                                    'is_delete': is_delete,
                                    'value': str(write['value'], 'utf-8')
                                }
                                _write_set.append(_write)
                            
                            # _write_set = str(_write_set).replace('\'{','{').replace('}\'','}')

                            combo = {
                                'reads': _read_set,
                                'writes': _write_set
                            }
                            _rwset.append(combo)
                    
                    _dataSection.append({'rwset':_rwset})
                    response = proposal['extension']['response']

                    _response = {
                        'status': response['status'],
                        'payload': str(response['payload'], 'utf-8')
                    }
                    print()
                    _dataSection.append({'response':_response})                                                    ########

                    chaincode = proposal['extension']['chaincode_id']

                    _chaincode = {
                        'name': chaincode['name'],
                        'version': chaincode['version']
                    }
                    _dataSection.append({'chaincode':_chaincode})                                            ##########
            
            except:
                print()


            trans = {
                'version': header['version'],
                'timestamp': header['timestamp'],
                'channel_id': header['channel_id'],
                'tx_id': header['tx_id'],
                'creator': signature_header['creator']['mspid'],
                'tx_nonce': nonce,
                'data_section': _dataSection
            }

            

            #.replace('\'[','[').replace(']\'',']')
            transactions.append(trans)
            print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')
        # print(str(data).replace('\'','"'))
        return transactions#str(transactions).replace('\'','"')