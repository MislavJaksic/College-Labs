package mjaksic.distributed_system_node.sensor;

import java.io.IOException;
import java.net.DatagramPacket;
import java.net.InetAddress;
import java.net.UnknownHostException;
import java.util.ArrayList;
import java.util.List;
import java.util.Set;
import java.util.concurrent.atomic.AtomicBoolean;
import java.util.concurrent.atomic.AtomicInteger;
import java.util.concurrent.atomic.AtomicIntegerArray;

import mjaksic.distributed_system_node.measurement.Measurement;
import mjaksic.distributed_system_node.measurement.MeasurementSimulator;
import mjaksic.distributed_system_node.message.Message;
import mjaksic.distributed_system_node.message.MessageManager;
import mjaksic.distributed_system_node.network_simulator.SimpleSimulatedDatagramSocket;
import mjaksic.distributed_system_node.serialisation.ByteSerialiser;

public class SensorClient implements Runnable {
	private static final int first_sleep_dutation = 5000;
	private static final int normal_sleep_dutation = 1000;
	private static final int number_of_sleeps_before_reporting_result = 5;
	
	private int start_time;
	// private AtomicBoolean server_running;

	private AtomicInteger scalar_time;
	private AtomicIntegerArray vector_time;

	private int port;
	private List<Integer> other_ports;

	private SimpleSimulatedDatagramSocket socket;

	private MessageManager message_manager;

	
	
	public SensorClient(AtomicBoolean server_running, AtomicInteger scalar_time, AtomicIntegerArray vector_time,
			List<Integer> ports, double loss_rate, int average_delay, MessageManager message_manager) {
		this.SetStartTime();
		// this.server_running = server_running;

		this.SetLogicClocks(scalar_time, vector_time);

		this.SetPorts(ports);

		this.SetSocket(loss_rate, average_delay);
		
		this.SetMessageManager(message_manager);
	}
	
	private void SetStartTime() {
		this.start_time = this.GetTimeInSeconds();
	}

	private int GetTimeInSeconds() {
		int seconds = (int) (System.currentTimeMillis() / 1000);
		return seconds;
	}

	private void SetLogicClocks(AtomicInteger scalar_time, AtomicIntegerArray vector_time) {
		this.scalar_time = scalar_time;
		this.vector_time = vector_time;
	}

	private void SetPorts(List<Integer> ports) {
		this.port = ports.get(0);
		this.other_ports = ports.subList(1, ports.size());
		System.out.println("My port: " + this.port + ", other ports: " + this.other_ports);
	}

	private void SetSocket(double loss_rate, int average_delay) {
		this.socket = this.CreateSocket(loss_rate, average_delay);
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

	private void SetMessageManager(MessageManager message_manager) {
		this.message_manager = message_manager;
	}
	
	
	
	@Override
	public void run() {
		this.Sleep(SensorClient.first_sleep_dutation);
		
		while (true) {
			for (int i = 0; i < SensorClient.number_of_sleeps_before_reporting_result; i++) {
				this.Sleep(SensorClient.normal_sleep_dutation);

				this.ResendMeasurements();
				this.SendMeasurements();
			}
			
			this.PrintMeasurements();
			this.DeleteMeasurements();
		}
		// this.Shutdown();
	}

	
	
	private void ResendMeasurements() {
		Set<Message> messages = this.message_manager.GetUnconfirmedMessages();
		for (Message message : messages) {
			this.SendMessage(message);
			// System.out.println("Resending: " + message);
		}
	}

	
	
	private void SendMeasurements() {
		this.IncrementLogicalClocks();

		Measurement measurement = this.GetMeasurement();
		this.CreateMessage(measurement);
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

	
	
	private void CreateMessage(Measurement measurement) {
		int scalar_time = this.GetScalarTime();
		List<Integer> vector_time = this.GetVectorTime();
		int port_of_origin = this.GetPortOfOrigin();
		List<Integer> destination_ports = this.GetDestinationPorts();

		Message message = null;
		for (int destination_port : destination_ports) {
			message = new Message(measurement, scalar_time, vector_time, port_of_origin, destination_port);

			this.SendMessage(message);
			this.RecordMessageWithoutResponse(message);
			// System.out.println("Sent: " + message);
		}

		this.RecordMeasurementMessage(message);
	}

	
	
	private void SendMessage(Message message) {
		byte[] byte_array = ByteSerialiser.Serialise(message);
		int destination_port = message.destination_port;

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

	
	
	private void PrintMeasurements() {
		System.out.println(this.message_manager.GetScalarSortedMeasurementMessages());
		System.out.println(this.message_manager.GetVectorSortedMeasurementMessages());
		System.out.println(this.message_manager.GetAverageMeasurement());
	}
	
	
	
	private void RecordMessageWithoutResponse(Message message) {
		this.message_manager.PutMessageWithoutResponse(message);
	}

	private void RecordMeasurementMessage(Message message) {
		this.message_manager.PutMeasurementMessage(message);
	}

	private void DeleteMeasurements() {
		this.message_manager.DeleteMeasurementMessages();
	}
	
	
	
	private int GetScalarTime() {
		return this.scalar_time.get();
	}

	private List<Integer> GetVectorTime() {
		ArrayList<Integer> vector_time = new ArrayList<Integer>();

		for (int i = 0; i < this.vector_time.length(); i++) {
			vector_time.add(this.vector_time.get(i));
		}

		return vector_time;
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

	private List<Integer> GetDestinationPorts() {
		return this.other_ports;
	}

	
	
	private void Sleep(int miliseconds) {
		// System.out.println("Sleeping...");
		try {
			Thread.sleep(miliseconds);
		} catch (InterruptedException e) {
			e.printStackTrace();
		}
	}

	
	
	/*
	 * private void Shutdown() { System.out.println("Closing client...");
	 * this.SetServerRunningFlag(false); System.out.println("Client closed"); }
	 * 
	 * private void SetServerRunningFlag(boolean state) {
	 * this.server_running.set(state); }
	 */
}
