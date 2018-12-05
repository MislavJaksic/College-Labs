package mjaksic.distributed_system_node.sensor;

import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.atomic.AtomicBoolean;
import java.util.concurrent.atomic.AtomicInteger;
import java.util.concurrent.atomic.AtomicIntegerArray;

public class Sensor {
	
	private static final int client_and_sever_threads = 2;
	
	private static final int number_of_sensors = 3;
	
	private static final double UDP_loss_rate = 0.2;
	private static final int UDP_average_delay = 200;
	
	private ExecutorService two_thread_pool = this.CreateThreadPool();
	
	private SensorClient client;
	private SensorServer server;
	
	
	public Sensor() {
		AtomicBoolean server_running = this.CreateServerControlFlag();
		AtomicInteger scalar_time = this.CreateScalarTime();
		AtomicIntegerArray vector_time = this.CreateVectorTime();
		
		this.server = this.CreateSensorServer(server_running, scalar_time, vector_time);
		this.client = this.CreateSensorClient(server_running, scalar_time, vector_time);
		
		this.RunServerAndClient();
		this.ShutdownUponExecutionCompletion();
	}

	private AtomicBoolean CreateServerControlFlag() {
		return new AtomicBoolean(true);
	}
	
	private AtomicInteger CreateScalarTime() {
		return new AtomicInteger(0);
	}
	
	private AtomicIntegerArray CreateVectorTime() {
		return new AtomicIntegerArray(Sensor.number_of_sensors) ;
	}
	
	private SensorServer CreateSensorServer(AtomicBoolean control_flag, AtomicInteger scalar_time, AtomicIntegerArray vector_time) {
		return new SensorServer(control_flag, scalar_time, vector_time, Sensor.UDP_loss_rate, Sensor.UDP_average_delay);
	}
	
	private String GetServerIP() {
		return this.server.GetIP();
	}
	
	private int GetServerPort() {
		return this.server.GetLocalPort();
	}
	
	private SensorClient CreateSensorClient(AtomicBoolean control_flag) {
		String server_ip = this.GetServerIP();
		int server_port = this.GetServerPort();
		return new SensorClient(control_flag, server_ip, server_port);
	}
	
	private ExecutorService CreateThreadPool() {
		System.out.println("Creating thread pool");
		return Executors.newFixedThreadPool(Sensor.client_and_sever_threads);
	}

	
	
	private void RunServerAndClient() {
		two_thread_pool.execute(this.server);
		two_thread_pool.execute(this.client);
	}
	
	private void ShutdownUponExecutionCompletion() {
		this.two_thread_pool.shutdown();
		System.out.println("Sensor ready to shutdown");
	}
	
}
