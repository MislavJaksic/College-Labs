package mjaksic.distributed_system_client;

import java.io.IOException;
import java.net.ServerSocket;
import java.util.Random;

public class PortGenerator {

	private static final int min_port = 49152;
	private static final int max_port = 65535;
	
	private static int max_backlog = 5;
	
	public static int GetValidPort() {
		return 1;
	}
	
	public static int GetPort() {
		Random random_seed = new Random();
		int port = PortGenerator.min_port + (PortGenerator.max_port - PortGenerator.min_port) * random_seed.nextInt();
		return port;
	}
	
	
	
	private static int TestServerSocket() {
		ServerSocket server_socket = null;
		int port = PortGenerator.GetPort();
		while (!PortGenerator.IsSocket(server_socket)) {
			port = PortGenerator.GetPort();
			server_socket = PortGenerator.CreateServerSocket(port);
		}
		
		return port;
	}
	
	private static boolean IsSocket(ServerSocket socket) {
		if(socket != null) {
			return true;
		}
		return false;
	}
	
	private static ServerSocket CreateServerSocket(int port) {
		ServerSocket server_socket = null;
		try {
			server_socket = new ServerSocket(port, PortGenerator.max_backlog);
		} catch (IOException e) {
			System.out.println("Port " + port + " taken, pick another");
		}
		return server_socket;
	}
	
	private static void CloseServerSocket() {
		
	}

}
