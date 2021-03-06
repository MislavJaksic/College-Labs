package mjaksic.distributed_system_node.sensor;

import java.io.IOException;
import java.net.DatagramPacket;
import java.net.InetAddress;
import java.net.UnknownHostException;
import java.util.List;
import java.util.concurrent.atomic.AtomicBoolean;
import java.util.concurrent.atomic.AtomicInteger;
import java.util.concurrent.atomic.AtomicIntegerArray;

import mjaksic.distributed_system_node.message.Message;
import mjaksic.distributed_system_node.message.MessageManager;
import mjaksic.distributed_system_node.network_simulator.SimpleSimulatedDatagramSocket;
import mjaksic.distributed_system_node.serialisation.ByteSerialiser;

public class SensorServer implements Runnable {
	//private AtomicBoolean server_running;
	
	private AtomicInteger scalar_time;
	private AtomicIntegerArray vector_time;

	private int port;

	private SimpleSimulatedDatagramSocket socket;
	
	private MessageManager message_manager;
	
	

	public SensorServer(AtomicBoolean server_running, AtomicInteger scalar_time, AtomicIntegerArray vector_time,
			List<Integer> ports, double loss_rate, int average_delay, MessageManager message_manager) {
		//this.server_running = server_running;
		
		this.SetLogicClocks(scalar_time, vector_time);
		
		this.SetPorts(ports);

		this.SetSocket(loss_rate, average_delay);
		
		this.SetMessageManager(message_manager);
	}
	
	private void SetLogicClocks(AtomicInteger scalar_time, AtomicIntegerArray vector_time) {
		this.scalar_time = scalar_time;
		this.vector_time = vector_time;
	}
	
	private void SetPorts(List<Integer> ports) {
		this.port = ports.get(0);
	}
	
	private void SetSocket(double loss_rate, int average_delay) {
		this.socket = this.CreateSocket(loss_rate, average_delay);
	}

	private SimpleSimulatedDatagramSocket CreateSocket(double loss_rate, int average_delay) {
		int my_port = this.GetPortOfOrigin();
		
		SimpleSimulatedDatagramSocket server_socket = null;
		try {
			server_socket = new SimpleSimulatedDatagramSocket(my_port, loss_rate, average_delay);
			System.out.println("Created server socket");
		} catch (IOException e) {
			e.printStackTrace();
		}
		return server_socket;
	}

	private void SetMessageManager(MessageManager message_manager) {
		this.message_manager = message_manager;
	}
	
	
	
	@Override
	public void run() {
		this.ListenForIncomingMessages();
		//this.Shutdown();
	}
	
	private void ListenForIncomingMessages() {
		Message message;
		//while (this.IsRunningFlagUp()) {
		while(true) {
			message = this.ReceiveMessage();
			this.ActOnMessage(message);
		}
	}

	/*private boolean IsRunningFlagUp() {
		boolean flag = this.server_running.get();
		return flag;
	}*/

	
	
	private Message ReceiveMessage() {
		byte[] byte_array = ReceiveBytes();
		Message message = (Message) ByteSerialiser.Deserialise(byte_array);

		return message;
	}

	private byte[] ReceiveBytes() {
		byte[] byte_array = new byte[1024];
		DatagramPacket packet = new DatagramPacket(byte_array, byte_array.length);

		try {
			this.socket.receive(packet);
		} catch (IOException e) {
			e.printStackTrace();
		}
		
		return byte_array;
	}

	
	
	private void ActOnMessage(Message message) {
		int scalar_time = message.scalar_time;
		List<Integer> vector_time = message.vector_time;
		
		this.UpdateLogicalClocks(scalar_time, vector_time);
		
		if (this.IsResponse(message)) {
			this.ActOnResponse(message);
		} else {
			this.ActOnMeasurement(message);
		}
	}
	
	private boolean IsResponse(Message message) {
		if (message.port_of_origin == this.GetPortOfOrigin()) {
			return true;
		}
		return false;
	}

	
	
	private void ActOnResponse(Message message) {
		//System.out.println("Received response: " + message);
		this.RecordResponse(message);
	}
	
	
	
	private void ActOnMeasurement(Message message) {
		//System.out.println("Received message: " + message);
		
		this.IncrementLogicalClocks();
		
		this.SendResponse(message);
		
		this.RecordMeasurementMessage(message);
	}
	
	private void SendResponse(Message message) {
		byte[] byte_array = ByteSerialiser.Serialise(message);
		int destination_port = message.port_of_origin;
		//System.out.println("Response sent: " + message);
		
		this.SendBytesToDestination(byte_array, destination_port);
	}
	
	
	
	private void SendBytesToDestination(byte[] byte_array, int destination_port) {
		InetAddress address = this.GetAddress();
		DatagramPacket packet = new DatagramPacket(byte_array, byte_array.length, address, destination_port);
		
	    this.SendPacket(packet);
	}
	
	private InetAddress GetAddress() {
		InetAddress address = null;
		try {
			address = InetAddress.getByName("localhost");
		} catch (UnknownHostException e) {
			e.printStackTrace();
		}
		
		return address;
	}
	
	
	
	private void SendPacket(DatagramPacket packet) {
		try {
			this.socket.send(packet);
		} catch (IOException e) {
			e.printStackTrace();
		}
	}

	
	
	private void RecordMeasurementMessage(Message message) {
		this.message_manager.PutMeasurementMessage(message);
	}
	
	private void RecordResponse(Message message) {
		this.message_manager.RegisterResponse(message);
	}
	
	
	
	private void UpdateLogicalClocks(int received_scalar_time, List<Integer> receieved_vector_time) {
		this.UpdateScalarTime(received_scalar_time);
		this.UpdateVectorTime(receieved_vector_time);
	}
		
	private void UpdateScalarTime(int received_scalar_time) {
		int new_time = Math.max(this.scalar_time.get(), received_scalar_time);
		
		this.scalar_time.set(new_time);
		
		this.IncrementScalarTime();
	}
	
	private void UpdateVectorTime(List<Integer> receieved_vector_time) {
		int length = this.vector_time.length();
		int new_time;
		
		for (int i = 0; i < length; i++) {
			new_time = Math.max(this.vector_time.get(i), receieved_vector_time.get(i));
			this.vector_time.set(i, new_time);
		}
		
		this.IncrementVectorTime();
	}
	
	private void IncrementLogicalClocks() {
		this.IncrementScalarTime();
		this.IncrementVectorTime();
	}
	
	private void IncrementScalarTime() {
		this.scalar_time.incrementAndGet();
	}

	private void IncrementVectorTime() {
		int index = this.GetPortOfOrigin() % this.vector_time.length();
		this.vector_time.incrementAndGet(index);
	}

	
	
	private int GetPortOfOrigin() {
		return this.port;
	}
	
	
	
	public void Shutdown() {
		System.out.println("Shutting down the server...");
		this.CloseServer();
		System.out.println("Server closed");
	}
	
	private void CloseServer() {
		System.out.println("Closing server...");
		this.CloseServerSocket();
	}
	
	private void CloseServerSocket() {
		this.socket.close();
		System.out.println("Server socket closed");
	}

}
