package mjaksic.distributed_system_client;

import java.util.Random;
import java.util.UUID;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

public class Sensor {
	
	private static final int number_of_threads = 2;
	
	private ExecutorService thread_pool = this.CreateThreadPool();
	
	private static final double longitude_min = 15.87;
	private static final double longitude_max = 16.0;
	private static final double latitude_min = 45.75;
	private static final double latitude_max = 45.85;
	
	private final double longitude = this.GenerateRandomDouble(longitude_min, longitude_max);
	private final double latitude = this.GenerateRandomDouble(latitude_min, latitude_max);
	
	private final int start_time = this.GetTimeInSeconds();
	
	private final String id = this.GenerateUUID();
	
	private String ip;
	private int port;
	
	private SensorClient client;
	private SensorServer server;
	
	
	public Sensor() {
		this.client = new SensorClient();
		this.server = new SensorServer();
		//PORT RANGE 49152–65535
	}
	
	private ExecutorService CreateThreadPool() {
		System.out.println("Creating thread pool");
		return Executors.newFixedThreadPool(Sensor.number_of_threads);
	}

	private double GenerateRandomDouble(double min, double max) {
		Random random_seed = new Random();
		double random_value = min + (max - min) * random_seed.nextDouble();
		return random_value;
	}
	
	private int GetTimeInSeconds() {
		int seconds = (int) (System.currentTimeMillis() / 1000);
		return seconds;
	}
	
	private String GenerateUUID() {
		return UUID.randomUUID().toString();
	}
	
	
}
