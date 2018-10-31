package mjaksic.distributed_system_server;

import java.util.HashMap;
import java.util.Map;
import java.util.logging.Level;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.ResponseBody;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class SensorRegistrationController {

	private static final Logger logger = LoggerFactory.getLogger(SensorRegistrationController.class);

	private Map<String, SensorRegistration> sensors = new HashMap<>();
	private Map<String, SensorRegistration> closest = new HashMap<>();

	
	
	@PutMapping("/sensor/{id}")
	public @ResponseBody SensorRegistration PutForm(@PathVariable("id") String id,
			@RequestBody SensorRegistration sensor) {
		this.RegisterSensor(id, sensor);
		this.RefreshClosestSensors();

		return sensor;
	}

	private void RegisterSensor(String id, SensorRegistration sensor) {
		this.sensors.put(id, sensor);
		this.LogString("Sensor id=" + id + " " + sensor + " has been registered");
	}

	private void RefreshClosestSensors() {
		DistanceCalculator calculator = new DistanceCalculator(this.sensors);
		this.closest = calculator.GetClosestSensors();
		
		for (Map.Entry<String, SensorRegistration> id_sensor_pair : this.closest.entrySet()) {
			this.LogString("Sensor id=" + id_sensor_pair.getKey() + " is closest to " + id_sensor_pair.getValue());
		}
	}

	
	
	@GetMapping("sensor/{id}")
	public @ResponseBody SensorRegistration GetForm(@PathVariable("id") String id) {
		return GetRegisteredSensor(id);
	}

	private SensorRegistration GetRegisteredSensor(String id) {
		return this.sensors.get(id);
	}

	
	
	@GetMapping("sensor/{id}/closest")
	public @ResponseBody SensorRegistration GetClosest(@PathVariable("id") String id) {
		return GetClosestSensor(id);
	}

	private SensorRegistration GetClosestSensor(String id) {
		return this.closest.get(id);
	}
	
	
	
	private void LogString(String string) {
		SensorRegistrationController.logger.info(string);
	}
}
