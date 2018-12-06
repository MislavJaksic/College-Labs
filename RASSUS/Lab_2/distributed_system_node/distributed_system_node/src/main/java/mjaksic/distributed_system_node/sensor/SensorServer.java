package mjaksic.distributed_system_node.sensor;

import java.io.IOException;
import java.net.DatagramPacket;
import java.util.List;
import java.util.concurrent.atomic.AtomicBoolean;
import java.util.concurrent.atomic.AtomicInteger;
import java.util.concurrent.atomic.AtomicIntegerArray;

import mjaksic.distributed_system_node.message.Message;
import mjaksic.distributed_system_node.network_simulator.SimpleSimulatedDatagramSocket;
import mjaksic.distributed_system_node.serialisation.ByteSerialiser;

public class SensorServer implements Runnable {

	private AtomicBoolean server_running;
	private AtomicInteger scalar_time;
	private AtomicIntegerArray vector_time;

	private int port;
	private List<Integer> other_ports;

	private SimpleSimulatedDatagramSocket socket;

	public SensorServer(AtomicBoolean server_running, AtomicInteger scalar_time, AtomicIntegerArray vector_time,
			List<Integer> ports, double loss_rate, int average_delay) {
		this.server_running = server_running;
		this.scalar_time = scalar_time;
		this.vector_time = vector_time;

		this.port = ports.get(0);
		this.other_ports = ports.subList(1, ports.size());

		this.socket = this.CreateSocketWithFixedPort(loss_rate, average_delay);
	}

	private SimpleSimulatedDatagramSocket CreateSocketWithFixedPort(double loss_rate, int average_delay) {
		SimpleSimulatedDatagramSocket server_socket = null;
		try {
			server_socket = new SimpleSimulatedDatagramSocket(this.port, loss_rate, average_delay);
			System.out.println("Created server socket");
		} catch (IOException e) {
			e.printStackTrace();
		}
		return server_socket;
	}

	
	
	@Override
	public void run() {
		this.ListenForIncomingMessages();
		this.Shutdown();
	}

	private void ListenForIncomingMessages() {
		Message message;
		while (this.IsRunningFlagUp()) {
			message = this.ReceiveMessage();
			this.ActOnMessage(message);
		}
	}

	private boolean IsRunningFlagUp() {
		boolean flag = this.server_running.get();
		return flag;
	}

	private Message ReceiveMessage() {
		byte[] byte_array = ReceivePacket();
		Message message = (Message) ByteSerialiser.Deserialise(byte_array);

		return message;
	}

	private byte[] ReceivePacket() {
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
		System.out.println("Received: " + message);
		if (message.is_confirm) {
			this.ActOnConfirm(message);
		} else {
			this.ActOnMeasurement(message);
		}
	}

	private void ActOnConfirm(Message message) {
		
	}

	private void ActOnMeasurement(Message message) {
		
	}

	
	
	void UpdateScalarTime(int received_scalar_time) {
		int new_time = Math.max(this.scalar_time.get(), received_scalar_time);
		this.scalar_time.set(new_time);
		this.IncrementScalarTime();
	}
	
	void UpdateVectorTime(List<Integer> receieved_vector_time) {
		int length = this.vector_time.length();
		int new_time;
		for (int i = 0; i < length; i++) {
			new_time = Math.max(this.vector_time.get(i), receieved_vector_time.get(i));
			this.vector_time.set(i, new_time);
		}
		
		this.IncrementVectorTime();
	}
	
	void IncrementScalarTime() {
		this.scalar_time.incrementAndGet();
	}

	void IncrementVectorTime() {
		int index = this.port % this.vector_time.length();
		this.vector_time.incrementAndGet(index);
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
