package mjaksic.distributed_system_node.serialisation;

import java.io.ByteArrayInputStream;
import java.io.ByteArrayOutputStream;
import java.io.IOException;
import java.io.ObjectInputStream;
import java.io.ObjectOutputStream;

public class ByteSerialiser {

	public static byte[] Serialise(Object object) {
		ByteArrayOutputStream byte_array_serialiser = ByteSerialiser.CreateByteArraySerialiser();
		ObjectOutputStream object_serialiser = ByteSerialiser.CreateSerialiser(byte_array_serialiser);
		
		try {
			object_serialiser.flush();
			object_serialiser.writeObject(object);
			object_serialiser.close();
		} catch (IOException e) {
			e.printStackTrace();
		}
		
		byte[] byte_array = byte_array_serialiser.toByteArray();
		return byte_array;
	}
	
	private static ByteArrayOutputStream CreateByteArraySerialiser() {
		ByteArrayOutputStream byte_array_serialiser = new ByteArrayOutputStream();
		
		return byte_array_serialiser;
	}
	
	private static ObjectOutputStream CreateSerialiser(ByteArrayOutputStream byte_array_serialiser) {
		ObjectOutputStream object_serialiser = null;
		try {
			object_serialiser = new ObjectOutputStream(byte_array_serialiser);
		} catch (IOException e) {
			e.printStackTrace();
		}
		
		return object_serialiser;
	}
	
	
	
	public static Object Deserialise(byte[] byte_array) {
		ByteArrayInputStream byte_array_deserialiser = ByteSerialiser.CreateByteArrayDeserialiser(byte_array);
		ObjectInputStream object_deserialiser = ByteSerialiser.CreateDeserialiser(byte_array_deserialiser);
		
		Object object = null;
		try {
			object = object_deserialiser.readObject();
			object_deserialiser.close();
		} catch (ClassNotFoundException e) {
			e.printStackTrace();
		} catch (IOException e) {
			e.printStackTrace();
		}
		
		return object;
	}
	
	private static ByteArrayInputStream CreateByteArrayDeserialiser(byte[] byte_array) {
		ByteArrayInputStream byte_array_deserialiser = new ByteArrayInputStream(byte_array);
		
		return byte_array_deserialiser;
	}
	
	private static ObjectInputStream CreateDeserialiser(ByteArrayInputStream byte_array_deserialiser) {
		ObjectInputStream object_deserialiser = null;
		try {
			object_deserialiser = new ObjectInputStream(byte_array_deserialiser);
		} catch (IOException e) {
			e.printStackTrace();
		}
		
		return object_deserialiser;
	}
	
}
