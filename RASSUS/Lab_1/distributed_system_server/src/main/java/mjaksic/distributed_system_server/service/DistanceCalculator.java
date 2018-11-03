package mjaksic.distributed_system_server.service;

import java.util.HashMap;
import java.util.Map;

public class DistanceCalculator {

	private final static int earth_radius = 6371;
	private Map<String, SensorRegistration> sensors;
	
	public DistanceCalculator(Map<String, SensorRegistration> sensors) {
		this.sensors = sensors;
	}

	public Map<String, SensorRegistration> GetClosestSensors() {
        String sensor_id;
        SensorRegistration sensor_registration;
		SensorRegistration closest_registration;
		HashMap<String, SensorRegistration> closest_sensors = new HashMap<>();
		
		for (Map.Entry<String, SensorRegistration> id_sensor_pair : this.sensors.entrySet()) {
			sensor_id = id_sensor_pair.getKey();
			sensor_registration = id_sensor_pair.getValue();

			closest_registration = this.FindClosestSensor(sensor_id, sensor_registration);
			closest_sensors.put(sensor_id, closest_registration);
		}
		
		return closest_sensors;
	}

	private SensorRegistration FindClosestSensor(String sensor_id, SensorRegistration sensor_registration) {
		SensorRegistration closest_registration = new SensorRegistration("255.255.255.255", 0, 0.0, 0.0);
		
		String candidate_id;
    	SensorRegistration candidate_registration;
    	
		double smallest_distance = Double.MAX_VALUE;
    	double distance;
    	
    	
    	for (Map.Entry<String, SensorRegistration> id_sensor_candidate_pair : this.sensors.entrySet()) {
    		candidate_id = id_sensor_candidate_pair.getKey();
    		candidate_registration = id_sensor_candidate_pair.getValue();
    		
    		if (this.IsSameSensor(sensor_id, candidate_id)) {
    			continue;
    		}
    		
    		distance = this.CalculateHaversineDistance(sensor_registration, candidate_registration);
    		
    		if (this.IsASmallerThenB(distance, smallest_distance)) {
    			smallest_distance = distance;
    			closest_registration = candidate_registration;
    		}
    	}
    	
    	return closest_registration;
    }
	
	private boolean IsSameSensor(String id_A, String id_B) {
		if (id_A.equals(id_B)) {
			return true;
		}
		return false;
	}
	
	private boolean IsASmallerThenB(double A, double B) {
		if (A < B) {
			return true;
		}
		return false;
	}

	private double CalculateHaversineDistance(SensorRegistration form_A, SensorRegistration form_B) {
		double longitude_A = form_A.getLongitude();
		double longitude_B = form_B.getLongitude();
		double latitude_A = form_A.getLatitude();
		double latitude_B = form_B.getLatitude();

		double longitude_difference = longitude_A - longitude_B;
		double latitude_difference = latitude_A - latitude_B;

		double sin_lat = Math.sin(latitude_difference / 2);
		double sin_long = Math.sin(longitude_difference / 2);

		double a = Math.pow(sin_lat, 2.0) + Math.cos(latitude_B) * Math.cos(latitude_A) * Math.pow(sin_long, 2.0);
		double c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));

		double haversine_distance = earth_radius * c;
		return haversine_distance;
	}

}
