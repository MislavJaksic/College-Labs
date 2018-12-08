package mjaksic.distributed_system_node.sensor;

import java.util.List;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.atomic.AtomicBoolean;
import java.util.concurrent.atomic.AtomicInteger;
import java.util.concurrent.atomic.AtomicIntegerArray;

import mjaksic.distributed_system_node.message.MessageManager;

public class Sensor {
	private static final int client_and_sever_threads = 2;

	private static final double UDP_loss_rate = 0.2;
	private static final int UDP_average_delay = 1000;

	private ExecutorService client_and_server_thraed_pool;

	private SensorClient client;
	private SensorServer server;



	public Sensor(List<Integer> my_port_and_other_ports) {
		AtomicBoolean shutdown_control_flag = this.CreateShutdownControlFlag();
		AtomicInteger scalar_time = this.CreateScalarTime();
		AtomicIntegerArray vector_time = this.CreateVectorTime(my_port_and_other_ports);

		MessageManager message_manager = this.CreateMessageManager();

		this.SetSensorServer(shutdown_control_flag, scalar_time, vector_time, my_port_and_other_ports, message_manager);
		this.SetSensorClient(shutdown_control_flag, scalar_time, vector_time, my_port_and_other_ports, message_manager);

		this.SetClientAndServerThraedPool();

		this.RunServerAndClient();
		this.ShutdownUponExecutionCompletion();
	}

	private AtomicBoolean CreateShutdownControlFlag() {
		return new AtomicBoolean(true);
	}

	private AtomicInteger CreateScalarTime() {
		return new AtomicInteger(0);
	}

	private AtomicIntegerArray CreateVectorTime(List<Integer> ports) {
		int number_of_sensors = ports.size();
		return new AtomicIntegerArray(number_of_sensors);
	}



	private MessageManager CreateMessageManager() {
		MessageManager manager = new MessageManager();

		return manager;
	}



	private void SetSensorServer(AtomicBoolean shutdown_control_flag, AtomicInteger scalar_time,
			AtomicIntegerArray vector_time, List<Integer> my_port_and_other_ports, MessageManager message_manager) {
		this.server = this.CreateSensorServer(shutdown_control_flag, scalar_time, vector_time, my_port_and_other_ports,
				message_manager);
	}

	private void SetSensorClient(AtomicBoolean shutdown_control_flag, AtomicInteger scalar_time,
			AtomicIntegerArray vector_time, List<Integer> my_port_and_other_ports, MessageManager message_manager) {
		this.client = this.CreateSensorClient(shutdown_control_flag, scalar_time, vector_time, my_port_and_other_ports,
				message_manager);
	}

	private SensorServer CreateSensorServer(AtomicBoolean shutdown_control_flag, AtomicInteger scalar_time,
			AtomicIntegerArray vector_time, List<Integer> my_port_and_other_ports, MessageManager message_manager) {
		return new SensorServer(shutdown_control_flag, scalar_time, vector_time, my_port_and_other_ports,
				Sensor.UDP_loss_rate, Sensor.UDP_average_delay, message_manager);
	}

	private SensorClient CreateSensorClient(AtomicBoolean shutdown_control_flag, AtomicInteger scalar_time,
			AtomicIntegerArray vector_time, List<Integer> my_port_and_other_ports, MessageManager message_manager) {
		return new SensorClient(shutdown_control_flag, scalar_time, vector_time, my_port_and_other_ports,
				Sensor.UDP_loss_rate, Sensor.UDP_average_delay, message_manager);
	}



	private void SetClientAndServerThraedPool() {
		this.client_and_server_thraed_pool = this.CreateThreadPool(Sensor.client_and_sever_threads);

	}

	private ExecutorService CreateThreadPool(int number_of_threads) {
		System.out.println("Creating thread pool");
		return Executors.newFixedThreadPool(number_of_threads);
	}



	private void RunServerAndClient() {
		this.client_and_server_thraed_pool.execute(this.server);
		this.client_and_server_thraed_pool.execute(this.client);
	}

	private void ShutdownUponExecutionCompletion() {
		this.client_and_server_thraed_pool.shutdown();
	}

}
