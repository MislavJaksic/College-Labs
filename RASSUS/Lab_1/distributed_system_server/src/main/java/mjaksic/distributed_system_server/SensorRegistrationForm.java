package mjaksic.distributed_system_server;

public class SensorRegistrationForm extends SensorAddress {

	private final double longitude;
	private final double latitude;

	
	public SensorRegistrationForm(String ip, int port, double longitude, double latitude) {
		super(ip, port);
		this.longitude = longitude;
		this.latitude = latitude;
	}
	
	public double getLongitude() {
		return longitude;
	}

	public double getLatitude() {
		return latitude;
	}

	@Override
	public String toString() {
		return "SensorRegistrationForm [longitude=" + longitude + ", latitude=" + latitude
				+ ", toString()=" + super.toString() + "]";
	}

}
