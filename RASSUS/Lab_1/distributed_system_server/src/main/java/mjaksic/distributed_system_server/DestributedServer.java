package mjaksic.distributed_system_server;

public interface DestributedServer {
	boolean register(SensorRegistrationForm form);
	
	SensorAddress SearchNeighbour(String username);
	
	boolean StoreMeasurement(String username, String parameter, float avarage);
}
