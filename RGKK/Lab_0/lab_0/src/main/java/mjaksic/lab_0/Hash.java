package mjaksic.lab_0;

import java.math.BigInteger;

public class Hash {
	public byte[] hash_bytes;
	public String hash_string;
	
	public Hash(byte[] hash_bytes) {
		this.hash_bytes = hash_bytes;
		this.hash_string = ByteArrayToString();
	}
	
	private String ByteArrayToString() {
		BigInteger big_number = new BigInteger(1, this.hash_bytes);
		String hexa_string = big_number.toString(16);
		return hexa_string;
	}

}
