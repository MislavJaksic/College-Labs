package mjaksic.distributed_system_node.measurements;

import java.io.FileNotFoundException;
import java.io.FileReader;
import java.util.List;

import com.opencsv.bean.CsvToBeanBuilder;

public class MeasurementsReader {

	public static List<Measurement> ReadFilesAsList(String file_name) {
		CsvToBeanBuilder<Measurement> bean_builder = MeasurementsReader.CreateMeasurementsCSVBeanBuilder(file_name);
		List<Measurement> list = bean_builder.withType(Measurement.class).build().parse();
		return list;
	}

	private static CsvToBeanBuilder<Measurement> CreateMeasurementsCSVBeanBuilder(String file_name) {
		FileReader file_reader = MeasurementsReader.CreateFileReader(file_name);
		CsvToBeanBuilder<Measurement> bean_builder = new CsvToBeanBuilder<Measurement>(file_reader);
		return bean_builder;
	}

	private static FileReader CreateFileReader(String file_name) {
		FileReader reader = null;
		try {
			reader = new FileReader(file_name);
		} catch (FileNotFoundException e) {
			e.printStackTrace();
		}
		return reader;
	}
}
