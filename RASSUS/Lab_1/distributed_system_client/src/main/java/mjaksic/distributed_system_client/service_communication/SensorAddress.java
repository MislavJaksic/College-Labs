package mjaksic.distributed_system_client.service_communication;

public class SensorAddress {

	private final String ip;
	private final int port;

	public SensorAddress(String ip, int port) {
		this.ip = ip;
		this.port = port;
	}

	public String getIp() {
		return ip;
	}

	public int getPort() {
		return port;
	}

	@Override
	public String toString() {
		return "SensorAddress [ip=" + ip + ", port=" + port + "]";
	}
}
