from Crypto.Cipher import AES, DES3
from Crypto import Random

crypto_safe_random = Random.new()

def DoEncryptionDecryption():
  message = ChooseMessage()
  construct = ChooseEncryptionConstruct()
  
  if construct == "envelope":
    sym_method = ChooseSymmetricMethod()
    asym_method = ChooseAsymmetricMethod()
    
    envelope = CreateDigitalEnvelope(message, sym_method, asym_method)
    
  elif construct == "signature":
    asym_method = ChooseAsymmetricMethod()
    digest = ChooseDigestAlgorithm()
    
  elif construct == "seal":
    sym_method = ChooseSymmetricMethod()
    asym_method = ChooseAsymmetricMethod()
    digest = ChooseDigestAlgorithm()
    
  elif construct == "demo":
    RunDemoOne(message)
    RunDemoTwo(message)
  
def RunDemoOne(message):
  sym_method = {}
  sym_method["algorithm"] = "AES"
  sym_method["mode"] = "CBC"
  sym_method["key_size"] = 32
  
  asym_method = ("RSA", 1024)
  envelope = CreateDigitalEnvelope(message, sym_method, asym_method)

def RunDemoTwo(message):
  sym_method = {}
  sym_method["algorithm"] = "3DES"
  sym_method["mode"] = "OFB"
  sym_method["key_size"] = 24
  
  asym_method = ("ElGamal", 1024 + 256)
  envelope = CreateDigitalEnvelope(message, sym_method, asym_method)
  
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
  
  sym_method = CreateAlgorithmDataStructure(algorithm, key_size, mode=mode)
  
  return sym_method

def ChooseAsymmetricMethod():
  algorithm = raw_input("Which asymmetric algorithm do you wish to use? (RSA, ElGamal)")
  algorithm = SanitiseInput(algorithm, ("RSA", "ElGamal"))
  
  key_size = ChooseAsymmetricKeySize()
  
  asym_method = CreateAlgorithmDataStructure(algorithm, key_size)
  
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

def CreateAlgorithmDataStructure(algorithm, key_size, mode="NONE"):
  method = {}
  method["algorithm"] = algorithm
  method["mode"] = mode
  method["key_size"] = key_size
  
  return algo

    
def CreateDigitalEnvelope(message, sym_method, asym_method):
  encrypter = CreateSymmetricCrypter(sym_method)
  padded_message = PadMessage(message, sym_method)
  
  ciphertext_message = encrypter["cipher"].encrypt(padded_message)
  print ciphertext_message
  
  decrypter = CreateSymmetricCrypter(sym_method, existing_cipher=encrypter)
  print decrypter["cipher"].decrypt(ciphertext_message)
  
  #key_pair = CreatePublicPrivateKeyPair(asym_method)
  #ciphertext_symmetric_key = EncryptSymmetricKey(symmetric_key, asym_method)
  
  #digital_envelope = ()

def CreateDigitalSignature():
  pass
  
def CreateDigitalSeal():
  pass
  
def EncryptMesage():
  pass
  
def EncryptSymmetricKey():
  pass
  
def EncryptDigest():
  pass
  
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

  
  
def AESEncryption():
  plaintext_message = "hello"
  plaintext_message = PadMessage("hello", ("AES", "CBC", 32))
  key = CreateSymmetricKey(32)
  encryption_mode = "OFB"
  init_vector = crypto_safe_random.read(AES.block_size)
  
  if encryption_mode == "ECB":
    cipher = AES.new(key, AES.MODE_ECB, init_vector)
  elif encryption_mode == "CBC":
    cipher = AES.new(key, AES.MODE_CBC, init_vector)
  elif encryption_mode == "OFB":
    cipher = AES.new(key, AES.MODE_OFB, init_vector)
  
  ciphertext_message = cipher.encrypt(plaintext_message)
  print ciphertext_message
  
  # WARNING: you can only encrypt/decrypt once with the same cipher
  if encryption_mode == "ECB":
    cipher = AES.new(key, AES.MODE_ECB, init_vector)
  elif encryption_mode == "CBC":
    cipher = AES.new(key, AES.MODE_CBC, init_vector)
  elif encryption_mode == "OFB":
    cipher = AES.new(key, AES.MODE_OFB, init_vector)
  
  print cipher.decrypt(ciphertext_message)
  
#AESEncryption()

DoEncryptionDecryption()





