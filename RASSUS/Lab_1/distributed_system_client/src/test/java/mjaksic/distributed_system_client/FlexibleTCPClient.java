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
	private BufferedReader reader;
	private PrintWriter writer;
	private BufferedReader user_input_reader;
	

	public FlexibleTCPClient(int port, String server_name) {
		this.port = port;
		this.server_name = server_name;
		
		this.client_socket = this.CreateClientSocket();
		this.reader = this.CreateReader();
		this.writer = this.CreateWriter();
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
		BufferedReader reader = new BufferedReader(stream_reader);
		return reader;
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

	private BufferedReader CreateUserInputReader() {
		InputStream stream = System.in;
		InputStreamReader stream_reader = new InputStreamReader(stream);
		BufferedReader reader = new BufferedReader(stream_reader);
		return reader;
	}
	
	public void Start() {
			String user_input;
			System.out.println("Insert new line of text: "); //TODO, continue refactoring!

			while ((user_input = user_input_reader.readLine()) != null && user_input.length() != 0) {
				// send a String then terminate the line and flush
				writer.println(user_input);// WRITE
				System.out.println("TCPClient sent: " + user_input);
				// read a line of text received from server
				String rcvString = reader.readLine();// READ
				System.out.println("TCPClient received: " + rcvString);
				if (user_input.equals("shutdown"))
					break;
				System.out.println("Insert new line of text: ");
			}
			client_socket.close(); // CLOSE client socket
	}
	
	private String ReadUserInput() {
		String received_string = null;
		try {
			received_string = this.user_input_reader.readLine();
		} catch (IOException e) {
			e.printStackTrace();
		}
		return received_string;
	}
	
	private boolean IsShutdownCommand(String string) {
		if (string == null) {
			return true;
		}
		if (string.length() == 0) {
			return true;
		}
		return false;
	}
	
	

	public static void main(String args[]) {
		int port = 10002;
		String server_name = "localhost";

		FlexibleTCPClient client = new FlexibleTCPClient(port, server_name);
		client.Start();
	}

}
