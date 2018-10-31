package mjaksic.distributed_system_server;

public interface SensorServer {
	boolean register(SensorRegistration form);
	
	SensorAddress SearchNeighbour(String username);
	
	boolean StoreMeasurement(String username, String parameter, float avarage);
}
