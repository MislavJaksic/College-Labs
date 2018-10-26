package mjaksic.lab_0;

public class ByteArray {
	public byte[] byte_array;

	public ByteArray(String string) {
		this.byte_array = string.getBytes();
	}

	public ByteArray(Integer integer) {
		this.byte_array = new byte[] { integer.byteValue() };
	}

	public ByteArray(Float floating) {
		this.byte_array = new byte[] { floating.byteValue() };
	}

	public ByteArray(Double double_floating) {
		this.byte_array = new byte[] { double_floating.byteValue() };
	}
}
