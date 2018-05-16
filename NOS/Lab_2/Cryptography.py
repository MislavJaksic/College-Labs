from Crypto.Cipher import AES, DES3
from Crypto.PublicKey import RSA, ElGamal
from Crypto.Hash import SHA, SHA224, SHA256, SHA384, SHA512
from Crypto import Random

crypto_safe_random = Random.new()

def DoEncryptionDecryption():
  message = ChooseMessage()
  construct = ChooseEncryptionConstruct()
  print ""
  
  if construct == "envelope":
    sym_method = ChooseSymmetricMethod()
    asym_method = ChooseAsymmetricMethod()
    padded_message = PadMessage(message, sym_method)
    
    envelope = CreateDigitalEnvelope(padded_message, sym_method, asym_method)
    
  elif construct == "signature":
    asym_method = ChooseAsymmetricMethod()
    digest_method = ChooseDigestAlgorithm()
    
    signature = CreateDigitalSignature(message, asym_method, digest_method)
    
  elif construct == "seal":
    sym_method = ChooseSymmetricMethod()
    asym_method = ChooseAsymmetricMethod()
    digest_method = ChooseDigestAlgorithm()
    padded_message = PadMessage(message, sym_method)
    
    seal = CreateDigitalSeal(message, sym_method, asym_method, digest_method)
    
  elif construct == "demo":
    RunDemoOne(message)
    RunDemoTwo(message)
    
    RunDemoThree(message)
    RunDemoFour(message)
    
    RunDemoFive(message)
    RunDemoSix(message)
  
def RunDemoOne(message):
  sym_method = CreateMethodDataStructure("AES", 32, mode="CBC")
  asym_method = CreateMethodDataStructure("RSA", 1024)
  
  padded_message = PadMessage(message, sym_method)
  envelope = CreateDigitalEnvelope(padded_message, sym_method, asym_method)

def RunDemoTwo(message):
  sym_method = CreateMethodDataStructure("3DES", 24, mode="OFB")
  asym_method = CreateMethodDataStructure("RSA", 1024 + 256)
  
  padded_message = PadMessage(message, sym_method)
  envelope = CreateDigitalEnvelope(padded_message, sym_method, asym_method)
  
def RunDemoThree(message):
  asym_method = CreateMethodDataStructure("RSA", 1024)
  digest_method = "SHA-1"
  
  signature = CreateDigitalSignature(message, asym_method, digest_method)
  
def RunDemoFour(message):
  asym_method = CreateMethodDataStructure("RSA", 1024)
  digest_method = "SHA-2-384"
  
  signature = CreateDigitalSignature(message, asym_method, digest_method)
  
def RunDemoFive(message):
  sym_method = CreateMethodDataStructure("AES", 32, mode="CBC")
  asym_method = CreateMethodDataStructure("RSA", 1024)
  digest_method = "SHA-1"
  
  padded_message = PadMessage(message, sym_method)
  seal = CreateDigitalSeal(padded_message, sym_method, asym_method, digest_method)
  
def RunDemoSix(message):
  sym_method = CreateMethodDataStructure("AES", 32, mode="OFB")
  asym_method = CreateMethodDataStructure("RSA", 1024)
  digest_method = "SHA-2-384"
  
  padded_message = PadMessage(message, sym_method)
  seal = CreateDigitalSeal(padded_message, sym_method, asym_method, digest_method)
  
  
  
def ChooseMessage():
  message = raw_input("What message do you want to send? (any)")
  return message
  
def ChooseEncryptionConstruct():
  construct = raw_input("What do you want to create? (envelope, signature, seal, demo)")
  construct = SanitiseInput(construct, ("envelope", "signature", "seal", "demo"))
  return construct
  
def ChooseSymmetricMethod():
  algorithm = raw_input("Which symmetric algorithm do you wish to use? (AES, 3DES)")
  algorithm = SanitiseInput(algorithm, ("AES", "3DES"))
  
  key_size = ChooseSymmetricKeySize()
  mode = ChooseEncryptionMode(algorithm)
  
  sym_method = CreateMethodDataStructure(algorithm, key_size, mode=mode)
  
  return sym_method

def ChooseAsymmetricMethod():
  algorithm = raw_input("Which asymmetric algorithm do you wish to use? (RSA, ElGamal)")
  algorithm = SanitiseInput(algorithm, ("RSA", "ElGamal"))
  
  key_size = ChooseAsymmetricKeySize()
  
  asym_method = CreateMethodDataStructure(algorithm, key_size)
  
  return asym_method
  
def ChooseDigestAlgorithm():
  algorithm = raw_input("Which digest do you wish to use? (SHA-1, SHA-2-224, SHA-2-256, SHA-2-384, SHA-2-512)")
  algorithm = SanitiseInput(algorithm, ("SHA-1", "SHA-2-224", "SHA-2-256", "SHA-2-384", "SHA-2-512"))
  return algorithm
    
def ChooseSymmetricKeySize(algorithm):
  if algorithm == "AES":
    key_size = raw_input("What will be the key length? (16, 24, 32)")
    key_size = SanitiseInput(int(key_size), (16, 24, 32))
  elif algorithm == "3DES":
    key_size = raw_input("What will be the key length? (16, 24)")
    key_size = SanitiseInput(int(key_size), (16, 24))
    
  return key_size
  
def ChooseAsymmetricKeySize():
  key_size = raw_input("What will be the key length? (multiple of 256 greater then 1024)")
  key_size = SanitiseInput(int(key_size), (x for x in range(1024, int(key_size)+1, 256)))
  return key_size
  
def ChooseEncryptionMode():
  mode = raw_input("Which mode is it going to use? (ECB, CBC, OFB)")
  mode = SanitiseInput(mode, ("ECB", "CBC", "OFB"))
  return mode

def SanitiseInput(input, acceptable_inputs):
  if input in acceptable_inputs:
    return input
  else:
    raise Exception("Acceptable inputs are:" + str(acceptable_inputs))

def CreateMethodDataStructure(algorithm, key_size, mode="NONE"):
  method = {}
  method["algorithm"] = algorithm
  method["mode"] = mode
  method["key_size"] = key_size
  
  return method

def PadMessage(message, sym_method):
  algorithm = sym_method["algorithm"]
  
  current_message_length = len(message)
  padded_message = message
  
  if algorithm == "AES":
    padding_length = (16 - current_message_length % 16)
    for i in range(padding_length):
      padded_message += "0"
      
  elif algorithm == "3DES":
    padding_length = (8 - current_message_length % 8)
    for i in range(padding_length):
      padded_message += "0"
  
  return padded_message
  
  
    
def CreateDigitalEnvelope(message, sym_method, asym_method):
  print "Digital Envelope: "
  
  ciphertext_message, symmetric_key = EncryptMesage(message, sym_method)
  
  ciphertext_symmetric_key = EncryptSymmetricKey(symmetric_key, asym_method)
  
  digital_envelope = (ciphertext_message, ciphertext_symmetric_key)
  return digital_envelope

def CreateDigitalSignature(message, asym_method, digest_method):
  print "Digital Signiture: "
  
  ciphertext_digest = SignMessageDigest(message, asym_method, digest_method)
  
  digital_signature = (message, ciphertext_digest)
  return digital_signature
  
def CreateDigitalSeal(message, sym_method, asym_method, digest_method):
  print "Digital Seal: "
  
  envelope = CreateDigitalEnvelope(message, sym_method, asym_method)
  
  seal = CreateDigitalSignature(envelope, asym_method, digest_method)
  return seal
  
def EncryptMesage(message, sym_method):
  print "Message to encrypt: " + message
  encrypter = CreateSymmetricCrypter(sym_method)
  
  ciphertext_message = encrypter["cipher"].encrypt(message)
  print "Encrypted message: " + ciphertext_message
  
  decrypter = CreateSymmetricCrypter(sym_method, existing_cipher=encrypter)
  print "Decrypted message: " + decrypter["cipher"].decrypt(ciphertext_message)
  
  print ""
  return ciphertext_message, encrypter["key"]
  
def EncryptSymmetricKey(symmetric_key, asym_method):
  print "Key to encrypt: ",
  print symmetric_key
  encrypter = CreateAsymmetricCrypter(asym_method)
  
  any_old_bits = 1234
  ciphertext_symmetric_key = encrypter["cipher"].encrypt(symmetric_key, any_old_bits)
  print "Encrypted key: ",
  print ciphertext_symmetric_key
  
  print "Decrypted key: ",
  print encrypter["cipher"].decrypt(ciphertext_symmetric_key)
  
  print ""
  return ciphertext_symmetric_key
  
def SignMessageDigest(message, asym_method, digest_method):
  digest = CreateMessageDigest(message, digest_method)
  
  crypter = CreateAsymmetricCrypter(asym_method)
  signer = crypter["cipher"]
  
  signed_digest = signer.decrypt(digest) #signing
  
  print "Signed digest: " + signed_digest
  any_old_bits = 1234
  unsigned_digest = signer.encrypt(signed_digest, any_old_bits)
  print "'Unsigned' digest: " + str(unsigned_digest)
  print ""
  
  return signed_digest
  
  
  
def CreateSymmetricCrypter(sym_method, existing_cipher=False):
  algorithm = sym_method["algorithm"]
  encryption_mode = sym_method["mode"]
  
  if existing_cipher == False:
    key, init_vector = GenerateKeyAndInitialVector(sym_method)
  else:
    key = existing_cipher["key"]
    init_vector = existing_cipher["init_vector"]
  
  if algorithm == "AES":
    cipher = CreateAESCipher(key, encryption_mode, init_vector)
  elif algorithm == "3DES":
    cipher = Create3DESCipher(key, encryption_mode, init_vector)
    
  crypter = CreateCrypterDataStructure(cipher, key, init_vector)
  
  return crypter
  
def GenerateKeyAndInitialVector(sym_method):
  key_size = sym_method["key_size"]
  key = CreateSymmetricKey(key_size)
  vector_size = ChooseVectorSize(sym_method)
  init_vector = CreateInitialVector(vector_size)
  
  return (key, init_vector)
  
def CreateSymmetricKey(key_size):
  key = crypto_safe_random.read(key_size)
  
  return key
  
def CreateInitialVector(vector_size):
  vector = CreateSymmetricKey(vector_size)
  
  return vector
  
def ChooseVectorSize(sym_method):
  algorithm = sym_method["algorithm"]
  
  if algorithm == "AES":
    size = AES.block_size
  elif algorithm == "3DES":
    size = DES3.block_size
    
  return size
  
def CreateAESCipher(key, encryption_mode, init_vector):
  if encryption_mode == "ECB":
    cipher = AES.new(key, AES.MODE_ECB, init_vector)
  elif encryption_mode == "CBC":
    cipher = AES.new(key, AES.MODE_CBC, init_vector)
  elif encryption_mode == "OFB":
    cipher = AES.new(key, AES.MODE_OFB, init_vector)
    
  return cipher
  
def Create3DESCipher(key, encryption_mode, init_vector):
  if encryption_mode == "ECB":
    cipher = DES3.new(key, DES3.MODE_ECB, init_vector)
  elif encryption_mode == "CBC":
    cipher = DES3.new(key, DES3.MODE_CBC, init_vector)
  elif encryption_mode == "OFB":
    cipher = DES3.new(key, DES3.MODE_OFB, init_vector)
    
  return cipher
  
def CreateCrypterDataStructure(cipher, key, init_vector):
  crypter = {}
  crypter["cipher"] = cipher
  crypter["key"] = key
  crypter["init_vector"] = init_vector
  
  return crypter

  
  
def CreateAsymmetricCrypter(asym_method):
  algorithm = asym_method["algorithm"]
  key_size = asym_method["key_size"]
  
  if algorithm == "RSA":
    cipher = CreateRSACipher(key_size)
  elif algorithm == "ElGamal":
    cipher = CreateElGamalCipher(key_size)
  
  crypter = {}
  crypter["cipher"] = cipher
  
  return crypter
  
def CreateRSACipher(key_size):
  key = RSA.generate(key_size)
  return key

def CreateElGamalCipher(key_size):
  key = ElGamal.generate(key_size, crypto_safe_random.read) #generaing a key takes a huge ammount of time
  return key
  
  
  
def CreateMessageDigest(message, digest_method):
  if digest_method == "SHA-1":
    digest = SHA.new()
  elif digest_method == "SHA-2-224":
    digest = SHA224.new()
  elif digest_method == "SHA-2-256":
    digest = SHA256.new()
  elif digest_method == "SHA-2-384":
    digest = SHA384.new()
  elif digest_method == "SHA-2-512":
    digest = SHA512.new()
  
  message = str(message)
  
  print "Message to digest: " + message
  digest.update(message)
  print "Digested message: " + digest.hexdigest()
  
  print ""
  return digest.hexdigest()
  
  

DoEncryptionDecryption()





