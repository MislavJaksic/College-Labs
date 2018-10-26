package mjaksic.lab_0;

import static org.junit.jupiter.api.Assertions.*;

import org.junit.jupiter.api.Test;

class HashTest {

	@Test
	void HashRandomBytes() {
		byte[] input = {0,1,2};
		Hash hash = new Hash(input);
		String exprected_result = "102";
		assertEquals(exprected_result, hash.hash_string);
	}

}
