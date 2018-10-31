package mjaksic.distributed_system_client.measurements;

import com.opencsv.bean.CsvBindByName;

public class Measurement {

	@CsvBindByName
	private int Temperature;
	@CsvBindByName
	private int Pressure;
	@CsvBindByName
	private int Humidity;
	@CsvBindByName
	private int CO;
	@CsvBindByName
	private int NO2;
	@CsvBindByName
	private int SO2;

	public int getTemperature() {
		return Temperature;
	}

	public void setTemperature(int temperature) {
		Temperature = temperature;
	}

	public int getPressure() {
		return Pressure;
	}

	public void setPressure(int pressure) {
		Pressure = pressure;
	}

	public int getHumidity() {
		return Humidity;
	}

	public void setHumidity(int humidity) {
		Humidity = humidity;
	}

	public int getCO() {
		return CO;
	}

	public void setCO(int cO) {
		CO = cO;
	}

	public int getNO2() {
		return NO2;
	}

	public void setNO2(int nO2) {
		NO2 = nO2;
	}

	public int getSO2() {
		return SO2;
	}

	public void setSO2(int sO2) {
		SO2 = sO2;
	}

}
