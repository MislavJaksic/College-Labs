package mjaksic.distributed_system_node.sensor;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.net.Socket;
import java.util.Random;
import java.util.UUID;
import java.util.concurrent.atomic.AtomicBoolean;

import mjaksic.distributed_system_client.measurements.Measurement;
import mjaksic.distributed_system_client.measurements.MeasurementSimulator;
import mjaksic.distributed_system_client.service_communication.RESTInteractor;
import mjaksic.distributed_system_client.service_communication.SensorAddress;
import mjaksic.distributed_system_client.service_communication.SensorRegistration;

public class SensorClient implements Runnable {

	private static final double longitude_min = 15.87;
	private static final double longitude_max = 16.0;
	private static final double latitude_min = 45.75;
	private static final double latitude_max = 45.85;
	
	private int start_time;
	private AtomicBoolean server_running;
	
	private SensorRegistration registration;
	private String client_id;
	
	private BufferedReader user_input_reader;
	private BufferedReader neighbour_reader;
	private Socket neighbour_socket;
	
	public SensorClient(AtomicBoolean server_running, String server_ip, int server_port) {
		this.start_time = this.GetTimeInSeconds();
		this.server_running = server_running;
		
		this.registration = this.CreateRegistration(server_ip, server_port);
		this.client_id = this.GenerateUUID();
		
		this.user_input_reader = this.CreateUserInputReader();
		this.RegisterSensor();
	}
	
	private int GetTimeInSeconds() {
		int seconds = (int) (System.currentTimeMillis() / 1000);
		return seconds;
	}
	
	private SensorRegistration CreateRegistration(String ip, int port) {
		double longitude = this.GenerateRandomDouble(longitude_min, longitude_max);
		double latitude = this.GenerateRandomDouble(latitude_min, latitude_max);
		SensorRegistration registration = new SensorRegistration(ip, port, longitude, latitude);
		return registration; 
	}
	
	private String GenerateUUID() {
		return UUID.randomUUID().toString();
	}
	
	private double GenerateRandomDouble(double min, double max) {
		Random random_seed = new Random();
		double random_value = min + (max - min) * random_seed.nextDouble();
		return random_value;
	}
	
	private BufferedReader CreateUserInputReader() {
		InputStream stream = System.in;
		InputStreamReader stream_reader = new InputStreamReader(stream);
		BufferedReader user_input_reader = new BufferedReader(stream_reader);
		return user_input_reader;
	}
	
	
	
	private void RegisterSensor() {
		RESTInteractor.Register(this.client_id, this.registration);
	}
	
	
	
	@Override
	public void run() {
		String user_input;

		while (true) {
			user_input = this.ReadUserInput();

			if (this.IsShutdownCommand(user_input)) {
				break;
			}
			
			if (this.IsMeasureCommand(user_input)) {
				this.Measure();
			}
		}
		this.Shutdown();
	}
	
	
	
	private String ReadUserInput() {
		String received_string = null;
		try {
			System.out.println("Awaiting user input::: ");
			received_string = this.user_input_reader.readLine();
		} catch (IOException e) {
			e.printStackTrace();
		}
		return received_string;
	}
	
	private boolean IsShutdownCommand(String string) {
		if (string == null) {
			return true;
		}
		if (string.length() == 0) {
			return true;
		}
		if (string.contains("shutdown")) {
			return true;
		}
		return false;
	}
	
	private boolean IsMeasureCommand(String string) {
		if (string.contains("measure")) {
			return true;
		}
		return false;
	}
	
	
	
	private void Measure() {
		Measurement measurement = this.GetMeasurement();
		Measurement neighbour_measurement = this.GetNeighbourMeasurement();
		
		Measurement average_measurement = this.AverageMeasurements(measurement, neighbour_measurement);
		this.StoreMeasurement(this.client_id, average_measurement);
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
	
	private Measurement GetNeighbourMeasurement() {
		SensorAddress address = this.GetNeighbourAddress();
		
		Measurement measurement = this.ReceiveMeasurement(address);
		return measurement;
	}
	
	
	private SensorAddress GetNeighbourAddress() {
		SensorAddress address = RESTInteractor.GetClosest(this.client_id);
		return address;
	}
	
	private Measurement ReceiveMeasurement(SensorAddress address) {
		this.EstablishNeighbourConnection(address);
		
		String string_measurement = this.ReadMeasurement();
		Measurement measurement = this.FromStringToMeasurement(string_measurement);
		
		return measurement;
	}
	
	private void EstablishNeighbourConnection(SensorAddress address) {
		if (this.IsNeighbourReaderMissing()) {
			this.neighbour_socket = this.CreateClientSocket(address);
			this.neighbour_reader = this.CreateReader();
		}
		}
	
	private boolean IsNeighbourReaderMissing() {
		if (this.neighbour_reader == null) {
			return true;
		}
		return false;
	}
	
	private Socket CreateClientSocket(SensorAddress address) {
		Socket socket = null;
		try {
			socket = new Socket(address.getIp(), address.getPort());
		} catch (IOException e) {
			e.printStackTrace();
		}
		return socket;
	}

	private BufferedReader CreateReader() {
		InputStream stream = this.CreateInputStream();
		InputStreamReader stream_reader = new InputStreamReader(stream);
		BufferedReader server_reader = new BufferedReader(stream_reader);
		return server_reader;
	}

	private InputStream CreateInputStream() {
		InputStream stream = null;
		try {
			stream = this.neighbour_socket.getInputStream();
		} catch (IOException e) {
			e.printStackTrace();
		}
		return stream;
	}
	
	
	
	private String ReadMeasurement() {
		String received_string = null;
		try {
			received_string = this.neighbour_reader.readLine();
			System.out.println("Sensor received:::" + received_string);
		} catch (IOException e) {
			e.printStackTrace();
		}
		return received_string;
	}
	
	private Measurement FromStringToMeasurement(String string) {
		String[] measurement_data = string.split(",");
		
		Measurement measurement = new Measurement();
		measurement.setTemperature(Integer.parseInt(measurement_data[0]));
		measurement.setPressure(Integer.parseInt(measurement_data[1]));
		measurement.setHumidity(Integer.parseInt(measurement_data[2]));
		measurement.setCO(Integer.parseInt(measurement_data[3]));
		measurement.setNO2(Integer.parseInt(measurement_data[4]));
		measurement.setSO2(Integer.parseInt(measurement_data[5]));
		
		return measurement;
	}
	
	
	
	private Measurement AverageMeasurements(Measurement measurement_A, Measurement measurement_B) {
		Measurement average_measurement = new Measurement();
		Integer number_A;
		Integer number_B;
		
		number_A = measurement_A.getTemperature();
		number_B = measurement_B.getTemperature();
		if ((number_A.equals(0)) || (number_B.equals(0))) {
			average_measurement.setTemperature(number_A + number_B);
		} else {
			average_measurement.setTemperature((number_A + number_B) / 2);
		}
		
		number_A = measurement_A.getPressure();
		number_B = measurement_B.getPressure();
		if ((number_A == 0) || (number_B == 0)) {
			average_measurement.setPressure(number_A + number_B);
		} else {
			average_measurement.setPressure((number_A + number_B) / 2);
		}
		
		number_A = measurement_A.getHumidity();
		number_B = measurement_B.getHumidity();
		if ((number_A == 0) || (number_B == 0)) {
			average_measurement.setHumidity(number_A + number_B);
		} else {
			average_measurement.setHumidity((number_A + number_B) / 2);
		}
		
		number_A = measurement_A.getCO();
		number_B = measurement_B.getCO();
		if ((number_A == 0) || (number_B == 0)) {
			average_measurement.setCO(number_A + number_B);
		} else {
			average_measurement.setCO((number_A + number_B) / 2);
		}
		
		number_A = measurement_A.getNO2();
		number_B = measurement_B.getNO2();
		if ((number_A == 0) || (number_B == 0)) {
			average_measurement.setNO2(number_A + number_B);
		} else {
			average_measurement.setNO2((number_A + number_B) / 2);
		}
		
		number_A = measurement_A.getSO2();
		number_B = measurement_B.getSO2();
		if ((number_A == 0) || (number_B == 0)) {
			average_measurement.setSO2(number_A + number_B);
		} else {
			average_measurement.setSO2((number_A + number_B) / 2);
		}
		return average_measurement;
	}
	
	
	
	private void StoreMeasurement(String id, Measurement measurement) {
		RESTInteractor.StoreMeasurement(id, measurement);
	}
	
	
	
	private void Shutdown() {
		System.out.println("Closing client...");
		this.CloseReader();
		this.CloseSocket();
		this.SetServerRunningFlag(false);
		System.out.println("Client closed");
	}
	
	private void CloseReader() {
		try {
			this.neighbour_reader.close();
		} catch (IOException e) {
			e.printStackTrace();
		}
	}
	
	private void CloseSocket() {
		try {
			this.neighbour_socket.close();
		} catch (IOException e) {
			e.printStackTrace();
		}
	}

	private void SetServerRunningFlag(boolean state) {
		this.server_running.set(state);
	}
}
