package mjaksic.distributed_system_node.sensor;

import java.io.IOException;
import java.net.DatagramPacket;
import java.util.concurrent.atomic.AtomicBoolean;
import java.util.concurrent.atomic.AtomicInteger;
import java.util.concurrent.atomic.AtomicIntegerArray;

import mjaksic.distributed_system_node.message.Message;
import mjaksic.distributed_system_node.network_simulator.SimpleSimulatedDatagramSocket;
import mjaksic.distributed_system_node.serialisation.ByteSerialiser;

public class SensorServer implements Runnable {
	
	private AtomicBoolean server_running;
	AtomicInteger scalar_time;
	AtomicIntegerArray vector_time;

	private SimpleSimulatedDatagramSocket server_socket;

	
	
	public SensorServer(AtomicBoolean server_running, AtomicInteger scalar_time, AtomicIntegerArray vector_time, int port, float loss_rate, int average_delay) {
		this.server_running = server_running;
		this.scalar_time = scalar_time;
		this.vector_time = vector_time;
		
		this.server_socket = this.CreateServerSocketWithFixedPort(port, loss_rate, average_delay);
	}

	private SimpleSimulatedDatagramSocket CreateServerSocketWithFixedPort(int port, float loss_rate,
			int average_delay) {
		SimpleSimulatedDatagramSocket server_socket = null;
		try {
			server_socket = new SimpleSimulatedDatagramSocket(port, loss_rate, average_delay);
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
			this.server_socket.receive(packet);
		} catch (IOException e) {
			e.printStackTrace();
		}

		return byte_array;
	}

	private void ActOnMessage(Message message) {
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
	
	
	
	public void Shutdown() {
		System.out.println("Closing server...");
		this.CloseServer();
		System.out.println("Server closed");
	}

	private void CloseServer() {
		System.out.println("Closing server...");
		this.CloseServerSocket();
	}

	private void CloseServerSocket() {
		this.server_socket.close();
		System.out.println("Server socket closed");
	}

}
