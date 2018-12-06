package mjaksic.distributed_system_node.sensor;

import java.io.IOException;
import java.net.DatagramPacket;
import java.net.InetAddress;
import java.net.UnknownHostException;
import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.atomic.AtomicBoolean;
import java.util.concurrent.atomic.AtomicInteger;
import java.util.concurrent.atomic.AtomicIntegerArray;

import mjaksic.distributed_system_node.measurement.Measurement;
import mjaksic.distributed_system_node.measurement.MeasurementSimulator;
import mjaksic.distributed_system_node.message.Message;
import mjaksic.distributed_system_node.network_simulator.SimpleSimulatedDatagramSocket;
import mjaksic.distributed_system_node.serialisation.ByteSerialiser;

public class SensorClient implements Runnable {
	private int start_time;
	private AtomicBoolean server_running;
	private AtomicInteger scalar_time;
	private AtomicIntegerArray vector_time;
	
	private int port;
	private List<Integer> other_ports;
	
	private SimpleSimulatedDatagramSocket socket;
	
	
	
	public SensorClient(AtomicBoolean server_running, AtomicInteger scalar_time, AtomicIntegerArray vector_time,
			List<Integer> ports, double loss_rate, int average_delay) {
		this.start_time = this.GetTimeInSeconds();
		this.server_running = server_running;
		this.scalar_time = scalar_time;
		this.vector_time = vector_time;
		
		this.port = ports.get(0);
		this.other_ports = ports.subList(1, ports.size());
		
		this.socket = this.CreateSocket(loss_rate, average_delay);
	}
	
	private int GetTimeInSeconds() {
		int seconds = (int) (System.currentTimeMillis() / 1000);
		return seconds;
	}
	
	private SimpleSimulatedDatagramSocket CreateSocket(double loss_rate, int average_delay) {
		SimpleSimulatedDatagramSocket server_socket = null;
		try {
			server_socket = new SimpleSimulatedDatagramSocket(loss_rate, average_delay);
			System.out.println("Created server socket");
		} catch (IOException e) {
			e.printStackTrace();
		}
		return server_socket;
	}
	
	
	
	@Override
	public void run() {
		this.Sleep(20000);
		while (true) {
			this.Sleep(1000);
			
			this.ResendMeasurements();
			this.SendMeasurement();
		}
		//this.Shutdown();
	}
	
	private void Sleep(int miliseconds) {
		System.out.println("Sleeping...");
		try {
			Thread.sleep(miliseconds);
		} catch (InterruptedException e) {
			e.printStackTrace();
		}
	}
	
	private void ResendMeasurements() {
		
	}
	
	private void SendMeasurement() {
		Message message = CreateMeasurementMessage();
		System.out.println("Sent: " + message);
		byte[] byte_array = ByteSerialiser.Serialise(message);
		
		this.SendPacketsToOtherPorts(byte_array);
	}
	
	private Message CreateMeasurementMessage() {
		Measurement measurement = this.GetMeasurement();
		int scalar_time = this.scalar_time.get();
		List<Integer> vector_time = CreateMessageVectorTime();
		boolean is_confirm = false;
		
		Message message = new Message(measurement, scalar_time, vector_time, is_confirm);
		
		return message;
	}
	
	private Measurement GetMeasurement() {
		int elapsed_time = this.GetElapsedSeconds();
		Measurement measurement = MeasurementSimulator.GetMeasurementBasedOnTime(elapsed_time);
		return measurement;
	}
	
	private int GetElapsedSeconds() {
		int current_time = this.GetTimeInSeconds();
		return current_time - this.start_time;
	}
	
	private List<Integer> CreateMessageVectorTime() {
		ArrayList<Integer> vector_time = new ArrayList<Integer>();
		
		for (int i = 0; i < this.vector_time.length(); i++) {
			vector_time.add(this.vector_time.get(i));
		}
		
		return vector_time;
	}
	
	
	private void SendPacketsToOtherPorts(byte[] byte_array) {
		InetAddress address = this.GetAddress();
		DatagramPacket packet;
		
		for (int i = 0; i < this.other_ports.size(); i++) {
			packet = new DatagramPacket(byte_array, byte_array.length, address, this.other_ports.get(i));
	        this.SendPacket(packet);
		}
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
	
	
	
	private void Shutdown() {
		System.out.println("Closing client...");
		this.SetServerRunningFlag(false);
		System.out.println("Client closed");
	}

	private void SetServerRunningFlag(boolean state) {
		this.server_running.set(state);
	}
}
