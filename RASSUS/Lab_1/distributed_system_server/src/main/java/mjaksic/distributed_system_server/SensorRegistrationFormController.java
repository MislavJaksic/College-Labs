package mjaksic.distributed_system_server;

import java.util.HashMap;
import java.util.Map;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.ResponseBody;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class SensorRegistrationFormController {

	private static final Logger logger = LoggerFactory.getLogger(SensorRegistrationFormController.class);

	private Map<String, SensorRegistrationForm> sensors = new HashMap<>();
	private Map<String, SensorRegistrationForm> closest = new HashMap<>();

	@PutMapping("/sensor/{id}")
	public @ResponseBody SensorRegistrationForm PutForm(@PathVariable("id") String id,
			@RequestBody SensorRegistrationForm sensor) {
		this.RegisterSensor(id, sensor);
		this.RefreshClosestSensors();

		return sensor;
	}

	@GetMapping("sensor/{id}")
	public @ResponseBody SensorRegistrationForm GetForm(@PathVariable("id") String id) {
		return GetRegisteredSensor(id);
	}

	@GetMapping("sensor/{id}/closest")
	public @ResponseBody SensorRegistrationForm GetClosest(@PathVariable("id") String id) {
		return GetClosestSensor(id);
	}
	
	
	
	private void RegisterSensor(String id, SensorRegistrationForm sensor) {
		this.sensors.put(id, sensor);
	}
	
	private SensorRegistrationForm GetRegisteredSensor(String id) {
		return this.sensors.get(id);
	}
	
	
	
	private SensorRegistrationForm GetClosestSensor(String id) {
		return this.closest.get(id);
	}
	
	
	
	private void RefreshClosestSensors() {
		SensorRegistrationForm closest_sensor;
		
		for (Map.Entry<String, SensorRegistrationForm> id_sensor_pair : this.sensors.entrySet()) {
			String id = id_sensor_pair.getKey();
			SensorRegistrationForm sensor = id_sensor_pair.getValue();

			closest_sensor = FindClosestSensor(id, sensor);
			this.closest.put(id, closest_sensor);
		}
	}

	private SensorRegistrationForm FindClosestSensor(String id, SensorRegistrationForm sensor) {
    	SensorRegistrationForm closest_sensor = new SensorRegistrationForm("255.255.255.255", 0, 0.0, 0.0);
    	double smallest_distance = Double.MAX_VALUE;
    	double distance;
    	
    	for (Map.Entry<String, SensorRegistrationForm> id_sensor_candidate_pair : this.sensors.entrySet()) {
    		String candidate_id = id_sensor_candidate_pair.getKey();
    		SensorRegistrationForm candidate_sensor = id_sensor_candidate_pair.getValue();
    		
    		if (id.equals(candidate_id)) {
    			continue;
    		}
    		
    		distance = this.CalculateHaversineDistance(sensor, candidate_sensor);
    		
    		if (smallest_distance > distance) {
    			smallest_distance = distance;
    			closest_sensor = candidate_sensor;
    		}
    	}
    	
    	SensorRegistrationFormController.logger.info("FindClosestSensor::" + sensor + "::smallest_distance is " + smallest_distance);
    	
    	return closest_sensor;
    }

	private double CalculateHaversineDistance(SensorRegistrationForm form_A, SensorRegistrationForm form_B) {
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

		int earth_radius = 6371;

		double haversine_distance = earth_radius * c;
		return haversine_distance;
	}

}
