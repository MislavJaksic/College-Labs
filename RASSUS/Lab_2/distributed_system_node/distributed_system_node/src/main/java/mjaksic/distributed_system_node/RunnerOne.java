package mjaksic.distributed_system_node;

import java.util.ArrayList;

import mjaksic.distributed_system_node.sensor.Sensor;

public class RunnerOne {
	
	public static void main(String[] args) {
		ArrayList<Integer> ports = new ArrayList<Integer>();
		ports.add(10000);
		ports.add(10001);
		//ports.add(10002);
		
		Sensor sensor_A = new Sensor(ports);
	}
}
