package mjaksic.distributed_system_node.sensor;

import java.io.IOException;
import java.io.OutputStream;
import java.io.OutputStreamWriter;
import java.io.PrintWriter;
import java.net.Socket;
import java.util.concurrent.atomic.AtomicBoolean;
import java.util.concurrent.atomic.AtomicInteger;

import mjaksic.distributed_system_client.measurements.Measurement;
import mjaksic.distributed_system_client.measurements.MeasurementSimulator;

public class Worker implements Runnable {
	
	private Socket client_socket;
	private AtomicBoolean all_workers_running;
	private AtomicInteger active_workers;

	private PrintWriter writer;
	
	private int start_time;

	public Worker(Socket client_socket, AtomicBoolean all_workers_running, AtomicInteger active_workers) {
		this.client_socket = client_socket;
		this.all_workers_running = all_workers_running;
		this.active_workers = active_workers;

		this.writer = this.CreateWriter();
		
		this.start_time = this.GetTimeInSeconds();
	}

	private PrintWriter CreateWriter() {
		OutputStream stream = this.CreateOutputStream();
		OutputStreamWriter stream_writer = new OutputStreamWriter(stream);
		PrintWriter writer = new PrintWriter(stream_writer, true);
		return writer;
	}

	private OutputStream CreateOutputStream() {
		OutputStream stream = null;
		try {
			stream = this.client_socket.getOutputStream();
		} catch (IOException e) {
			e.printStackTrace();
		}
		return stream;
	}
	
	private int GetTimeInSeconds() {
		int seconds = (int) (System.currentTimeMillis() / 1000);
		return seconds;
	}

	
	
	public void run() {
		String measurement;
		while (this.IsAllWorkerRunningFlagUp()) {
			this.Sleep(5000);
			measurement = this.DoWork();

			this.Write(measurement);
		}
		this.Shutdown();
	}
	
	
	
	private boolean IsAllWorkerRunningFlagUp() {
		return this.all_workers_running.get();
	}
	
	private void Sleep(int miliseconds) {
		try {
			Thread.sleep(miliseconds);
		} catch (InterruptedException e) {
			e.printStackTrace();
		}
	}
	
	

	private void Write(String string) {
		this.writer.println(string);
	}
	
	
	
	private String DoWork() {
		Measurement measurement = this.GetMeasurement();
		String string = measurement.getTemperature() + "," + measurement.getPressure() + "," + measurement.getHumidity() + "," + measurement.getCO() + "," + measurement.getNO2() + "," + measurement.getSO2();
		return string;
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
	
	
	
	private void Shutdown() {
		System.out.println("Shutdown has begun...");
		this.DecrementActiveWorkers();
		System.out.println("Shutdown successful");
	}
	
	private void DecrementActiveWorkers() {
		this.active_workers.getAndDecrement();
		System.out.println("Decremented workers to " + this.active_workers.get());
	}
}