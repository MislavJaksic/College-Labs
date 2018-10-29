package mjaksic.distributed_system_server;

public class SensorRegistrationForm extends SensorAddress {

	private final String id;
	private final double longitude;
	private final double latitude;

	
	public SensorRegistrationForm(String ip, int port, String id, double longitude, double latitude) {
		super(ip, port);
		this.id = id;
		this.longitude = longitude;
		this.latitude = latitude;
	}

	public String getId() {
		return id;
	}

	public double getLongitude() {
		return longitude;
	}

	public double getLatitude() {
		return latitude;
	}

	@Override
	public String toString() {
		return "SensorRegistrationForm [id=" + id + ", longitude=" + longitude + ", latitude=" + latitude
				+ ", toString()=" + super.toString() + "]";
	}

}
