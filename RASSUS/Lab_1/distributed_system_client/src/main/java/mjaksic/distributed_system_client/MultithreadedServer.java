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
		this.thread_pool = this.CreateThreadPool();
		this.running_flag = this.CreateAtomicBoolean();
		
		this.server_socket = this.CreateServerSocket();
		this.SetSocketBlockingTimeout(blocking_timeout);
	}

	private AtomicInteger CreateAtomicInteger() {
		System.out.println("Creating atomic integer");
		return new AtomicInteger(0);
	}
	
	private ExecutorService CreateThreadPool() {
		System.out.println("Creating thread pool");
		return Executors.newFixedThreadPool(this.number_of_threads);
	}
	
	private AtomicBoolean CreateAtomicBoolean() {
		System.out.println("Creating atomic boolean");
		return new AtomicBoolean(true);
	}

	private ServerSocket CreateServerSocket() {
		ServerSocket server_socket = null;
		try {
			server_socket = new ServerSocket(this.port, this.backlog);
			System.out.println("Created server socket");
		} catch (IOException e) {
			e.printStackTrace();
		}
		return server_socket;
	}

	private void SetSocketBlockingTimeout(int blocking_timeout) {
		try {
			this.server_socket.setSoTimeout(blocking_timeout);
			System.out.println("Set blocking timeout");
		} catch (SocketException e) {
			e.printStackTrace();
		}
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
		boolean flag = this.running_flag.get();
		System.out.println("Running flag is " + flag);
		return flag;
	}

	private Socket AcceptConnectionAndCreateSocket() {
		System.out.println("Listening for a connection");
		Socket socket = null;
		try {
			socket = this.server_socket.accept();
			System.out.println("Connection accepted");
		} catch (IOException e) {
			System.out.println("Listening time expired");
		}
		return socket;
	}

	private void MakeWorkerUsingSocket(Socket socket) {
		if (this.IsSocket(socket)) {
			Worker worker = new Worker(socket, this.running_flag, this.active_workers);
			this.IncrementActiveWorkers();
			this.ExecuteWorker(worker);
		}
	}
	
	private boolean IsSocket(Socket socket) {
		if(socket != null) {
			System.out.println("Socket exists");
			return true;
		}
		return false;
	}

	private void IncrementActiveWorkers() {
		this.active_workers.getAndIncrement();
		System.out.println("Incremented workers to " + this.active_workers.get());
	}

	private void ExecuteWorker(Worker worker) {
		this.thread_pool.execute(worker);
		System.out.println("Executed a worker");
	}

	
	
	@Override
	public void shutdown() {
		System.out.println("Shutdown has begun...");
		while (this.IsWorkersActive()) {
			this.Sleep(5000);
		}
		this.CloseServer();
		System.out.println("Shutdown successful");
	}

	private boolean IsWorkersActive() {
		int active_workers = this.GetActiveWorkers();
		if (active_workers > 0) {
			System.out.println("There are still " + active_workers + " active workers");
			return true;
		}
		return false;
	}

	private int GetActiveWorkers() {
		return this.active_workers.get();
	}

	private void Sleep(int miliseconds) {
		System.out.println("Sleeping...");
		try {
			Thread.sleep(5000);
		} catch (InterruptedException e) {
			e.printStackTrace();
		}
	}

	
	
	private void CloseServer() {
		System.out.println("Closing server...");
		this.CloseServerSocket();
		this.CloseThreadPool();
	}

	private void CloseServerSocket() {
		try {
			this.server_socket.close();
			System.out.println("Server socket closed");
		} catch (IOException e) {
			e.printStackTrace();
		}
	}

	private void CloseThreadPool() {
		this.thread_pool.shutdown();
		System.out.println("Thread pool closed");
	}

	
	
	@Override
	public boolean getRunningFlag() {
		return running_flag.get();
	}

	
	
	public static void main(String[] args) {
		int port = 10002;
		int number_of_threads = 4;
		int backlog = 10;
		int blocking_timeout = 2500;

		ServerIf server = new MultithreadedServer(port, number_of_threads, backlog, blocking_timeout);

		server.loop();
		server.shutdown();

	}

}
