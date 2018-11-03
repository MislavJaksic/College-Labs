package mjaksic.distributed_system_client.sensor;

import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.atomic.AtomicBoolean;

public class Sensor {
	
	private static final int client_and_sever_threads = 2;
	
	private static final int server_threads = 2;
	private static final int server_max_backlog = 10;
	private static final int server_blocking_timeout = 2500;
	
	private ExecutorService two_thread_pool = this.CreateThreadPool();
	
	private SensorClient client;
	private SensorServer server;
	
	
	public Sensor() {
		AtomicBoolean server_running = this.CreateServerControlFlag();
		this.server = this.CreateSensorServer(server_running);
		this.client = this.CreateSensorClient(server_running);
		
		this.RunServerAndClient();
		this.ShutdownUponExecutionCompletion();
	}
	
	private AtomicBoolean CreateServerControlFlag() {
		return new AtomicBoolean(true);
	}
	
	private SensorServer CreateSensorServer(AtomicBoolean control_flag) {
		return new SensorServer(control_flag, Sensor.server_threads, Sensor.server_max_backlog, Sensor.server_blocking_timeout);
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
