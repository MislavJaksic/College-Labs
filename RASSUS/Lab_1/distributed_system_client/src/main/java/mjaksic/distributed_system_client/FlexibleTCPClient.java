package mjaksic.distributed_system_client;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.io.OutputStreamWriter;
import java.io.PrintWriter;
import java.net.Socket;

public class FlexibleTCPClient {

	private int port;
	private String server_name;

	private Socket client_socket;
	private BufferedReader server_reader;
	private PrintWriter server_writer;
	private BufferedReader user_input_reader;

	public FlexibleTCPClient(int port, String server_name) {
		this.port = port;
		this.server_name = server_name;

		this.client_socket = this.CreateClientSocket();
		this.server_reader = this.CreateReader();
		this.server_writer = this.CreateWriter();
		this.user_input_reader = this.CreateUserInputReader();
	}

	private Socket CreateClientSocket() {
		Socket socket = null;
		try {
			socket = new Socket(this.server_name, this.port);
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
			stream = this.client_socket.getInputStream();
		} catch (IOException e) {
			e.printStackTrace();
		}
		return stream;
	}

	private PrintWriter CreateWriter() {
		OutputStream stream = this.CreateOutputStream();
		OutputStreamWriter stream_writer = new OutputStreamWriter(stream);
		PrintWriter server_writer = new PrintWriter(stream_writer, true);
		return server_writer;
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

	private BufferedReader CreateUserInputReader() {
		InputStream stream = System.in;
		InputStreamReader stream_reader = new InputStreamReader(stream);
		BufferedReader server_reader = new BufferedReader(stream_reader);
		return server_reader;
	}

	
	
	public void Start() {
		String user_input;
		String received_string;

		while (true) {
			user_input = this.ReadUserInput();

			if (this.IsShutdownCommand(user_input)) {
				break;
			}
			this.WriteToServer(user_input);
			received_string = this.ReadFromServer();
		}
		this.CloseSocket();
		System.out.println("Shutdown successful");
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

	private String ReadFromServer() {
		String received_string = null;
		try {
			received_string = server_reader.readLine();
			System.out.println("Sensor received:::" + received_string);
		} catch (IOException e) {
			e.printStackTrace();
		}
		return received_string;
	}

	private void WriteToServer(String string) {
		this.server_writer.println(string);
		System.out.println("Sensor sent:::" + string);
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
	
	private void CloseSocket() {
		try {
			this.client_socket.close();
			System.out.println("Sensor socket closed");
		} catch (IOException e) {
			e.printStackTrace();
		}
	}

	
	
	public static void main(String args[]) {
		int port = 10002;
		String server_name = "localhost";

		FlexibleTCPClient client = new FlexibleTCPClient(port, server_name);
		client.Start();
	}

}
