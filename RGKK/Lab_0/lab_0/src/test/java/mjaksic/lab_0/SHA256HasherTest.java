package mjaksic.lab_0;

import static org.junit.jupiter.api.Assertions.assertEquals;

import org.junit.jupiter.api.Test;

class SHA256HasherTest {

	@Test
	void HashString() {
		SHA256Hasher hasher = SHA256Hasher.GetInstance();
		ByteArray input = new ByteArray("hello uničode");
		String exprected_result = "ae73f23421c315e4951b52a2541a6120d10e49f678c462609e64dc6dc14ce65d";
		assertEquals(exprected_result, hasher.Hash(input).hash_string);
	}
	
	@Test
	void HashInteger() {
		SHA256Hasher hasher = SHA256Hasher.GetInstance();
		ByteArray input = new ByteArray(12345);
		String exprected_result = "19581e27de7ced00ff1ce50b2047e7a567c76b1cbaebabe5ef03f7c3017bb5b7";
		assertEquals(exprected_result, hasher.Hash(input).hash_string);
	}
	
	@Test
	void HashFloat() {
		SHA256Hasher hasher = SHA256Hasher.GetInstance();
		ByteArray input = new ByteArray(1.2345);
		String exprected_result = "4bf5122f344554c53bde2ebb8cd2b7e3d1600ad631c385a5d7cce23c7785459a";
		assertEquals(exprected_result, hasher.Hash(input).hash_string);
	}
	
	@Test
	void HashDouble() {
		SHA256Hasher hasher = SHA256Hasher.GetInstance();
		ByteArray input = new ByteArray(0.0000000000001);
		String exprected_result = "6e340b9cffb37a989ca544e6bb780a2c78901d3fb33738768511a30617afa01d";
		assertEquals(exprected_result, hasher.Hash(input).hash_string);
	}
	
	@Test
	void HashComplexData() {
		SHA256Hasher hasher = SHA256Hasher.GetInstance();
		ByteArray double_input = new ByteArray(0.0000000000001);
		ByteArray string_input = new ByteArray("hello uničode");
		
		hasher.Update(double_input);
		hasher.Update(string_input);
		
		String exprected_result = "ed515633de529c7e2f127e44507c47b2453a9dec2d95d9539cfdb61fec8f05d3";
		assertEquals(exprected_result, hasher.Hash().hash_string);
	}
}