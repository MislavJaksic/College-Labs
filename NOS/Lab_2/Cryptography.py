from Crypto.Cipher import AES, DES
from Crypto import Random

crypto_safe_random = Random.new()

def DoEncryptionDecryption():
  message = ChooseMessage()
  construct = ChooseEncryptionConstruct()
  
  if construct == "envelope":
    sym_algo = ChooseSymmetricAlgorithm()
    asym_algo = ChooseAsymmetricAlgorithm()
    
    envelope = CreateEnvelope(sym_algo, asym_algo)
    
  elif construct == "signature":
    asym_algo = ChooseAsymmetricAlgorithm()
    digest = ChooseDigestAlgorithm()
    
  elif construct == "seal":
    sym_algo = ChooseSymmetricAlgorithm()
    asym_algo = ChooseAsymmetricAlgorithm()
    digest = ChooseDigestAlgorithm()
  
def ChooseMessage():
  message = raw_input("What message do you want to send? (any)")
  
  return message
  
def ChooseEncryptionConstruct():
  construct = raw_input("What do you want to create? (envelope, signature, seal)")
  construct = SanitiseInput(construct, ("envelope", "signature", "seal"))
  return construct
  
def ChooseSymmetricAlgorithm():
  algorithm = raw_input("Which symmetric algorithm do you wish to use? (AES, TripleDES)")
  algorithm = SanitiseInput(algorithm, ("AES", "TripleDES"))
  
  mode = ChooseEncryptionMode()
  
  key_size = ChooseSymmetricKeySize()
  
  return (algorithm, mode, key_size)

def ChooseAsymmetricAlgorithm():
  algorithm = raw_input("Which asymmetric algorithm do you wish to use? (RSA, ElGamal)")
  algorithm = SanitiseInput(algorithm, ("RSA", "ElGamal"))
  
  key_size = ChooseAsymmetricKeySize()
  
  return (algorithm, key_size)
  
def ChooseDigestAlgorithm():
  algorithm = raw_input("Which digest do you wish to use? (SHA-1, SHA-2-224, SHA-2-256, SHA-2-384, SHA-2-512)")
  algorithm = SanitiseInput(algorithm, ("SHA-1", "SHA-2-224", "SHA-2-256", "SHA-2-384", "SHA-2-512"))
  return algorithm
    
def ChooseSymmetricKeySize():
  key_size = raw_input("What will be the key length? (16, 24, 32)")
  key_size = SanitiseInput(int(key_size), (16, 24, 32))
  return key_size
  
def ChooseAsymmetricKeySize():
  key_size = raw_input("What will be the key length? (multiple of 256 greater then 1024)")
  key_size = SanitiseInput(int(key_size), (x for x in range(1024, int(key_size)+1, 256)))
  return key_size
  
def ChooseEncryptionMode():
  mode = raw_input("Which mode is it going to use? (ECB, CBC, CTR)")
  mode = SanitiseInput(mode, ("ECB", "CBC", "CTR"))
  return mode

def SanitiseInput(input, acceptable_inputs):
  if input in acceptable_inputs:
    return input
  else:
    raise Exception("Acceptable inputs are:" + str(acceptable_inputs))


def CreateDigitalEnvelope():
  ciphertext_message = EncryptMessage()
  ciphertext_symmetric_key = hi
  digital_envelope = ()

def CreateDigitalSignature():
  pass
def CreateDigitalSeal():
  pass


def EncryptMessage():
  pass
def EncryptSymmetricKey():
  pass
  
def EncryptDigest():
  pass
def CreateAESKey(key_size):
  key_size = ConformToAESKeySize(key_size)
  key = crypto_safe_random.read(key_size)
  
  return key
  
def ConformToAESKeySize(key_size):
  if key_size <= 16:
    key_size = 16
  elif (key_size > 16) and (key_size <= 24):
    key_size = 24
  else:
    key_size = 32
    
  return key_size
  
def AESEncryption(key, plaintext_message, encryption_mode):
  
  init_vector = crypto_safe_random.read(AES.block_size)

  cipher = AES.new(key, AES.MODE_ECB, init_vector) #AES.MODE_CTR, AES.MODE_CBC

  ciphertext_message = cipher.encrypt(plaintext_message)

  print ciphertext_message

  print cipher.decrypt(ciphertext_message)


def TripleDESEncryption():
  init_vector = crypto_safe_random.read(AES.block_size)

  cipher = DES.new(key, AES.MODE_ECB, init_vector) #AES.MODE_CTR, AES.MODE_CBC
  print cipher
  ciphertext_message = cipher.encrypt(plaintext_message)

  print ciphertext_message

  print cipher.decrypt(ciphertext_message)
  
DoEncryptionDecryption()
