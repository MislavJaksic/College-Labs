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

    @PutMapping("/register")
    public @ResponseBody SensorRegistrationForm PutForm(@RequestBody SensorRegistrationForm form) {
    	SensorRegistrationFormController.logger.info("PutForm::" + form);
    	
    	this.sensors.put(form.getId(), form);
        return form;
    }
    
    @GetMapping("/{id}")
    public @ResponseBody SensorRegistrationForm GetForm(@PathVariable("id") String id) {
    	SensorRegistrationForm form = this.sensors.get(id);
    	
    	SensorRegistrationFormController.logger.info("GetForm::" + form);
    	
        return form;
    }

}
