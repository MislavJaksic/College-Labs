package mjaksic.distributed_system_node.serialisation;

import java.io.ByteArrayInputStream;
import java.io.ByteArrayOutputStream;
import java.io.IOException;
import java.io.ObjectInputStream;
import java.io.ObjectOutputStream;

public class ByteSerialiser {
	
	private static ByteArrayOutputStream byte_array_serialiser = CreateByteArraySerialiser();
	private static ObjectOutputStream object_serialiser = CreateSerialiser();
	
	

	private static ByteArrayOutputStream CreateByteArraySerialiser() {
		ByteArrayOutputStream byte_array_serialiser = new ByteArrayOutputStream();
		
		return byte_array_serialiser;
	}
	
	private static ObjectOutputStream CreateSerialiser() {
		ObjectOutputStream object_serialiser = null;
		try {
			object_serialiser = new ObjectOutputStream(ByteSerialiser.byte_array_serialiser);
		} catch (IOException e) {
			e.printStackTrace();
		}
		
		return object_serialiser;
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
	
	
	
	public static byte[] Serialise(Object object) {
		try {
			ByteSerialiser.object_serialiser.flush();
			ByteSerialiser.object_serialiser.writeObject(object);
		} catch (IOException e) {
			e.printStackTrace();
		}
		
		return ByteSerialiser.byte_array_serialiser.toByteArray();
	}
	
	public static Object Deserialise(byte[] byte_array) {
		ByteArrayInputStream byte_array_deserialiser = CreateByteArrayDeserialiser(byte_array);
		ObjectInputStream object_deserialiser = CreateDeserialiser(byte_array_deserialiser);
		
		Object object = null;
		try {
			object = object_deserialiser.readObject();
		} catch (ClassNotFoundException e) {
			e.printStackTrace();
		} catch (IOException e) {
			e.printStackTrace();
		}
		
		return object;
	}
	
}
