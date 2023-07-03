# All commands with pybitcointools
# https://github.com/primal100/pybitcointools.git

>>> target = '32GkPB9XjMAELR4Q2Hr31Jdz2tntY18zCe'
>>> unspent(target)
[{'output': '8602122a7044b8795b5829b6b48fb1960a124f42ab1c003e769bbaad31cb2afd:0', 'value': 677200}, {'output': 'bd992789fd8cff1a2e515ce2c3473f510df933e1f44b3da6a8737630b82d0786:0', 'value': 5000000}]
# Get the outputs of each transaction
>>> deserialize(fetchtx('8602122a7044b8795b5829b6b48fb1960a124f42ab1c003e769bbaad31cb2afd'))['outs'][0]
{'value': 677200, 'script': 'a91406612b7cb2027e80ec340f9e02ffe4a9a59ba76287'}
>>> deserialize(fetchtx('bd992789fd8cff1a2e515ce2c3473f510df933e1f44b3da6a8737630b82d0786'))['outs'][0]
{'value': 5000000, 'script': 'a91406612b7cb2027e80ec340f9e02ffe4a9a59ba76287'}
# Get an existing scriptSig
>>> deserialize(fetchtx('6102bfd4bad33443bcb99765c0751b6b8e4e65f4db4e3b65324c5e9e3dac8132'))['ins'][0]
{'script': '00483045022100e5d7c59ea1fb5d0285e755dfc09634e1e3af36d12950b9b5d5f92b136021b3d202202c181129443b08dcfb8d9ced30187186c57c96f9cdb3f3914e0798682ea35d2b03493046022100e1f8dbad16926cfa3bf61b66e23b3846323dcabf6c75748bcfad762fc50bfaf402210081d955160b5f8d2b9d09d8838a2cf61f5055009d9031e0e106e19ebab234d949034c695221023927b5cd7facefa7b85d02f73d1e1632b3aaf8dd15d4f9f359e37e39f05611962103d2c0e82979b8aba4591fe39cffbf255b3b9c67b3d24f94de79c5013420c67b802103ec010970aae2e3d75eef0b44eaa31d7a0d13392513cd0614ff1c136b3b1020df53ae', 'outpoint': {'index': 1, 'hash': 'ec2a40cac3ac5dadf1d31f3cad03bdc8465caab5acbc5407ee7f4a7400aab577'}, 'sequence': 4294967295}
# Confirm that the corresponding output script matches the one discovered above
>>> deserialize(fetchtx('ec2a40cac3ac5dadf1d31f3cad03bdc8465caab5acbc5407ee7f4a7400aab577'))['outs'][1]
{'value': 350000, 'script': 'a91406612b7cb2027e80ec340f9e02ffe4a9a59ba76287'}
>>> import hashlib
>>> data = "5221023927b5cd7facefa7b85d02f73d1e1632b3aaf8dd15d4f9f359e37e39f05611962103d2c0e82979b8aba4591fe39cffbf255b3b9c67b3d24f94de79c5013420c67b802103ec010970aae2e3d75eef0b44eaa31d7a0d13392513cd0614ff1c136b3b1020df53ae".decode("hex")
>>> data = hashlib.sha256(data).digest()
>>> hashlib.new('ripemd160', data).hexdigest()
'06612b7cb2027e80ec340f9e02ffe4a9a59ba762'
>>> pubs = ['023927b5cd7facefa7b85d02f73d1e1632b3aaf8dd15d4f9f359e37e39f0561196', '03d2c0e82979b8aba4591fe39cffbf255b3b9c67b3d24f94de79c5013420c67b80', '03ec010970aae2e3d75eef0b44eaa31d7a0d13392513cd0614ff1c136b3b1020df']
>>> sigs = [der_decode_sig('3045022100dfcfafcea73d83e1c54d444a19fb30d17317f922c19e2ff92dcda65ad09cba24022001e7a805c5672c49b222c5f2f1e67bb01f87215fb69df184e7c16f66c1f87c2903'), der_decode_sig('304402204a657ab8358a2edb8fd5ed8a45f846989a43655d2e8f80566b385b8f5a70dab402207362f870ce40f942437d43b6b99343419b14fb18fa69bee801d696a39b3410b803')]
>>> hash = '\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
>>> ecdsa_raw_verify(hash, sigs[0], pubs[0])
True
>>> ecdsa_raw_verify(hash, sigs[1], pubs[1])
True
# My address
>>> addr
'1Lyafe8mSqubnynbAWPcXbHE5pnHMzEnT3'
# Unspent transaction outputs (legitimately) under my control
>>> unspent(addr)
[{'output': '23e81960ba8bb95c33c2336c84c126e378e4d1123921f881da9247c25f524161:1', 'value': 300000}]
# Target address and unspent transaction outputs
>>> target = '32GkPB9XjMAELR4Q2Hr31Jdz2tntY18zCe'
>>> unspent(target)
[{'output': '8602122a7044b8795b5829b6b48fb1960a124f42ab1c003e769bbaad31cb2afd:0', 'value': 677200}, {'output': 'bd992789fd8cff1a2e515ce2c3473f510df933e1f44b3da6a8737630b82d0786:0', 'value': 5000000}]
# The unspent outputs are the inputs to the new transaction
>>> ins = unspent(addr) + unspent(target)
# Amount to send in the transaction
# Sum of the three inputs minus a fee for the block miner
>>> amount = 300000 + 5000000 + 677200
>>> amount -= 10000
# Single output to my address
>>> outs = [{'address': addr, 'value': value}]
# Create a new transaction from these inputs and outputs
>>> tx = mktx(ins, outs)
# Sign the first input with my private key
>>> tx = sign(tx, 0, priv)
>>> tx = deserialize(tx)
# Add the scriptSigs containing SIGHASH_SINGLE signatures of 1
>>> tx['ins'][1]['script'] = '00483045022100dfcfafcea73d83e1c54d444a19fb30d17317f922c19e2ff92dcda65ad09cba24022001e7a805c5672c49b222c5f2f1e67bb01f87215fb69df184e7c16f66c1f87c290347304402204a657ab8358a2edb8fd5ed8a45f846989a43655d2e8f80566b385b8f5a70dab402207362f870ce40f942437d43b6b99343419b14fb18fa69bee801d696a39b3410b8034c695221023927b5cd7facefa7b85d02f73d1e1632b3aaf8dd15d4f9f359e37e39f05611962103d2c0e82979b8aba4591fe39cffbf255b3b9c67b3d24f94de79c5013420c67b802103ec010970aae2e3d75eef0b44eaa31d7a0d13392513cd0614ff1c136b3b1020df53ae'
>>> tx['ins'][2]['script'] = '00483045022100dfcfafcea73d83e1c54d444a19fb30d17317f922c19e2ff92dcda65ad09cba24022001e7a805c5672c49b222c5f2f1e67bb01f87215fb69df184e7c16f66c1f87c290347304402204a657ab8358a2edb8fd5ed8a45f846989a43655d2e8f80566b385b8f5a70dab402207362f870ce40f942437d43b6b99343419b14fb18fa69bee801d696a39b3410b8034c695221023927b5cd7facefa7b85d02f73d1e1632b3aaf8dd15d4f9f359e37e39f05611962103d2c0e82979b8aba4591fe39cffbf255b3b9c67b3d24f94de79c5013420c67b802103ec010970aae2e3d75eef0b44eaa31d7a0d13392513cd0614ff1c136b3b1020df53ae'
>>> serialize(tx)
'01000000036141525fc24792da81f8213912d1e478e326c18...'
