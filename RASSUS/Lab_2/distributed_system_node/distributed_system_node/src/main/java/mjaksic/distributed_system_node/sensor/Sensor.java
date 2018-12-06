package mjaksic.distributed_system_node.sensor;

import java.util.List;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.atomic.AtomicBoolean;
import java.util.concurrent.atomic.AtomicInteger;
import java.util.concurrent.atomic.AtomicIntegerArray;

public class Sensor {
	
	private static final int client_and_sever_threads = 2;
	
	private static final double UDP_loss_rate = 0.2;
	private static final int UDP_average_delay = 1000;
	
	private ExecutorService two_thread_pool = this.CreateThreadPool();
	
	private SensorClient client;
	private SensorServer server;
	
	
	public Sensor(List<Integer> ports) {
		AtomicBoolean server_running = this.CreateServerControlFlag();
		AtomicInteger scalar_time = this.CreateScalarTime();
		AtomicIntegerArray vector_time = this.CreateVectorTime(ports);
		
		this.server = this.CreateSensorServer(server_running, scalar_time, vector_time, ports);
		this.client = this.CreateSensorClient(server_running, scalar_time, vector_time, ports);
		
		this.RunServerAndClient();
		this.ShutdownUponExecutionCompletion();
	}

	private AtomicBoolean CreateServerControlFlag() {
		return new AtomicBoolean(true);
	}
	
	private AtomicInteger CreateScalarTime() {
		return new AtomicInteger(0);
	}
	
	private AtomicIntegerArray CreateVectorTime(List<Integer> ports) {
		int number_of_sensors = ports.size();
		return new AtomicIntegerArray(number_of_sensors);
	}
	
	private SensorServer CreateSensorServer(AtomicBoolean control_flag, AtomicInteger scalar_time, AtomicIntegerArray vector_time, List<Integer> ports) {
		return new SensorServer(control_flag, scalar_time, vector_time, ports, Sensor.UDP_loss_rate, Sensor.UDP_average_delay);
	}
	
	private SensorClient CreateSensorClient(AtomicBoolean control_flag, AtomicInteger scalar_time, AtomicIntegerArray vector_time, List<Integer> ports) {
		return new SensorClient(control_flag, scalar_time, vector_time, ports, Sensor.UDP_loss_rate, Sensor.UDP_average_delay);
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
	}
	
}
