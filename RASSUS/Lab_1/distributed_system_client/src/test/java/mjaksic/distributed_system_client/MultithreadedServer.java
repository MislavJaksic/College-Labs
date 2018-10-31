package mjaksic.distributed_system_client;

import java.io.IOException;
import java.net.ServerSocket;
import java.net.Socket;
import java.net.SocketException;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.atomic.AtomicBoolean;
import java.util.concurrent.atomic.AtomicInteger;

public class MultithreadedServer implements ServerIf {
	
	private int port;
	private int number_of_threads;
	private int backlog;

	private AtomicInteger active_workers;
	private ServerSocket server_socket;
	private ExecutorService thread_pool;
	private AtomicBoolean running_flag;

	public MultithreadedServer(int port, int number_of_threads, int backlog, int blocking_timeout) {
		this.port = port;
		this.number_of_threads = number_of_threads;
		this.backlog = backlog;

		this.active_workers = this.CreateAtomicInteger();
		this.server_socket = this.CreateServerSocket();
		this.SetSocketBlockingTimeout(blocking_timeout);
		this.thread_pool = this.CreateThreadPool();
		this.running_flag = this.CreateAtomicBoolean();
	}

	private AtomicInteger CreateAtomicInteger() {
		return new AtomicInteger(0);
	}

	private ServerSocket CreateServerSocket() {
		ServerSocket server_socket = null;
		try {
			server_socket = new ServerSocket(this.port, this.backlog);
		} catch (IOException e) {
			e.printStackTrace();
		}
		return server_socket;
	}

	private void SetSocketBlockingTimeout(int blocking_timeout) {
		try {
			this.server_socket.setSoTimeout(blocking_timeout);
		} catch (SocketException e) {
			e.printStackTrace();
		}
	}

	private ExecutorService CreateThreadPool() {
		return Executors.newFixedThreadPool(this.number_of_threads);
	}

	private AtomicBoolean CreateAtomicBoolean() {
		return new AtomicBoolean(true);
	}

	
	
	@Override
	public void startup() {

	}

	
	
	@Override
	public void loop() {
		Socket socket;
		while (this.IsRunningFlagUp()) {
			socket = this.AcceptConnectionAndCreateSocket();
			this.MakeWorkerUsingSocket(socket);
		}
	}

	private boolean IsRunningFlagUp() {
		return this.running_flag.get();
	}

	private Socket AcceptConnectionAndCreateSocket() {
		Socket socket = null;
		try {
			socket = this.server_socket.accept();
		} catch (IOException e) {
			e.printStackTrace();
		}
		return socket;
	}

	private void MakeWorkerUsingSocket(Socket socket) {
		Worker worker = new Worker(socket, this.running_flag, this.active_workers);
		this.IncrementActiveWorkers();
		this.ExecuteWorker(worker);
	}

	private void IncrementActiveWorkers() {
		this.active_workers.getAndDecrement();
	}

	private void ExecuteWorker(Worker worker) {
		this.thread_pool.execute(worker);
	}

	
	
	@Override
	public void shutdown() {
		while (this.IsWorkersActive()) {
			Sleep(5000);
		}
		this.CloseServer();

	}

	private boolean IsWorkersActive() {
		if (this.GetActiveWorkers() > 0) {
			return true;
		}
		return false;
	}

	private int GetActiveWorkers() {
		return this.active_workers.get();
	}

	
	
	private void Sleep(int miliseconds) {
		System.out.println("WARNING: There are still active connections");
		try {
			Thread.sleep(5000);
		} catch (InterruptedException e) {
			e.printStackTrace();
		}
	}

	private void CloseServer() {
		this.CloseServerSocket();
		this.CloseThreadPool();
	}

	private void CloseServerSocket() {
		try {
			this.server_socket.close();
		} catch (IOException e) {
			e.printStackTrace();
		}
	}

	private void CloseThreadPool() {
		this.thread_pool.shutdown();
	}

	
	
	@Override
	public boolean getRunningFlag() {
		return running_flag.get();
	}

	
	
	public static void main(String[] args) {
		int port = 10002;
		int number_of_threads = 4;
		int backlog = 10;
		int blocking_timeout = 500;

		ServerIf server = new MultithreadedServer(port, number_of_threads, backlog, blocking_timeout);

		server.loop();
		server.shutdown();

	}

}
