package mjaksic.lab_0;

import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;


public class SHA256Hasher {
	public final static SHA256Hasher INSTANCE = new SHA256Hasher();
	
	private MessageDigest hash_function = null;

	public SHA256Hasher() {
		this.SetHashFunctionInstance();
	}

	private void SetHashFunctionInstance() {
		try {
			this.hash_function = MessageDigest.getInstance("SHA-256");
		} catch (NoSuchAlgorithmException e) {
			e.printStackTrace();
		}
	}
	
	public static SHA256Hasher GetInstance() {
		return INSTANCE;
	}
	
	
	
	public void Update(ByteArray data) {
		this.hash_function.update(data.byte_array);
	}

	public Hash Hash(ByteArray data) {
		byte[] bytes = ComputeHashAndReset(data);
		Hash hash = new Hash(bytes);
		return hash;
	}
	
	public Hash Hash() {
		byte[] bytes = ComputeHashAndReset();
		Hash hash = new Hash(bytes);
		return hash;
	}

	private byte[] ComputeHashAndReset(ByteArray data) {
		byte[] hash = this.hash_function.digest(data.byte_array);
		return hash;
	}
	
	private byte[] ComputeHashAndReset() {
		byte[] hash = this.hash_function.digest();
		return hash;
	}

}
