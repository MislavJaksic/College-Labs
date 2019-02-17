package mjaksic.distributed_system_node.measurement;

import java.util.List;

public class MeasurementSimulator {
	
	private static final String file_name = "Measurements.csv";
	private static final List<Measurement> measurements = MeasurementsReader.ReadFilesAsList(file_name);

	public static Measurement GetMeasurementBasedOnTime(int time) {
		int index = MeasurementSimulator.CalculateIndex(time);
		return measurements.get(index);
	}
	
	private static int CalculateIndex(int seconds) {
		return seconds % 100;
	}

}
